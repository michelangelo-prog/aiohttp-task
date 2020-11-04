from .api.v1.views import routes as api_v1_routes


def setup_routes(app):
    app.add_routes(api_v1_routes)
