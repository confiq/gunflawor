FROM ubuntu:xenial

RUN apt-get update && apt-get install -y python2 python-pip

RUN pip install gunicorn

COPY app /app

EXPOSE 9080