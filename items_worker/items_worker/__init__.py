from functools import partial

from aio_pika import connect_robust

from .config import RabbitConfig
from .utils import message_handler


async def main(loop):
    connection = await connect_robust(RabbitConfig.BROKER_URL, loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(RabbitConfig.STORAGE_QUEUE_NAME, durable=True)
    await queue.consume(partial(message_handler, channel.default_exchange))
