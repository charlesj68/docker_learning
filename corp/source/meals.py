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

api = Blueprint('meals', __name__, url_prefix='/meals')


@api.route('/', methods=['GET'])
def meals():
    return "Hello World"
