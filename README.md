# gunflawor
Stats for Gunicorn and flask with workers

Gunicorn has few workers types that you can use for your app.

It's been argued what type of the worker is best for your environment so we are trying to make some answer to the following questions:

All tests are c5.xlarge with 4 vCPU

Myths:
1) It's not crucial what worker type you have when you have big CPU/Mem load
2) Async worker might help when you have slow external load but not that much (graphs will illustrate)
3) will gevent.wsgi perform better then gunicorn.workers.ggevent on flask?



How to mesure it?

Lets first check what type of workers we have and what types of load we have

Workers:
1) gunicorn sync worker
2) gunicorn async worker - gevent
3) gevent.wsgi

Types of load:

1) CPU
2) Memory
3) sleep(2)
4) slow external web page (slow API)


There should be metrics of checks like this

| Type of load  | Gunicorn sync worker  | Gunicorn async worker | gevent.wsgi |
| ------------- | --------------------- | --------------------- | ----------- |
| CPU       | 🔢  | 🔢 | 🔢  | 🔢 |
| Memory    | 🔢  | 🔢 | 🔢  | 🔢 |
| sleep(2)  | 🔢  | 🔢 | 🔢  | 🔢 |
| slow API  | 🔢  | 🔢 | 🔢  | 🔢 |


How to check?

There is a tool by name Hey (simular to ApacheBench (ab).