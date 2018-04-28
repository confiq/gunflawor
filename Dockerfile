FROM ubuntu:xenial

RUN apt-get update && apt-get install -y python python-pip ipython python3

RUN pip install gunicorn gevent
ARG NoCache
COPY app /app

EXPOSE 9080