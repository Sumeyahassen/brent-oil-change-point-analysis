from flask import Blueprint, jsonify # type: ignore
from services.data_loader import load_changepoints

changepoints_bp = Blueprint("changepoints", __name__)


@changepoints_bp.route("/api/changepoints", methods=["GET"])
def get_changepoints():
    """Returns detected change points from the Task 2 PyMC model."""
    df = load_changepoints()
    return jsonify(df.to_dict(orient="records"))