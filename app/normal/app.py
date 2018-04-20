# To start... gunicorn -w XXX server1.gunicorn_syncworker:app

def app(environ, start_response):
    data = b"Simple Data!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])



