import datetime

from todo import db

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from flask_script import Command, Option

from settings import Config


class BaseModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    info = db.relationship('UserInfo', backref='owner')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # todos = db.relationship('Todo', backref='owner')

    def __repr__(self):
        return '<User: %r>' % self.username

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method=current_app.config['PASSWORD_HASH_ALGORITHM'],
            salt_length=current_app.config['PASSWORD_HASH_LENGTH'],

        )

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.ForeignKey('users.id'))
    sex = db.Column(db.Boolean, nullable=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    phone_number = db.Column(db.String(11), nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    birthday = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<UserInfo: %d, %r>' % (self.id, self.owner)


class Todo(db.Model, BaseModel):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    publish_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_done = db.Column(db.Boolean, default=False)
    is_important = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Todo: %r>' % self.name

    def __str__(self):
        return self.name


class CreateAdmin(Command):
    """Create a super admin user"""

    def __init__(self, default_email=Config.ADMIN_EMAIL_ADDRESS, default_username='admin', default_password='password'):
        super(CreateAdmin, self).__init__()
        self.default_email = default_email
        self.default_username = default_username
        self.default_password = default_password

    def get_options(self):
        return [
            Option('-e', '--email', dest='email', default=self.default_email),
            Option('-u', '--username', dest='username', default=self.default_username),
            Option('-p', '--password', dest='password', default=self.default_password)
        ]

    def run(self, email, username, password):
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User()
            user.email = email
            user.username = username
        user.set_password(password)
        user.save()
        print(
            'Admin user (%s) and password (%s)'
            ' has created.' %
            (
                username,
                '-' * len(password)
            )
        )
