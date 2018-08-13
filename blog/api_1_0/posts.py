from flask import jsonify
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal
from flask_restful import reqparse
from blog.api_1_0 import blog_api

from blog.models import Channel
from blog.models import Post


class Channels(Resource):
    channel_fields = dict(
        id=fields.Integer,
        name=fields.String
    )

    channel_parser = reqparse.RequestParser()

    def get(self):
        channels = Channel.query.all()
        return jsonify(marshal(channels, self.channel_fields))


blog_api.add_url_rule('/channels/', view_func=Channels.as_view('channels'))


class Posts(Resource):
    post_fields = dict(
        id=fields.Integer,
        name=fields.String,
        channel=fields.String,
        content=fields.String,
        publishTime=fields.DateTime,
        updateTime=fields.DateTime
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

    def get(self):
        posts = Post.query.all()
        return jsonify(marshal(posts, self.post_fields))

    def post(self):
        # return jsonify(message='Hi')
        post_args = self.post_parser.parse_args()
        channel_name = post_args.get('channel')
        channel = Channel.query.filter_by(name=channel_name)
        if not channel:
            channel = Channel()
            channel.name = channel_name
            channel.save()
        post = Post()
        post.name = post_args.get('name')
        post.channel = channel
        post.content = post_args.get('content')
        post.save()
        return jsonify(marshal(post, self.post_fields)), 201


blog_api.add_url_rule('/posts/', view_func=Posts.as_view('posts'))
