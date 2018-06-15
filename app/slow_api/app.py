# coding=utf-8
# so this should look something like this: $ gunicorn --workers=2 app.cpu.app:app ¯\_(ツ)_/¯

def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])