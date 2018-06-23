# gunflawor

## WORK IN PROGRESS
Please notice that this is still work in process, so all this text is about what/how this software SHOULD look

# What is it?

Stats for Gunicorn and flask with workers types

Gunicorn has few workers types that you can use for your app.

It's been argued what type of the worker is best for your environment so we are trying to make some answer to the following questions:


Questions:
1) What type of worker I should use for my app? 
1) It's not crucial what worker type you have when you have big CPU/Mem load 
cause the utilisation of resourses will be same when sync/async
  
1) Async worker might help when you have slow external load but not that much
1) will gevent.wsgi perform better then gunicorn.workers.ggevent on flask?



# How to measure it?

Lets first check what type of workers we have and what types of load we have

Workers:
1) gunicorn sync worker
1) gunicorn async worker - gevent
1) eventlet
1) gevent.wsgi - NOT YET IMPLEMENTED

Types of load:

1) CPU
2) Memory
3) sleep(2)
4) slow external web page (slow API)


There should be metrics of checks like this

| Type of load  | sync  | eventlet | gevent |
| ------------- | ----- | -------- | ------ |
| CPU           | 🔢  | 🔢 | 🔢  | 🔢 |
| Memory        | 🔢  | 🔢 | 🔢  | 🔢 |
| sleep(2)      | 🔢  | 🔢 | 🔢  | 🔢 |
| slow API      | 🔢  | 🔢 | 🔢  | 🔢 |


# How to check?

We need metric tfor this. I'm thinking about the following:

* Stress test for 2 minutes
* 120*5 requests with timeout of 3 secs
* The result would be the successful requests

# Requirements

* Docker daemon running

#TODO:

* Move workers_class and loads to classes with inheritance 
* Find external slow link for `slow_api` load