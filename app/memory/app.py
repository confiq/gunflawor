# coding=utf-8
# so this should look something like this: $ gunicorn --workers=2 app.memory.app:app ¯\_(ツ)_/¯

MEMORY_SIZE = 1000000

def app(environ, start_response):
    """Simplest possible application object"""
    data = 'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    foo = "A" * MEMORY_SIZE
    del foo
    return iter([data])