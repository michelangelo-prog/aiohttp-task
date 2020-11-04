import os

basedir = os.path.abspath(os.path.dirname(__file__))
PATH_TO_DB = os.path.join(os.path.dirname(basedir), "my_db.sqlite")


class RabbitConfig:
    BROKER_URL = "amqp://{}:{}@{}:{}".format(
        os.getenv("RABBITMQ_DEFAULT_USER"),
        os.getenv("RABBITMQ_DEFAULT_PASS"),
        os.getenv("RABBITMQ_HOST"),
        os.getenv("RABBITMQ_PORT"),
    )
    STORAGE_QUEUE_NAME = os.getenv("STORAGE_QUEUE_NAME")
