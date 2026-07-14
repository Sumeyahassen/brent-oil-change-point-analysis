"""
analyze_prices.py
Exploratory Data Analysis (EDA) of Brent oil prices, aligned with Task 1
requirements: trend analysis, stationarity testing, and volatility patterns.
Also cross-references detected high-volatility periods with the compiled
events dataset.

Run from the `backend` folder with:
    python3 analysis/analyze_prices.py

Outputs (saved to backend/outputs/):
    - price_trend.png
    - log_returns.png
    - rolling_volatility.png
    - stationarity_report.txt
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no display needed, just save files
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller # type: ignore

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.data_loader import load_prices, load_events

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_adf_test(series, label):
    """Runs the Augmented Dickey-Fuller stationarity test and returns a summary string."""
    series = series.dropna()
    result = adfuller(series)
    lines = [
        f"--- ADF Test: {label} ---",
        f"ADF Statistic: {result[0]:.4f}",
        f"p-value: {result[1]:.4f}",
        f"Critical Values:"
    ]
    for key, value in result[4].items():
        lines.append(f"    {key}: {value:.4f}")

    if result[1] < 0.05:
        lines.append("Result: Stationary (reject null hypothesis of a unit root)")
    else:
        lines.append("Result: Non-stationary (fail to reject null hypothesis of a unit root)")
    lines.append("")
    return "\n".join(lines)


def plot_price_trend(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df["Price"], linewidth=0.8, color="#1F4E79")
    plt.title("Brent Oil Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD/barrel)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "price_trend.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Saved: {path}")


def plot_log_returns(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df["log_return"], linewidth=0.5, color="#C00000")
    plt.title("Brent Oil Log Returns (Volatility Clustering)")
    plt.xlabel("Date")
    plt.ylabel("Log Return")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "log_returns.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Saved: {path}")


def plot_rolling_volatility(df, window=30):
    df["rolling_vol"] = df["log_return"].rolling(window=window).std()
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df["rolling_vol"], linewidth=0.8, color="#548235")
    plt.title(f"{window}-Day Rolling Volatility of Log Returns")
    plt.xlabel("Date")
    plt.ylabel("Rolling Std Dev")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "rolling_volatility.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Saved: {path}")
    return df


def cross_reference_events(df, events_df, window=30):
    """
    For each event, reports the average rolling volatility in the
    `window` days after the event date, to see which events line up
    with elevated volatility.
    """
    print("\n=== Volatility Around Events (30-day avg after event) ===")
    for _, event in events_df.iterrows():
        mask = (df["Date"] >= event["event_date"]) & \
               (df["Date"] <= event["event_date"] + pd.Timedelta(days=window))
        avg_vol = df.loc[mask, "rolling_vol"].mean()
        if pd.notna(avg_vol):
            print(f"{event['event_date'].date()} | {event['event_name']:<35} | avg volatility: {avg_vol:.4f}")


def main():
    print("Loading data...")
    prices = load_prices()
    events = load_events()

    # --- Log returns ---
    prices["log_return"] = np.log(prices["Price"]) - np.log(prices["Price"].shift(1))

    # --- Trend plot ---
    plot_price_trend(prices)

    # --- Log returns plot ---
    plot_log_returns(prices)

    # --- Rolling volatility ---
    prices = plot_rolling_volatility(prices)

    # --- Stationarity tests ---
    report = ""
    report += run_adf_test(prices["Price"], "Raw Price Series")
    report += run_adf_test(prices["log_return"], "Log Returns Series")

    report_path = os.path.join(OUTPUT_DIR, "stationarity_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved: {report_path}")
    print("\n" + report)

    # --- Cross-reference with events ---
    cross_reference_events(prices, events)


if __name__ == "__main__":
    main()