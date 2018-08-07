#!/usr/bin/env bash

ROOT='/var/www/todoapp/'

mv ${ROOT}/app /tmp
git clone https://github.com/l769829723/todo.git ${ROOT}/app

source ${ROOT}/venv/bin/activate
cd ${ROOT}/app/
python manage.py db upgrade
python manage.py db migrate
