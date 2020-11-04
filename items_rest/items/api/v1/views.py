import asyncio
import json

from aiohttp import web
from items.helpers import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from items.utils import GetItemRpcClient, send_message_to_broker

routes = web.RouteTableDef()


@routes.post("/api/v1/items/", name="add_item")
async def add_item(request):
    data = await request.json()
    await send_message_to_broker(
        json.dumps({"method": "POST", "data": data}), priority=9
    )
    return web.json_response(
        data={"status": "Request created."}, status=HTTP_201_CREATED
    )


@routes.get("/api/v1/items/{key}", name="get_item")
async def get_item(request):
    key = request.match_info["key"]
    loop = asyncio.get_running_loop()
    rpc_client = await GetItemRpcClient(loop).connect()
    response = await rpc_client.call(
        json.dumps({"method": "GET", "data": {"key": key}})
    )

    response_data = json.loads(response)
    if response_data["status"] == "success":
        return web.json_response(
            data={
                "key": response_data["data"]["key"],
                "value": response_data["data"]["value"],
            },
            status=HTTP_200_OK,
        )
    elif response_data["status"] == "failure":
        return web.json_response(
            data={"error": response_data["data"]["error"]}, status=HTTP_404_NOT_FOUND
        )
    else:
        return web.json_response(data=dict(), status=HTTP_500_INTERNAL_SERVER_ERROR)
