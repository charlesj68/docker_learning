from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for)


api = Blueprint('kitchen', __name__, url_prefix='/kitchen')


@api.route('/', methods=['GET'])
def kitchen():
    return "Kitchen root"

