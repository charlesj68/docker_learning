"""Register Flask app."""
from flask import Flask
import menus


def create_app():
    """Create and return the Flask app."""
    app = Flask("corp")
    app.register_blueprint(menus.api)
    return app
