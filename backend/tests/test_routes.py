"""
test_routes.py
Unit tests for the Brent Oil Change Point Analysis backend API.

Run with:
    pytest tests/ --verbose
"""

import sys
import os
import pytest # type: ignore

# Ensure the backend package is importable when running pytest from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


@pytest.fixture
def client():
    """Creates a Flask test client for making requests without running a real server."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- Root endpoint ---

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "endpoints" in data


# --- /api/prices ---

def test_get_prices_returns_200(client):
    response = client.get("/api/prices")
    assert response.status_code == 200


def test_get_prices_returns_list(client):
    response = client.get("/api/prices")
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_prices_record_structure(client):
    response = client.get("/api/prices")
    data = response.get_json()
    first_record = data[0]
    assert "Date" in first_record
    assert "Price" in first_record


def test_get_prices_with_date_filter(client):
    response = client.get("/api/prices?start_date=2020-01-01&end_date=2020-12-31")
    assert response.status_code == 200
    data = response.get_json()
    for record in data:
        assert "2020" in record["Date"]


# --- /api/events ---

def test_get_events_returns_200(client):
    response = client.get("/api/events")
    assert response.status_code == 200


def test_get_events_minimum_count(client):
    response = client.get("/api/events")
    data = response.get_json()
    assert len(data) >= 10  # brief requires at least 10-15 events


def test_get_events_record_structure(client):
    response = client.get("/api/events")
    data = response.get_json()
    first_record = data[0]
    assert "event_date" in first_record
    assert "event_name" in first_record
    assert "description" in first_record
    assert "category" in first_record


# --- /api/changepoints ---

def test_get_changepoints_returns_200(client):
    response = client.get("/api/changepoints")
    assert response.status_code == 200


def test_get_changepoints_returns_list(client):
    response = client.get("/api/changepoints")
    data = response.get_json()
    assert isinstance(data, list)


# --- 404 handling ---

def test_unknown_route_returns_404(client):
    response = client.get("/api/does-not-exist")
    assert response.status_code == 404