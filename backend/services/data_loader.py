"""
data_loader.py
Handles loading and basic cleaning of Brent oil price data and event data.
Falls back to generated placeholder price data if the real dataset
(BrentOilPrices.csv) has not been added yet, so the API can be tested
before Task 2 analysis is complete.
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PRICES_FILE = os.path.join(DATA_DIR, "BrentOilPrices.csv")
EVENTS_FILE = os.path.join(DATA_DIR, "events.csv")
CHANGEPOINTS_FILE = os.path.join(DATA_DIR, "change_points.json")


def load_prices():
    """
    Loads Brent oil price data.
    Expects columns: Date, Price
    If the real file is not present yet, generates placeholder
    synthetic data so the API/frontend can be developed in parallel.
    """
    if os.path.exists(PRICES_FILE):
        df = pd.read_csv(PRICES_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
        df = df.dropna(subset=["Date"]).sort_values("Date")
        return df

    # --- Placeholder synthetic data (used only until real CSV is added) ---
    dates = pd.date_range(start="2015-01-01", end="2022-09-30", freq="D")
    rng = np.random.default_rng(seed=42)
    price = 50 + np.cumsum(rng.normal(0, 0.5, size=len(dates)))
    price = np.clip(price, 20, 130)
    df = pd.DataFrame({"Date": dates, "Price": price})
    return df


def load_events():
    """Loads the researched events CSV."""
    df = pd.read_csv(EVENTS_FILE)
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    return df.dropna(subset=["event_date"])


def load_changepoints():
    """
    Loads change point results produced by the Task 2 PyMC model.
    Returns placeholder data if the real results file isn't ready yet.
    """
    if os.path.exists(CHANGEPOINTS_FILE):
        return pd.read_json(CHANGEPOINTS_FILE)

    # Placeholder change point result
    return pd.DataFrame([
        {
            "change_point_date": "2020-03-08",
            "mean_before": 60.2,
            "mean_after": 33.4,
            "percent_change": -44.5,
            "likely_event": "Saudi-Russia Price War / COVID-19 Demand Collapse"
        }
    ])