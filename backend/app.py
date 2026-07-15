"""
app.py
Main entry point for the Brent Oil Change Point Analysis backend API.


"""

from flask import Flask, jsonify # type: ignore
from flask_cors import CORS # type: ignore

from routes.prices import prices_bp
from routes.events import events_bp
from routes.changepoints import changepoints_bp
from routes.correlation import correlation_bp
from routes.stats import stats_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(prices_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(changepoints_bp)
    app.register_blueprint(correlation_bp)
    app.register_blueprint(stats_bp)

    @app.route("/")
    def index():
        return jsonify({
            "message": "Brent Oil Change Point Analysis API",
            "endpoints": [
                "/api/prices",
                "/api/events",
                "/api/changepoints",
                "/api/events/correlation",
                "/api/stats"
            ]
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)