from flask import request
from flask import current_app
from flask import render_template
from blog import blog
from blog.models import Post
from blog.models import Channel


@blog.route('/')
def home():
    channels = Channel.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.update_time.desc()).filter_by(is_published=True).paginate(
        page, per_page=current_app.config['COUNTS_OF_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', channels=channels, posts=posts, pagination=pagination)


@blog.route('/<string:name>')
def channel(name):
    channels = Channel.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(channel=name).filter_by(is_published=True).order_by(Post.update_time.desc()).paginate(
        page, per_page=current_app.config['COUNTS_OF_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('channel.html', channels=channels, posts=posts, pagination=pagination, name=name)


@blog.route('/p/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail.html', post=post)
