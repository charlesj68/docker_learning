from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for)
from requests import get
import menus, meals


def create_app():
    app = Flask("corp")

    # As of yet, no routes in our main app. All
    # work is being performed in Blueprints

    app.register_blueprint(menus.api)
    app.register_blueprint(meals.api)

    return app
