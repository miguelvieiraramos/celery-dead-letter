from celery import Celery, bootsteps
from kombu import Exchange, Queue
from celery.exceptions import Reject
from kombu import Consumer, Exchange, Queue


deadletter_exchange = Exchange('e.deadletter', type='direct')
deadletter_queue = Queue(name='q.deadletter', exchange=deadletter_exchange, routing_key='deadletter')

class DeadLetterConsumer(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[deadletter_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        message.ack()


def setup(app):
    app.conf.task_queues = (deadletter_queue,)
    app.conf.task_routes = {'tasks.print_hi': {'queue': 'q.app'}}

    app.steps['consumer'].add(DeadLetterConsumer)


def create_app():
    app = Celery('dead_letter')
    app.autodiscover_tasks(['tasks'], force=True)
    setup(app)
    return app

dead_letter_app = create_app()
