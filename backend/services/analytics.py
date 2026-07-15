"""
analytics.py
Computes derived analytics used by the dashboard: volatility and price
change correlated with each event, plus overall performance metrics.
"""

import numpy as np
import pandas as pd
from services.data_loader import load_prices, load_events


def compute_log_returns(prices):
    prices = prices.copy()
    prices["log_return"] = np.log(prices["Price"]) - np.log(prices["Price"].shift(1))
    prices["rolling_vol"] = prices["log_return"].rolling(window=30).std()
    return prices.dropna(subset=["log_return"])


def get_event_correlation(window=30):
    """
    For each researched event, computes:
      - average price before/after the event
      - percent price change
      - average 30-day rolling volatility following the event
    """
    prices = compute_log_returns(load_prices())
    events = load_events()

    results = []
    for _, event in events.iterrows():
        event_date = event["event_date"]

        before_mask = (prices["Date"] < event_date) & (prices["Date"] >= event_date - pd.Timedelta(days=window))
        after_mask = (prices["Date"] >= event_date) & (prices["Date"] <= event_date + pd.Timedelta(days=window))

        price_before = prices.loc[before_mask, "Price"].mean() # type: ignore
        price_after = prices.loc[after_mask, "Price"].mean() # type: ignore
        avg_volatility_after = prices.loc[after_mask, "rolling_vol"].mean() # type: ignore

        pct_change = None
        if pd.notna(price_before) and pd.notna(price_after) and price_before != 0:
            pct_change = round((price_after - price_before) / price_before * 100, 2)

        results.append({
            "event_name": event["event_name"],
            "event_date": str(event_date.date()),
            "category": event["category"],
            "avg_price_before": round(float(price_before), 2) if pd.notna(price_before) else None,
            "avg_price_after": round(float(price_after), 2) if pd.notna(price_after) else None,
            "percent_change": pct_change,
            "avg_volatility_after": round(float(avg_volatility_after), 4) if pd.notna(avg_volatility_after) else None,
        })

    return results


def get_performance_metrics():
    """
    Overall dataset-wide performance metrics for dashboard summary cards.
    """
    prices = compute_log_returns(load_prices())

    return {
        "date_range_start": str(prices["Date"].min().date()),
        "date_range_end": str(prices["Date"].max().date()),
        "total_days": int(len(prices)),
        "avg_price": round(float(prices["Price"].mean()), 2),
        "min_price": round(float(prices["Price"].min()), 2),
        "max_price": round(float(prices["Price"].max()), 2),
        "avg_daily_volatility": round(float(prices["log_return"].std()), 5),
        "avg_30day_rolling_volatility": round(float(prices["rolling_vol"].mean()), 5),
        "highest_volatility_period": {
            "date": str(prices.loc[prices["rolling_vol"].idxmax(), "Date"].date()), # type: ignore
            "volatility": round(float(prices["rolling_vol"].max()), 4)
        }
    }