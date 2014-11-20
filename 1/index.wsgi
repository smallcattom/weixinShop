import sae

def app(environ, start_response):
    status = '300 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello, catTom']

application = sae.create_wsgi_app(app)