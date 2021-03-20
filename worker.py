from celery import Celery
from kombu import Exchange, Queue
from celery.exceptions import Reject
from dead_letter import DeadLetterConsumer


def setup(app):
    app_exchange = Exchange('e.app', type='direct')
    app_queue = Queue(
        name='q.app', 
        exchange=app_exchange, 
        routing_key='app', 
        queue_arguments={
        'x-dead-letter-exchange': 'e.deadletter',
        'x-dead-letter-routing-key': 'deadletter'
    })
    app.conf.task_queues = (app_queue,)
    app.conf.beat_schedule = {
        'print-every-20-seconds': {
          'task': 'tasks.print_hi',
          'schedule': 20.0,
          'args': ('Kakashi',),
          'options': {'queue': 'q.app'}
      },
    }
    # app.steps['consumer'].add(DeadLetterConsumer)


def create_app():
    app = Celery('app')
    app.autodiscover_tasks(['tasks'], force=True)
    setup(app)
    return app

app = create_app()
