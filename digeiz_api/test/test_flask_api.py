import unittest
from digeiz_api.app import flask_api
import json


def check_response(value):
    return value == [] or value.get_json()[0]['id'] is not None


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = flask_api.test_client()

    def test_accounts_get_endpoint(self):
        response = self.app.get("/Accounts/")

        self.assertEqual(
            response.status, '200 OK'
        )
        self.assertTrue(
            check_response(response)
        )

    def test_accounts_post_endpoint(self):
        data = json.dumps({"name": "acc_name"})
        response = self.app.post("/Accounts/", data=data, content_type='application/json')

        self.assertEqual(
            response.status, '200 OK'
        )

        self.assertEqual(
            response.get_json()['name'], 'acc_name'
        )

        data2 = json.dumps({"name": "acc_name2"})
        response2 = self.app.post("/Accounts/", data=data2, content_type='application/json')

        self.assertEqual(
            response2.status, '200 OK'
        )

        self.assertEqual(
            response2.get_json()['name'], 'acc_name2'
        )
