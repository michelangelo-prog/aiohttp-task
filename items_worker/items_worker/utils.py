import json

from aio_pika import Exchange, IncomingMessage, Message

from .storage import add_to_storage, get_from_storage


async def reply_for_incoming_message(
    exchange: Exchange, message: IncomingMessage, data
):
    response = json.dumps(data).encode()
    await exchange.publish(
        Message(
            body=response,
            correlation_id=message.correlation_id,
        ),
        routing_key=message.reply_to,
    )


async def message_handler(exchange: Exchange, message: IncomingMessage):
    with message.process():
        data = json.loads(message.body.decode())
        if data["method"] == "POST":
            add_to_storage(data["data"]["key"], data["data"]["value"])
        elif data["method"] == "GET":
            try:
                value = get_from_storage(data["data"]["key"])
                response = {
                    "status": "success",
                    "data": {"key": data["data"]["key"], "value": value},
                }
            except KeyError:
                response = {"status": "failure", "data": {"error": "Not found."}}
            await reply_for_incoming_message(exchange, message, response)
