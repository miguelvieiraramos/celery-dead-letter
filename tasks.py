from celery import shared_task
from celery.exceptions import Reject

@shared_task(acks_late=True)
def print_hi(name):
    print(f'Hi, {name}')
    raise Reject(Exception('dead-letter exception'), requeue=False)