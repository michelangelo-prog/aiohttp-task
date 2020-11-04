import asyncio
import json

from aiohttp import web
from items.utils import GetItemRpcClient, send_message_to_broker

routes = web.RouteTableDef()


@routes.post("/items/", name="add_item")
async def add_item(request):
    data = await request.json()
    await send_message_to_broker(json.dumps({"method": "POST", "data": data}))
    return web.json_response(data={"status": "Request created."}, status=201)


@routes.get("/items/{key}", name="get_item")
async def get_item(request):
    key = request.match_info["key"]
    loop = asyncio.get_running_loop()
    rpc_client = await GetItemRpcClient(loop).connect()
    response = await rpc_client.call(
        json.dumps({"method": "GET", "data": {"key": key}})
    )
    return web.json_response(
        data=json.loads(response),
        status=200,
    )
