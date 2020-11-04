from aio_pika import connect, connect_robust, Message, IncomingMessage
import json
import uuid

async def send_message(data, routing_key):
    connection = await connect_robust("amqp://admin:mypass@rabbitmq:5672")
    channel = await connection.channel()
    await channel.default_exchange.publish(
        Message(
            json.dumps(data).encode(),
            content_type="text/plain"
        ),
        routing_key=routing_key
    )


class RpcClient:
    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self):
        self.connection = await connect(
            "amqp://admin:mypass@rabbitmq:5672", loop=self.loop
        )
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True, auto_delete=True)
        await self.callback_queue.consume(self.on_response)

        return self

    async def on_response(self, message: IncomingMessage):
        async with message.process():
            future = self.futures.pop(message.correlation_id)
            future.set_result(message.body.decode('utf-8'))
            await self.channel.close()

    async def call(self, data):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                json.dumps(data).encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key="storage_queue",
        )

        return await future
