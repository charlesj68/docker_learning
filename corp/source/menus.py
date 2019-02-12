"""Define blueprint for menus endpoints."""
from flask import Blueprint, jsonify
from db import connect_db

# SQL Statements

SQL_GET_MENUS = """
    SELECT item_name
        FROM menu"""

api = Blueprint('menus', __name__, url_prefix='/menus')


@api.route('/', methods=['GET'])
def menus():
    """Return a list of all active menu item names."""
    cursor = connect_db().cursor()
    cursor.execute(SQL_GET_MENUS)
    return jsonify(cursor.fetchall())
