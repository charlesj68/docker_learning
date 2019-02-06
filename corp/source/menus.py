from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for)
from requests import get
from json import dumps
import MySQLdb
from MySQLdb.cursors import DictCursor
from os import environ
from db import connect_db

# SQL Statements
GET_MENUS = """
    SELECT item_name
        FROM menu"""

api = Blueprint('menus', __name__, url_prefix='/menus')


@api.route('/', methods=['GET'])
def menus():
    QUERY = GET_MENUS
    dbhandle = connect_db()
    cur = dbhandle.cursor()
    cur.execute(QUERY)
    res = dumps(cur.fetchall())
    return res
