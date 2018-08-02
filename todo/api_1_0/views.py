from flask import jsonify
from flask_restful import Resource, marshal, fields, reqparse
from todo.api_1_0 import api


class Name:
    name = ''


class APIRoot(Resource):

    my_parser = reqparse.RequestParser()

    my_fields = dict(
        name=fields.String
    )

    def get(self):
        resp = jsonify(marshal(Name, self.my_fields))
        return resp

    def post(self):
        args = self.my_parser.parse_args()
        name = args.get('name', default='')
        Name.name = name
        return jsonify(Name)


api.add_url_rule('/', view_func=APIRoot.as_view('APIRoot'))