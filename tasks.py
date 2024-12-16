# tasks.py

import logging

from os import environ

from celery import Celery

CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL', 'pyamqp://guest:guest@127.0.0.1:5672//')
CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')

app = Celery(name='projet', backend=CELERY_RESULT_BACKEND)


@app.task(name="task_1")
def task_1(message):
    """ celery task - task_1  """

    try:
        return f"task_1 message : {message}"

    except Exception as exc:
        logging.exception(exc)



@app.task(name="task_2")
def task_2(message):
    """ celery task - task_2  """

    try:
        return f"task_2 message : {message}"

    except Exception as exc:
        logging.exception(exc)
