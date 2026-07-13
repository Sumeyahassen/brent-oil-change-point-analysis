"""
app.py
Main entry point for the Brent Oil Change Point Analysis backend API.

Run with:
    python app.py
"""

from flask import Flask, jsonify # type: ignore
from flask_cors import CORS

from routes.prices import prices_bp # type: ignore
from routes.events import events_bp # type: ignore
from routes.changepoints import changepoints_bp # type: ignore


def create_app():
    app = Flask(__name__)
    CORS(app)  # allow requests from the React frontend during development

    # Register route blueprints
    app.register_blueprint(prices_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(changepoints_bp)

    @app.route("/")
    def index():
        return jsonify({
            "message": "Brent Oil Change Point Analysis API",
            "endpoints": [
                "/api/prices",
                "/api/events",
                "/api/changepoints"
            ]
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)