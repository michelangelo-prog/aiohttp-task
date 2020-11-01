from aiohttp import web
import asyncio

from items.app.celery import broker

routes = web.RouteTableDef()

@routes.post('/items/', name='add_item')
async def add_item(request):
    data = await request.json()
    await send_task(data)
    await asyncio.sleep(7)
    return web.json_response(data=data, status=201)

@routes.get('/items/{key}', name="get_item")
async def get_item(request):
    key = request.match_info['key']
    return web.json_response(
        data={"key": key},
        status=200,
    )



async def send_task(data):

    broker.send_task('periodic.train_speed', kwargs=data)