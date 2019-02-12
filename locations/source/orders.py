"""Support the Order API."""
from bson.objectid import ObjectId
from datetime import datetime
from db import get_order_db
from flask import (
    Blueprint,
    jsonify,
    make_response,
    request)
from json import dumps
from pymongo import MongoClient

# Constants

DB_NAME = 'mongodb'
DB_USER = 'root'
DB_PASSWD = 'example'

# Endpoints returning lists
# /orders/open GET - Return IDs of all active orders
# /orders/pending GET - Return IDs of all orders ready for prep
# /orders/plated GET - Return IDs of all orders ready for serving
# /orders/monitor GET - Return IDs of all orders served and awaiting checkout

# Endpoints returning full order details
# /orders/<id> GET - Return details of a specific order

# Endpoints for data creation or update
# /orders POST - Create a new order
# /orders/<id>/state/<state> PUT - Transition an order to a new state


# Minimum data format for orders
# {
#   "createTime": Time of order creation,
#   "startTime": Time of entry into kitchen,
#   "serveTime": Time of exit from kitchen,
#   "checkoutTime": Time of payment made,
#   "status": One of "new", "preparing", "served", "closed",
#   "items": [
#       {
#           "name": Menu item name,
#           "quantity": Number ordered
#       }
#   ]
# }

def get_order_db():
    client = MongoClient(
        DB_NAME,
        username=DB_USER,
        password=DB_PASSWD)
    return client.order_db


def find_all_order_ids_by(test):
    """Return list of order _id's based on specified test."""
    order_set = get_order_db().all_orders
    cursor = order_set.find(test)
    return [str(item['_id']) for item in cursor]


def find_one_order_detail_by(test):
    """Return full order detail based on specified test."""
    order_set = get_order_db().all_orders
    item = order_set.find_one(test)
    return [item]


@api.route('/', methods=['POST'])
def orders_detail_post():
    """Create new order in database."""
    jsonData = request.get_json()
    orderdoc = {
        "createTime": datetime.now(),
        "status": "new",
        "items": jsonData}
    order_collection = get_order_db().all_orders
    order_id = order_collection.insert_one(orderdoc).inserted_id
    return make_response(jsonify(id=str(order_id)), 201)


@api.route('/<id>', methods=['GET'])
def orders_detail_get(id):
    """Get detailed order info for given _id."""
    return dumps(
        find_one_order_detail_by({"_id": ObjectId(id)}),
        default=str)


@api.route('/<id>/status/<status>', methods=['PUT'])
def orders_move_status_put(id, new_status):
    """Change the status of an order, and register when it happens."""
    order_set = get_order_db().all_orders
    order_doc = find_one_order_detail_by({"_id": ObjectId(id)})[0]
    # TODO Enhancement, ensure that the requested status makes sense given
    # the current status. For now, just check that the requested status is
    # _different_ than the current status.
    if order_doc["status"] == new_status:
        return make_response(None, 204)
    if new_status == "preparing":
        order_doc["status"] = "preparing"
        order_doc["startTime"] = datetime.now()
    elif new_status == "served":
        order_doc["status"] = "served"
        order_doc["serveTime"] = datetime.now()
    elif new_status == "closed":
        order_doc["status"] = "closed"
        order_doc["checkoutTime"] = datetime.now()
    res = order_set.update_one({"_id": ObjectId(id)}, order_doc)
    if res.matched_count != 1:
        # TODO Failed to update the document, barf!
        pass
    return make_response(None, 204)


@api.route('/open', methods=['GET'])
def orders_open():
    """Get list of orders not yet closed."""
    return dumps(find_all_order_ids_by({"status": {"$ne": "closed"}}))


@api.route('/pending', methods=['GET'])
def orders_pending():
    """Get list of orders not yet preparing."""
    return dumps(find_all_order_ids_by({"status": {"$eq": "new"}}))


@api.route('/plated', methods=['GET'])
def orders_plated():
    """Get list of orders not yet served."""
    return dumps(find_all_order_ids_by({"status": {"$eq": "preparing"}}))


@api.route('/monitor', methods=['GET'])
def orders_monitor():
    """Get list of orders not yet paid."""
    return dumps(find_all_order_ids_by({"status": {"$eq": "served"}}))

api = Blueprint('orders', __name__, url_prefix='/orders')
