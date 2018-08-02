import pymysql

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from settings import ENV

pymysql.install_as_MySQLdb()

api = Api()
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(
        ENV.get(
            config.strip().replace('\'', '').replace('"', '')
        )
    )
    db.init_app(app)
    jwt.init_app(app)

    from todo import api_1_0
    api.init_app(api_1_0.api)
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1')

    return app
