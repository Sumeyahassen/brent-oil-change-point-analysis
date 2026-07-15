from flask import Blueprint, jsonify # type: ignore
from services.analytics import get_performance_metrics

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/api/stats", methods=["GET"])
def stats():
    """Returns overall dataset performance metrics for dashboard summary cards."""
    data = get_performance_metrics()
    return jsonify(data)