FROM ubuntu:xenial

RUN apt-get update && apt-get install -y python3-pip ipython

RUN pip3 install gunicorn gevent eventlet futures aiohttp==1.3.5
COPY app /app

EXPOSE 9081