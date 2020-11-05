import json
from unittest.mock import call

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, mock, unittest_run_loop
from items.helpers import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from items.routes import setup_routes
from items.tests.factories import ItemDictFactory


class TestAddItem(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        setup_routes(app)
        return app

    async def add_item(self, **kwargs):
        response = await self.client.post("/api/v1/items/", **kwargs)
        return response

    async def side_effect__send_message_to_broker(self, *args, **kwargs):
        pass

    @mock.patch(
        "items.api.v1.views.send_message_to_broker",
        side_effect=side_effect__send_message_to_broker,
    )
    @unittest_run_loop
    async def test_add_item(self, mock_send_message_to_broker):
        data = ItemDictFactory.build()
        response = await self.add_item(data=json.dumps(data))
        resp_json = await response.json()

        self.assertEqual(HTTP_201_CREATED, response.status)
        expected_json = {"status": "Request created."}
        self.assertEqual(expected_json, resp_json)

        # check if add_item send message to broker
        mock_send_message_to_broker.assert_called_once()
        expected_call = call(
            json.dumps(
                {
                    "method": "POST",
                    "data": {
                        "key": data["key"],
                        "value": data["value"],
                    },
                }
            ),
            priority=9,
        )
        self.assertIn(expected_call, mock_send_message_to_broker.call_args_list)

    @mock.patch(
        "items.api.v1.views.send_message_to_broker",
        side_effect=side_effect__send_message_to_broker,
    )
    @unittest_run_loop
    async def test_get_error_when_send_request_without_body(
        self, mock_send_message_to_broker
    ):
        response = await self.add_item()
        resp_json = await response.json()
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status)
        self.assertIn("error", resp_json.keys())

        mock_send_message_to_broker.assert_not_called()

    @mock.patch(
        "items.api.v1.views.send_message_to_broker",
        side_effect=side_effect__send_message_to_broker,
    )
    @unittest_run_loop
    async def test_get_error_when_send_request_without_key(
        self, mock_send_message_to_broker
    ):
        data = ItemDictFactory.build()
        data.pop("key")
        response = await self.add_item(data=json.dumps(data))
        resp_json = await response.json()
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status)
        self.assertIn("error", resp_json.keys())
        self.assertIn("key", resp_json["errors"].keys())

        mock_send_message_to_broker.assert_not_called()

    @mock.patch(
        "items.api.v1.views.send_message_to_broker",
        side_effect=side_effect__send_message_to_broker,
    )
    @unittest_run_loop
    async def test_get_error_when_send_request_without_value(
        self, mock_send_message_to_broker
    ):
        data = ItemDictFactory.build()
        data.pop("value")
        response = await self.add_item(data=json.dumps(data))
        resp_json = await response.json()
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status)
        self.assertIn("error", resp_json.keys())
        self.assertIn("value", resp_json["errors"].keys())

        mock_send_message_to_broker.assert_not_called()

    @mock.patch(
        "items.api.v1.views.send_message_to_broker",
        side_effect=side_effect__send_message_to_broker,
    )
    @unittest_run_loop
    async def test_get_error_when_send_request_with_key_as_int(
        self, mock_send_message_to_broker
    ):
        data = ItemDictFactory.build()
        data["key"] = 1
        response = await self.add_item(data=json.dumps(data))
        resp_json = await response.json()
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status)
        self.assertIn("error", resp_json.keys())
        self.assertIn("key", resp_json["errors"].keys())

        mock_send_message_to_broker.assert_not_called()

    @mock.patch(
        "items.api.v1.views.send_message_to_broker",
        side_effect=side_effect__send_message_to_broker,
    )
    @unittest_run_loop
    async def test_get_error_when_send_request_with_value_as_string(
        self, mock_send_message_to_broker
    ):
        data = ItemDictFactory.build()
        data["value"] = "1"
        response = await self.add_item(data=json.dumps(data))
        resp_json = await response.json()
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status)
        self.assertIn("error", resp_json.keys())
        self.assertIn("value", resp_json["errors"].keys())

        mock_send_message_to_broker.assert_not_called()
