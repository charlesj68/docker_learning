"""Create the Flask app for the locations service."""
from flask import Flask
import orders


def create_app():
    """Create and return app instance."""
    app = Flask("locations")
    app.register_blueprint(orders.api)
    return app
