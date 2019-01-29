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

"""
MySQLdb reference: https://mysqlclient.readthedocs.io/index.html
MySQL language: https://dev.mysql.com/doc/refman/8.0/en/
"""

version="1.4"

if "BEAN_DB" in environ:
    db_host = environ["BEAN_DB"]
else:
    db_host="db"
db_user = "beaner"
db_passwd = "password"
db_name = "DockBeanBiz"

api = Blueprint('api', __name__, url_prefix='/api')

def connect_db():
    return MySQLdb.connect(
        user=db_user,
        passwd=db_passwd,
        db=db_name,
        host=db_host,
        port=3306,
        cursorclass=DictCursor)

########
#
# API
#
########

@api.route('/debug', methods=['GET'])
def debug():
    return "Hello World"

@api.route('/menus', methods=['GET'])
def menus():
    QUERY = """
    SELECT menu_item_id, item_name
        FROM menu
    """
    db = connect_db()
    cur = db.cursor()
    cur.execute(QUERY)
    res = dumps(cur.fetchall())
    return res

@api.route('/orders', methods=['GET'])
def orders():
    QUERY = """
    SELECT menu.item_name, orders.quantity, orders.placement_time
        FROM orders
    JOIN menu ON orders.menu_item_id = menu.menu_item_id
    """
    db = connect_db()
    cur = db.cursor()
    # TODO: Right now we are returning all the data in the database, which
    # could be very much indeed. Need to include support for pagination
    cur.execute(QUERY)
    # GOTCHA: Our database contains datetime objects, which the default json
    # serializer has no functionality to handle. Thus we specify the 
    # default=str in the dumps call, which tells the serializer to simply use\
    # the built-in str() convert on any types that it otherwise doesn't know
    # how to handle.
    res = dumps(cur.fetchall(), default=str)
    return res
