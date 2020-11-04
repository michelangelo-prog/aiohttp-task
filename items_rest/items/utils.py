import uuid

from aio_pika import IncomingMessage, Message, connect, connect_robust
from items.config import RabbitConfig


async def send_message_to_broker(
    message,
    broker_url=RabbitConfig.BROKER_URL,
    routing_key=RabbitConfig.STORAGE_QUEUE_NAME,
    priority=0,
):
    connection = await connect_robust(broker_url)
    channel = await connection.channel()
    await channel.default_exchange.publish(
        Message(message.encode(), content_type="text/plain", priority=priority),
        routing_key=routing_key,
    )


class GetItemRpcClient:
    def __init__(
        self,
        loop,
        broker_url=RabbitConfig.BROKER_URL,
        routing_queue_name=RabbitConfig.STORAGE_QUEUE_NAME,
    ):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop
        self.broker_url = broker_url
        self.routing_queue_name = routing_queue_name

    async def connect(self):
        self.connection = await connect(self.broker_url, loop=self.loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(
            exclusive=True, auto_delete=True
        )
        await self.callback_queue.consume(self.on_response)

        return self

    async def on_response(self, message: IncomingMessage):
        async with message.process():
            future = self.futures.pop(message.correlation_id)
            future.set_result(message.body.decode())
            await self.channel.close()

    async def call(self, message):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                message.encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key=self.routing_queue_name,
        )

        return await future
