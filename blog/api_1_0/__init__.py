from flask import Blueprint

blog_api = Blueprint('blog_api', __name__)

from blog.api_1_0 import posts
