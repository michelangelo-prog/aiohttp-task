import logging

from .routes import setup_routes
from aiohttp import web


async def init_app():
    app = web.Application()

    # setup views and routes
    setup_routes(app)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)
