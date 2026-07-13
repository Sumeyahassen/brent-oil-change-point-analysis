from flask import Blueprint, jsonify # type: ignore
from services.data_loader import load_events

events_bp = Blueprint("events", __name__)


@events_bp.route("/api/events", methods=["GET"])
def get_events():
    """Returns the list of researched key events affecting oil prices."""
    df = load_events()
    result = df.copy()
    result["event_date"] = result["event_date"].dt.strftime("%Y-%m-%d")
    return jsonify(result.to_dict(orient="records"))