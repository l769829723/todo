# PROJECT_NAME
# PROJECT_ENV
# PROJECT_ADMIN
# PROJECT_SETTING
# PROJECT_ADMIN_USER
# PROJECT_ADMIN_PASS
import os
import datetime

__all__ = ['ENV']


class Config(object):
    ROOT = os.path.abspath(__file__)
    NAME = ''
    DEBUG = False
    TESTING = False

    STATIC_FOLDER = os.path.dirname(ROOT) + '/static'

    # Database settings
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(ROOT) + '/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '|w\xfd\xbc01\xec\x7f\r.\xe8\x13\x07?\x06V'

    # APP Exception send mail to admin
    EXCEPTION_EMAIL = False

    # Password hash
    PASSWORD_HASH_LENGTH = 8
    PASSWORD_HASH_ALGORITHM = 'pbkdf2:sha256'

    # Datetime format string
    DATETIME_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'

    # Pagination
    COUNTS_OF_PER_PAGE = 16

    # JSON web token
    JWT_HEADER_NAME = 'X-APP-TOKEN'
    JWT_HEADER_TYPE = 'Token'
    ACCESS_TOKEN_DURATION_SECONDS = 300
    JWT_SECRET_KEY = '2K#\xe0\xc4\xe7H\xbf\x87\x11\xe2w)6\xbf\xc3'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(
        seconds=ACCESS_TOKEN_DURATION_SECONDS
    )

    # E-mail
    ADMIN_EMAIL_ADDRESS = '1054473703@qq.com'

    # Upload
    UPLOAD_FOLDER = os.path.join(ROOT, 'store')

    # The extends name of upload file list
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    ALLOWED_TYPES_OF_UPLOAD = [
        'head_picture'
    ]
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class ProductionConfig(Config):
    # EXCEPTION_EMAIL = True
    # CORS
    CORS = '*'
    SQLALCHEMY_DATABASE_URI = 'mysql://todoadmin:password@localhost/todo'


class DevelopmentConfig(Config):
    DEBUG = True
    # CORS
    CORS = 'http://localhost:8080'
    ACCESS_TOKEN_DURATION_SECONDS = 10


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(Config.ROOT) + '/db-test.sqlite3'


ENV = {
    'PRO': ProductionConfig,
    'DEV': DevelopmentConfig,
    'TES': TestingConfig
}
