from .api.v1.views import routes

def setup_routes(app):
    app.add_routes(routes)
