from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal
from flask_restful import abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, fresh_jwt_required

from todo.api_1_0 import api
from todo.models import User


class Login(Resource):
    def post(self):
        token_fields = dict(
            token=fields.String
        )
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username',
            type=str,
            location='json',
            required=True,
            help='Specified your user name.'
        )
        parser.add_argument(
            'password',
            type=str,
            location='json',
            required=True,
            help='Specified your user password.'
        )
        args = parser.parse_args()
        user = User.query.filter_by(email=args.get('username')).first()
        if user and user.verify_password(args.get('password')):
            return jsonify(marshal(
                dict(token=create_access_token(user.id)),
                token_fields
            ))
        abort(401)


api.add_url_rule('/login/', view_func=Login.as_view('login'))


class Verify(Resource):
    method_decorators = [jwt_required]

    def get(self):
        return jsonify({'token': 'invalid'}), 200


api.add_url_rule('/login/verify/', view_func=Verify.as_view('verify'))


class UserInfo(Resource):
    method_decorators = [jwt_required]

    user_field = dict(
        username=fields.String,
        email=fields.String
    )

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        location='json',
        required=True,
        help='Specified your user name.'
    )
    parser.add_argument(
        'old_password',
        type=str,
        location='json',
        required=True,
        help='Specified your old password.'
    )
    parser.add_argument(
        'new_password',
        type=str,
        location='json',
        required=True,
        help='Specified your new password.'
    )

    def get(self):
        current_user = self.get_object()
        return jsonify(dict(
            username=current_user.username,
            email=current_user.email
        )), 200

    def post(self):
        args = self.parser.parse_args()
        old_password = args.get('old_password')
        current_user = self.get_object()
        verify_result = current_user.verify_password(old_password)
        if verify_result:
            username = args.get('username')
            password = args.get('new_password')
            current_user.username = username
            current_user.set_password(password)
            current_user.save()
            return jsonify({'message': 'Your profile has updated.'})
        return jsonify(
            {'message': 'Identity invalid, please check your profile.'}
        ), 401

    def get_object(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        return user


api.add_url_rule('/login/me/', view_func=UserInfo.as_view('user_info'))
