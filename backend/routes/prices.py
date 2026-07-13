from flask import Blueprint, request, jsonify # type: ignore
from services.data_loader import load_prices

prices_bp = Blueprint("prices", __name__)


@prices_bp.route("/api/prices", methods=["GET"])
def get_prices():
    """
    Returns historical Brent oil prices.
    Optional query params: start_date, end_date (format: YYYY-MM-DD)
    Example: /api/prices?start_date=2020-01-01&end_date=2020-12-31
    """
    df = load_prices()

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date:
        df = df[df["Date"] >= start_date]
    if end_date:
        df = df[df["Date"] <= end_date]

    result = df.copy()
    result["Date"] = result["Date"].dt.strftime("%Y-%m-%d")

    return jsonify(result.to_dict(orient="records"))