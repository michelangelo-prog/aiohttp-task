import asyncio
import json
from functools import partial

from aio_pika import Exchange, IncomingMessage, Message, connect_robust
from sqlitedict import SqliteDict

PATH_TO_DB = "./my_db.sqlite"


def get_storage():
    return SqliteDict(PATH_TO_DB, autocommit=True)


def add_to_storage(data):
    storage = get_storage()
    storage[data["key"]] = data["value"]


def get_from_storage(key):
    storage = get_storage()
    return storage[key]


async def send_message_to_client(exchange: Exchange, message: IncomingMessage, data):
    response = json.dumps(data).encode("utf-8")
    await exchange.publish(
        Message(
            body=response,
            correlation_id=message.correlation_id,
        ),
        routing_key=message.reply_to,
    )


async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        data = json.loads(message.body.decode())
        if data["method"] == "POST":
            add_to_storage(data["data"])
        elif data["method"] == "GET":
            try:
                value = get_from_storage(data["data"]["key"])
                response = {
                    "status": "success",
                    "data": {"key": data["data"]["key"], "value": value},
                }
            except KeyError:
                response = {"status": "failure", "data": {"error": "Not found."}}
            await send_message_to_client(exchange, message, response)
        print("Request completed")


async def main(loop):
    connection = await connect_robust("amqp://admin:mypass@rabbitmq:5672", loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue("storage_queue", durable=True)
    await queue.consume(partial(on_message, channel.default_exchange))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    print(" [*] Waiting for messages...")
    loop.run_forever()
