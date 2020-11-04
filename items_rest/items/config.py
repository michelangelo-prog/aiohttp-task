import os


class BaseConfig:
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")


class RabbitConfig:
    BROKER_URL = "amqp://{}:{}@{}:{}".format(
        os.getenv("RABBITMQ_DEFAULT_USER"),
        os.getenv("RABBITMQ_DEFAULT_PASS"),
        os.getenv("RABBITMQ_HOST"),
        os.getenv("RABBITMQ_PORT"),
    )
    STORAGE_QUEUE_NAME = os.getenv("STORAGE_QUEUE_NAME")
