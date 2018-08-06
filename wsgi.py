from todo import create_app
from waitress import serve


app = create_app('PRO')

serve(app.wsgi_app, listen='127.0.0.1:5000', url_scheme='https')
