import datetime

from todo import db
from todo.models import BaseModel


class Channel(db.Model, BaseModel):
    __tablename__ = 'blog_channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    # posts = db.relationship('Post', backref='channel', lazy='dynamic')


class Post(db.Model, BaseModel):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.ForeignKey(Channel.name))
    name = db.Column(db.String(128), unique=True, index=True)
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=None, nullable=True)
#
# Data statistics
# class DataStatistic(BaseModel):
#     __tablename__ = 'data_statistics'
#     id = db.Column(db.Integer, primary_key=True)
