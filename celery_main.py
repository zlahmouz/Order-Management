#client.py

from os import environ

from celery import Celery

from tasks import task_1

CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL','pyamqp://guest:guest@127.0.0.1:5672//')
CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND','redis://127.0.0.1:6379/0')

# Celery instance
app = Celery(name='projet', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Send task to rabbitMq, wait the result and retrieve it from redis backend
task = task_1.delay("message produit avec la méthode delay")
result = task.get(timeout=30)

print (result)