from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for)
from requests import get
import orders, register, kitchen


def create_app():
    app = Flask("locations")

    # As of yet, no routes in our main app. All
    # work is being performed in Blueprints

    app.register_blueprint(orders.api)
    app.register_blueprint(register.api)
    app.register_blueprint(kitchen.api)

    return app
