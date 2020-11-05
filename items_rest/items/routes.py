from .api.v1.views import add_item, get_item


def setup_routes(app):
    app.router.add_post("/api/v1/items/", add_item, name="add_item")
    app.router.add_get("/api/v1/items/{key}", get_item, name="get_item")
