# To start... gunicorn -w XXX server1.gunicorn_syncworker:app
from time import sleep

SLEEP_TIME = 0.5

def app(environ, start_response):
    data = b"Simple Data!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    sleep(SLEEP_TIME)
    return iter([data])



