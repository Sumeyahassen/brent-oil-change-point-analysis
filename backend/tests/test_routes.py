"""
test_data_loader.py
Unit tests for the data loading and error-handling logic.
"""

import sys
import os
import pandas as pd
import pytest # type: ignore

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from services.data_loader import load_prices, load_events, load_changepoints


def test_load_prices_returns_dataframe():
    df = load_prices()
    assert isinstance(df, pd.DataFrame)
    assert "Date" in df.columns
    assert "Price" in df.columns


def test_load_prices_dates_are_datetime():
    df = load_prices()
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_load_prices_sorted_chronologically():
    df = load_prices()
    assert df["Date"].is_monotonic_increasing


def test_load_prices_no_null_dates():
    df = load_prices()
    assert df["Date"].isnull().sum() == 0


def test_load_events_returns_dataframe():
    df = load_events()
    assert isinstance(df, pd.DataFrame)


def test_load_events_minimum_count():
    df = load_events()
    assert len(df) >= 10, "Brief requires at least 10-15 events"


def test_load_events_required_columns():
    df = load_events()
    for col in ["event_date", "event_name", "description", "category"]:
        assert col in df.columns


def test_load_changepoints_returns_dataframe():
    df = load_changepoints()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0