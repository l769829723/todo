import os
from flask_script import Manager, Shell
from flask_migrate import (
    Migrate,
    MigrateCommand
)

from todo import db
from todo import create_app
from settings import ENV

from todo.models import User
from todo.models import Todo
from todo.models import CreateAdmin

# Config APP
config = os.environ.get('PROJECT_ENV') or 'PRO'
# config = 'DEV'
app = create_app(ENV.get(config.strip().replace('\'', '').replace('"', '')))

# Migration DB
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User, Todo=Todo)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('createadmin', CreateAdmin())


if __name__ == '__main__':
    manager.run()
