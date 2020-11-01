from  ..celery import make_celery_broker

worker = make_celery_broker()


@worker.task(name="periodic.train_speed")
def train_speed(**data):
    print("Train speed {} - TASK START".format(data))
