"""
changepoint_model.py
Task 2: Bayesian Change Point Detection for Brent Oil Prices.

Builds a PyMC model that detects a single structural break (change point)
in the Brent oil log-return series, following the brief's specification:
    - tau: discrete uniform prior over the switch point
    - mu1, mu2: "before" and "after" mean parameters
    - pm.math.switch to select the correct mean based on tau
    - Normal likelihood connecting the model to observed log returns

Run from the `backend` folder with:
    python3 analysis/changepoint_model.py

Outputs (saved to backend/outputs/):
    - trace_plot.png              convergence diagnostics
    - posterior_tau.png           posterior distribution of the change point
    - posterior_means.png         posterior distributions of mu1 / mu2
    - model_summary.txt           pm.summary() table (r_hat, etc.)
    - change_points.json          machine-readable result for the dashboard API
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import pymc as pm # type: ignore
import arviz as az # type: ignore
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.data_loader import load_prices, load_events

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def prepare_data():
    """Loads prices and returns a clean log-return series with a reset integer index."""
    prices = load_prices()
    prices["log_return"] = np.log(prices["Price"]) - np.log(prices["Price"].shift(1))
    prices = prices.dropna(subset=["log_return"]).reset_index(drop=True)
    return prices


def build_and_run_model(prices, draws=3000, tune=3000, chains=4):
    """
    Builds the PyMC change point model and runs MCMC sampling.
    Returns the fitted model and the inference trace (idata).
    """
    log_returns = prices["log_return"].values
    n = len(log_returns)

    with pm.Model() as model:
        # Discrete uniform prior over the switch point (day index)
        tau = pm.DiscreteUniform("tau", lower=0, upper=n - 1)

        # "Before" and "after" mean parameters
        mu1 = pm.Normal("mu1", mu=0, sigma=0.05)
        mu2 = pm.Normal("mu2", mu=0, sigma=0.05)

        # Shared standard deviation (kept simple per the brief's mean-shift model)
        sigma = pm.HalfNormal("sigma", sigma=0.05)

        # Switch function: select mu1 before tau, mu2 after tau
        idx = np.arange(n)
        mu = pm.math.switch(idx >= tau, mu2, mu1)

        # Likelihood
        likelihood = pm.Normal("likelihood", mu=mu, sigma=sigma, observed=log_returns)

        # Run the sampler
        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=1,
            target_accept=0.9,
            return_inferencedata=True,
            progressbar=True
        )

    return model, idata


def check_convergence(idata):
    """Prints and saves the pm.summary() table (r_hat, ess, etc.)."""
    summary = az.summary(idata, var_names=["tau", "mu1", "mu2", "sigma"])
    print("\n=== Model Summary (Convergence Diagnostics) ===")
    print(summary)

    path = os.path.join(OUTPUT_DIR, "model_summary.txt")
    with open(path, "w") as f:
        f.write(summary.to_string())
    print(f"Saved: {path}")

    max_rhat = pd.to_numeric(summary["r_hat"], errors="coerce").max()
    if max_rhat < 1.05:
        print(f"Convergence looks good (max r_hat = {max_rhat:.3f})")
    else:
        print(f"WARNING: max r_hat = {max_rhat:.3f} — consider more tuning/draws")

    return summary


def plot_trace(idata):
    az.plot_trace(idata, var_names=["tau", "mu1", "mu2", "sigma"])
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "trace_plot.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Saved: {path}")


def plot_posterior_tau(idata, prices):
    tau_samples = idata.posterior["tau"].values.flatten()
    most_likely_idx = int(np.round(np.median(tau_samples)))
    change_date = prices.loc[most_likely_idx, "Date"]

    plt.figure(figsize=(10, 4))
    plt.hist(tau_samples, bins=100, color="#1F4E79")
    plt.axvline(most_likely_idx, color="red", linestyle="--", label=f"Most likely: {change_date.date()}")
    plt.title("Posterior Distribution of Change Point (tau)")
    plt.xlabel("Day Index")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "posterior_tau.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Saved: {path}")

    return most_likely_idx, change_date


def plot_posterior_means(idata):
    """
    Plots posterior histograms for mu1 (before) and mu2 (after) using plain
    matplotlib, avoiding dependence on ArviZ's plotting API (which has
    changed across versions).
    """
    mu1_samples = idata.posterior["mu1"].values.flatten()
    mu2_samples = idata.posterior["mu2"].values.flatten()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].hist(mu1_samples, bins=60, color="#1F4E79", alpha=0.85)
    axes[0].axvline(mu1_samples.mean(), color="red", linestyle="--",
                     label=f"mean = {mu1_samples.mean():.5f}")
    axes[0].set_title("Posterior: mu1 (before change point)")
    axes[0].set_xlabel("Mean log return")
    axes[0].legend()

    axes[1].hist(mu2_samples, bins=60, color="#C00000", alpha=0.85)
    axes[1].axvline(mu2_samples.mean(), color="red", linestyle="--",
                     label=f"mean = {mu2_samples.mean():.5f}")
    axes[1].set_title("Posterior: mu2 (after change point)")
    axes[1].set_xlabel("Mean log return")
    axes[1].legend()

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "posterior_means.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Saved: {path}")


def quantify_impact(idata, prices, change_idx, change_date):
    """
    Converts the mean log-return shift into an interpretable price-level
    impact statement, and finds the nearest researched event.
    """
    mu1_samples = idata.posterior["mu1"].values.flatten()
    mu2_samples = idata.posterior["mu2"].values.flatten()

    mu1_mean = mu1_samples.mean()
    mu2_mean = mu2_samples.mean()

    # Average price in a 30-day window before and after the change point
    before_window = prices.iloc[max(0, change_idx - 30):change_idx]
    after_window = prices.iloc[change_idx:change_idx + 30]
    price_before = before_window["Price"].mean()
    price_after = after_window["Price"].mean()
    pct_change = (price_after - price_before) / price_before * 100

    # Probability mu2 > mu1 (i.e. shift was an increase)
    prob_increase = (mu2_samples > mu1_samples).mean()

    # Find nearest event
    events = load_events()
    events["days_diff"] = (events["event_date"] - change_date).abs().dt.days
    nearest_event = events.loc[events["days_diff"].idxmin()]

    result = {
        "change_point_date": str(change_date.date()),
        "mean_log_return_before": float(mu1_mean),
        "mean_log_return_after": float(mu2_mean),
        "avg_price_before": round(float(price_before), 2),
        "avg_price_after": round(float(price_after), 2),
        "percent_change": round(float(pct_change), 2),
        "probability_increase": round(float(prob_increase), 3),
        "likely_event": nearest_event["event_name"],
        "likely_event_date": str(nearest_event["event_date"].date()),
        "days_from_event": int(nearest_event["days_diff"]) # type: ignore
    }

    print("\n=== Quantified Impact ===")
    for k, v in result.items():
        print(f"{k}: {v}")

    path = os.path.join(DATA_DIR, "change_points.json")
    with open(path, "w") as f:
        json.dump([result], f, indent=2)
    print(f"\nSaved: {path}")

    return result


def main():
    print("Loading and preparing data...")
    prices = prepare_data()
    print(f"Modeling {len(prices)} daily log returns "
          f"({prices['Date'].min().date()} to {prices['Date'].max().date()})")

    print("\nBuilding and sampling the model (this may take several minutes)...")
    model, idata = build_and_run_model(prices)

    check_convergence(idata)
    plot_trace(idata)
    change_idx, change_date = plot_posterior_tau(idata, prices)
    plot_posterior_means(idata)
    quantify_impact(idata, prices, change_idx, change_date)


if __name__ == "__main__":
    main()