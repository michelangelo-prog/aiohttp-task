from aiohttp import web
from .utils import send_message, RpcClient
import asyncio
import json

routes = web.RouteTableDef()

@routes.post('/items/', name='add_item')
async def add_item(request):
    data = await request.json()
    await send_message({"method": "POST", "data": data}, "storage_queue")
    return web.json_response(data={"status": "Request created."}, status=201)

@routes.get('/items/{key}', name="get_item")
async def get_item(request):
    key = request.match_info['key']
    data = {"method": "GET", "data": {"key": key}}
    loop = asyncio.get_running_loop()
    rpc = await RpcClient(loop).connect()
    response = await rpc.call(data)
    return web.json_response(
        data=json.loads(response),
        status=200,
    )