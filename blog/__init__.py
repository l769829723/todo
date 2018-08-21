from flask import Blueprint
from flask import render_template

blog = Blueprint('blog', __name__, template_folder='templates', static_folder='static')

from blog import views


@blog.app_errorhandler(404)
def resource_not_found(error):
    return render_template('404.html')


@blog.app_errorhandler(500)
def resource_not_found(error):
    return render_template('500.html')
