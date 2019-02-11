from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for)

api = Blueprint('register', __name__, url_prefix='/register')


@api.route('/', methods=['GET'])
def register():
    return "Register root"
