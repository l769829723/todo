from todo import create_app
from waitress import serve


wsgiapp = create_app('PRO')

serve(wsgiapp, listen='127.0.0.1:5000', url_scheme='https')
