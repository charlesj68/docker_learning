from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for)
from requests import get

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def main_page():
        return render_template('main_page.html')

    @app.route('/show_menu', methods=['GET'])
    def show_menu():
        items = get(url_for('api.menus', _external=True)).json()
        return render_template('menus.html', items=items)

    @app.route('/show_orders', methods=['GET'])
    def show_orders():
        items = get(url_for('api.orders', _external=True)).json()
        return render_template('orders.html', items=items)

    from . import api
    app.register_blueprint(api.api)

    return app
