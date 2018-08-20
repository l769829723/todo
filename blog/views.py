from flask import render_template
from blog import blog
from blog.models import Post
from blog.models import Channel


@blog.route('/')
def home():
    channels = Channel.query.all()
    posts = Post.query.all()
    return render_template('index.html', channels=channels, posts=posts)


@blog.route('/<string:name>')
def channel(name):
    channels = Channel.query.all()
    posts = Post.query.filter_by(channel=name).all()
    return render_template('index.html', channels=channels, posts=posts)


@blog.route('/p/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('detail.html', post=post)
