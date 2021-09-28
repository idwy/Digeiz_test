import unittest
from digeiz_api.app import flask_api, db
import json


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        flask_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_api.db'
        flask_api.config['TESTING'] = True
        self.app = flask_api.test_client()
        db.drop_all()
        db.create_all()

    def test_get_all_accounts_endpoint_empty(self):
        response = self.app.get("/Accounts/")

        self.assertEqual(
            response.status, '200 OK'
        )
        self.assertEqual(
            response.get_json(), []
        )

    def test_create_account_endpoint_valid_payload_and_check_get_all_account(self):
        data = json.dumps({"name": "acc_name1"})
        response = self.app.post("/Accounts/", data=data, content_type='application/json')

        self.assertEqual(
            response.status, '200 OK'
        )

        self.assertEqual(
            response.get_json()['name'], 'acc_name1'
        )

        data2 = json.dumps({"name": "acc_name2"})
        response2 = self.app.post("/Accounts/", data=data2, content_type='application/json')

        self.assertEqual(
            response2.status, '200 OK'
        )

        self.assertEqual(
            response2.get_json()['name'], 'acc_name2'
        )

        response = self.app.get("/Accounts/")

        self.assertEqual(
            response.status, '200 OK'
        )
        self.assertEqual(
            response.get_json(), [{'id': 1, 'name': 'acc_name1'}, {'id': 2, 'name': 'acc_name2'}]
        )

    def test_delete_invalid_account_endpoint(self):
        account_id = 1
        response = self.app.delete(f"/Accounts/{account_id}")
        self.assertEqual(
            response.status, '404 NOT FOUND'
        )

    def test_delete_valid_account_endpoint(self):
        account_id = 1
        data = json.dumps({"name": "acc_name1"})
        self.app.post("/Accounts/", data=data, content_type='application/json')

        response = self.app.delete(f"/Accounts/{account_id}")
        self.assertEqual(
            response.status, '204 NO CONTENT'
        )

    def test_get_single_account_endpoint(self):

        data = json.dumps({"name": "acc_name1"})
        self.app.post("/Accounts/", data=data, content_type='application/json')

        account_id = 1
        response = self.app.get(f"/Accounts/{account_id}")

        self.assertEqual(
            response.status, '200 OK'
        )
        self.assertEqual(
            response.get_json(), {'id': account_id, 'name': 'acc_name1'}
        )

    def test_change_name_single_valid_account_endpoint(self):
        account_id = 1
        old_name = "acc_name1"
        new_name = "new_account_name"
        data1 = json.dumps({"name": old_name})
        self.app.post("/Accounts/", data=data1, content_type='application/json')

        data2 = json.dumps({"name": new_name})
        self.app.put(f"/Accounts/{account_id}", data=data2, content_type='application/json')

        response = self.app.get(f"/Accounts/{account_id}")

        self.assertEqual(
            response.status, '200 OK'
        )
        self.assertEqual(
            response.get_json(), {'id': account_id, 'name': new_name}
        )

    def test_change_name_single_invalid_account_endpoint_and_display_custom_error(self):
        account_id = 1
        new_name = "new_account_name"
        data2 = json.dumps({"name": new_name})
        self.app.put(f"/Accounts/{account_id}", data=data2, content_type='application/json')

        response = self.app.get(f"/Accounts/{account_id}")

        self.assertEqual(
            response.status, '404 NOT FOUND'
        )
        self.assertEqual(
            response.get_json()['error'], f'DB result not found for Account ID : {account_id}'
        )
