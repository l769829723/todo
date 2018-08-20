from flask import Blueprint
from flask import jsonify
from flask import current_app

api = Blueprint('api', __name__)

from todo.api_1_0 import todo
from todo.api_1_0 import auth
from todo.api_1_0 import posts
from todo import jwt


@api.after_request
def after_reqeust(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-APP-Token'
    response.headers['Access-Control-Allow-Origin'] = current_app.config['CORS']
    return response


@jwt.expired_token_loader
def expired_token_loader():
    return jsonify(dict(
        message='The token has expired'
    )), 401


@jwt.unauthorized_loader
def unauthorized_loader(error):
    return jsonify(dict(
        message='Request Invalid authorization credentials'
    )), 401


@api.errorhandler(401)
def auth_error(error):
    return jsonify(dict(
        message='Request Invalid authorization credentials'
    )), 401


@api.app_errorhandler(404)
def resource_not_found(error):
    return jsonify(dict(
        message='Sorry, you required resources not found.'
    )), 404
