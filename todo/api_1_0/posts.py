from datetime import datetime
from flask import jsonify
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from todo import db
from todo.api_1_0 import api

from blog.models import Channel
from blog.models import Post


class Channels(Resource):
    decorators = [jwt_required]

    channel_fields = fields.String

    channel_parser = reqparse.RequestParser()
    channel_parser.add_argument(
        'name',
        type=str,
        location='json',
        required=True,
        help='Please, specified a channel name.'
    )

    def get(self):
        channels = [c.name for c in Channel.query.all()]
        channels_and_posts = []
        for channel in channels:
            channel_with_posts = dict(
                name=channel,
                posts=Post.query.filter_by(channel=channel).count()
            )
            channels_and_posts.append(channel_with_posts)
        return jsonify(channels_and_posts)

    # def post(self):
    #     channel_args = self.channel_parser.parse_args()
    #     try:
    #         channel = Channel()
    #         channel.name = channel_args.get('name')
    #         channel.save()
    #     except IntegrityError:
    #         db.session.rollback()
    #         return jsonify(message='Channel {} already exists.'.format(channel_args.get('name')))
    #     return jsonify(marshal(channel, self.channel_fields)), 201


api.add_url_rule('/channels/', view_func=Channels.as_view('channels'))


class Posts(Resource):
    method_decorators = [jwt_required]

    post_fields = dict(
        id=fields.Integer,
        name=fields.String,
        channel=fields.String,
        content=fields.String,
        publish_time=fields.DateTime,
        update_time=fields.DateTime
    )

    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name',
        type=str,
        location='json',
        required=True,
        help='Please, specified a post name.'
    )
    post_parser.add_argument(
        'channel',
        type=str,
        location='json',
        required=True,
        help='Please, specified a post channel.'
    )
    post_parser.add_argument(
        'content',
        type=str,
        location='json',
        required=True,
        help='Please, specified a post content.'
    )

    def get(self, *args):
        posts = Post.query.all()
        return jsonify(marshal(posts, self.post_fields))

    def post(self):
        post_args = self.post_parser.parse_args()
        channel_name = post_args.get('channel')
        channel = Channel.query.filter_by(name=channel_name).first()
        now = datetime.utcnow()
        if not channel:
            return jsonify(message='Please choose a channel for publishing.'), 404
        try:
            post = Post()
            post.name = post_args.get('name')
            post.channel = channel.name
            post.content = post_args.get('content')
            post.publish_time = now
            post.save()
        except IntegrityError:
            db.session.rollback()
            return jsonify(message='Post {} already exists.'.format(post_args.get('name'))), 409
        return jsonify(marshal(post, self.post_fields)), 201


class PostDetail(Posts):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return jsonify(marshal(post, self.post_fields))

    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify(message='Post not found.'), 404
        post.delete()
        return jsonify(message='Post deleted success.')


api.add_url_rule('/posts/', view_func=Posts.as_view('posts'))
api.add_url_rule('/posts/<int:post_id>/', view_func=PostDetail.as_view('posts_detail'))
