from celery import Celery
import os

class CeleryBrokerConfig(object):
    """Celery Broker configuration."""

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "amqp://myuser:mypassword@rabbitmq_broker:5672/myvhost")
    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND", "amqp://myuser:mypassword@rabbitmq_broker:5672/myvhost"
    )


def make_celery_broker():
    celery = Celery(
        "test",
        broker='pyamqp://admin:mypass@rabbit:5672',
        backend='rpc://',
    )
    return celery

broker = make_celery_broker()
