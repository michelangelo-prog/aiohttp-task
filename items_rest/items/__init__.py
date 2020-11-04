import logging

from .routes import setup_routes
from aiohttp import web
from .config import BaseConfig

async def init_app():
    app = web.Application()
    setup_routes(app)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app,
                host=BaseConfig.HOST,
                port=BaseConfig.PORT)