import os

class BaseConfig:
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

class RabbitConfig:
    BROKER_URL = os.getenv("RABBIT_URL")
    STORAGE_QUEUE_NAME = os.getenv("STORAGE_QUEUE_NAME")
