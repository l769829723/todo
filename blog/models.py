from datetime import datetime
from sqlalchemy.orm import relationship
from todo import db
from todo.models import BaseModel


class Channel(db.Model, BaseModel):
    __tablename__ = 'blog_channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    # posts = db.relationship('Post', backref='channel', lazy='dynamic')


class Tag(db.Model, BaseModel):
    __tablename__ = 'blog_tags'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    name = db.Column(db.String(128), unique=True)
    posts = relationship("Post", back_populates="tags")

    def __repr__(self):
        return self.name


class Post(db.Model, BaseModel):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.ForeignKey(Channel.name))
    name = db.Column(db.String(128), unique=True, index=True)
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    tags = relationship("Tag", back_populates="posts")
    is_published = db.Column(db.Boolean, default=False)
#
# Data statistics
# class DataStatistic(BaseModel):
#     __tablename__ = 'data_statistics'
#     id = db.Column(db.Integer, primary_key=True)
