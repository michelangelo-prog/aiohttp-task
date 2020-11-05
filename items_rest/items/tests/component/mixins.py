from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from items.routes import setup_routes


class BaseTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        setup_routes(app)
        return app


class ItemMixin:
    async def add_item(self, **kwargs):
        response = await self.client.post("/api/v1/items/", **kwargs)
        return response

    async def get_item(self, key="", **kwargs):
        path = "/api/v1/items/{}".format(key)
        response = await self.client.get(path, **kwargs)
        return response
