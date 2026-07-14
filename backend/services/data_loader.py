"""
data_loader.py
Handles loading and cleaning of Brent oil price data and event data,
with robust error handling and clear failure messages.
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
    Loads Brent oil price data. Expects columns: Date, Price.

    Handles two known date formats in the instructor-provided dataset:
      - '15-Apr-20'      (day-month abbreviation-year)
      - 'Apr 22, 2020'   (month abbreviation day, year)

    Falls back to generated placeholder data if the real file is missing,
    and raises clear errors if the file exists but is malformed.
    """
    if not os.path.exists(PRICES_FILE):
        print(f"Notice: '{PRICES_FILE}' not found. Using placeholder synthetic data.")
        dates = pd.date_range(start="2015-01-01", end="2022-09-30", freq="D")
        rng = np.random.default_rng(seed=42)
        price = 50 + np.cumsum(rng.normal(0, 0.5, size=len(dates)))
        price = np.clip(price, 20, 130)
        return pd.DataFrame({"Date": dates, "Price": price})

    try:
        df = pd.read_csv(PRICES_FILE)
    except pd.errors.EmptyDataError:
        raise ValueError(f"'{PRICES_FILE}' exists but is empty.")
    except pd.errors.ParserError as e:
        raise ValueError(f"'{PRICES_FILE}' could not be parsed as CSV: {e}")

    if "Date" not in df.columns or "Price" not in df.columns:
        raise ValueError(
            f"'{PRICES_FILE}' is missing required columns. "
            f"Expected 'Date' and 'Price', found: {list(df.columns)}"
        )

    parsed_old = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
    parsed_new = pd.to_datetime(df["Date"], format="%b %d, %Y", errors="coerce")
    df["Date"] = parsed_old.fillna(parsed_new)

    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["Date", "Price"]).sort_values("Date").reset_index(drop=True)
    after = len(df)

    if after == 0:
        raise ValueError(
            f"'{PRICES_FILE}' was loaded but no valid rows remained after parsing. "
            f"Check the Date/Price formats match what this loader expects."
        )

    if before != after:
        print(f"Warning: dropped {before - after} rows with unparseable dates or prices.")

    return df


def load_events():
    """Loads the researched events CSV, with error handling for missing/malformed files."""
    if not os.path.exists(EVENTS_FILE):
        raise FileNotFoundError(
            f"Events file not found at '{EVENTS_FILE}'. "
            f"This file is a required Task 1 deliverable — make sure it's committed."
        )

    try:
        df = pd.read_csv(EVENTS_FILE)
    except pd.errors.EmptyDataError:
        raise ValueError(f"'{EVENTS_FILE}' exists but is empty.")

    required_cols = {"event_date", "event_name", "description", "category"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"'{EVENTS_FILE}' is missing required columns: {missing_cols}")

    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df.dropna(subset=["event_date"])

    if len(df) < 10:
        print(f"Warning: only {len(df)} valid events found; the brief requires at least 10-15.")

    return df


def load_changepoints():
    """
    Loads change point results produced by the Task 2 PyMC model.
    Returns placeholder data if the real results file isn't ready yet.
    """
    if os.path.exists(CHANGEPOINTS_FILE):
        try:
            return pd.read_json(CHANGEPOINTS_FILE)
        except ValueError as e:
            print(f"Warning: '{CHANGEPOINTS_FILE}' could not be parsed ({e}). Using placeholder.")

    return pd.DataFrame([
        {
            "change_point_date": "2020-03-08",
            "mean_before": 60.2,
            "mean_after": 33.4,
            "percent_change": -44.5,
            "likely_event": "Saudi-Russia Price War / COVID-19 Demand Collapse"
        }
    ])