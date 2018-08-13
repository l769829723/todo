import os
from flask_script import Manager, Shell
from flask_migrate import (
    Migrate,
    MigrateCommand
)

from todo import db
from todo import create_app

from todo.models import User
from todo.models import Todo
from todo.models import CreateAdmin

from blog.models import Channel
from blog.models import Post

# Config APP
config = os.environ.get('PROJECT_ENV', default='PRO')
app = create_app(config)

# Migration DB
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Todo=Todo,
        Channel=Channel,
        Post=Post
    )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('createadmin', CreateAdmin())


@manager.command
def test():
    """ Running test suite case """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
