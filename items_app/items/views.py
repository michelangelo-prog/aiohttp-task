from aiohttp import web

routes = web.RouteTableDef()

@routes.post('/items/', name='add_item')
async def add_item(request):
    data = await request.json()
    return web.json_response(data=data, status=201)

@routes.get('/items/{key}', name="get_item")
async def get_item(request):
    key = request.match_info['key']
    return web.json_response(
        data={"key": key},
        status=200,
    )