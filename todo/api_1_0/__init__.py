from flask import Blueprint
from flask import jsonify

api = Blueprint('api', __name__)

from todo.api_1_0 import todo
from todo.api_1_0 import auth
# from todo.api_1_0 import views
from todo import jwt


@api.after_request
def after_reqeust(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-APP-Token'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@jwt.expired_token_loader
def expired_token_loader():
    return jsonify(dict(
        message='The token has expired'
    )), 401


@api.errorhandler(401)
def AuthError(code):
    return jsonify(dict(
        message='Request Invalid authorization credentials'
    )), 401
