from flask import render_template
from blog import blog


@blog.route('/')
def home():
    return render_template('index.html')
