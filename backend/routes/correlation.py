from flask import Blueprint, request, jsonify # type: ignore
from services.analytics import get_event_correlation

correlation_bp = Blueprint("correlation", __name__)


@correlation_bp.route("/api/events/correlation", methods=["GET"])
def event_correlation():
    """
    Returns, for each event: price before/after, percent change, and
    average volatility following the event. Supports an optional
    ?window=N query param (default 30 days).
    """
    window = request.args.get("window", default=30, type=int)
    data = get_event_correlation(window=window)
    return jsonify(data)