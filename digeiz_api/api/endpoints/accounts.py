import logging

from flask import request
from flask_restplus import Resource, marshal
from digeiz_api.api.db_access_module import create_account, delete_account, update_account
from digeiz_api.api.custom_exceptions import AccountNotFoundException, current_time
from digeiz_api.api.ApiModels import ApiModels
from digeiz_api.app import app
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
from digeiz_api.database.models import Account, Mall, Unit

log = logging.getLogger(__name__)

ns_accounts = app.namespace('Accounts', description='Operations related to Accounts')


@ns_accounts.route('/')
class AccountCollection(Resource):

    @app.response(200, 'Success ', ApiModels.account_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(400, 'Error response ', ApiModels.error_response)
    def get(self):
        accounts = Account.query.all()
        return marshal(accounts, ApiModels.account_definition_response), 200

    @app.expect(ApiModels.account_definition_request)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(200, 'Success ', ApiModels.error_response)
    def post(self):
        data = request.json
        try:
            account = create_account(data)
            return marshal(account, ApiModels.account_definition_response), 200
        except exc.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500
        except:
            return marshal(
                {'error': f'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500


@ns_accounts.route('/<int:id>')
@app.response(404, 'account not found.')
class AccountItem(Resource):
    @app.response(200, 'Success response ', ApiModels.account_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def get(self, id):
        try:
            account = Account.query.filter(Account.id == id).one()
            return marshal(account, ApiModels.account_definition_response), 200
        except NoResultFound:
            return marshal(
                {'error': f'DB result not found for Account ID : {id}', 'requested_at': current_time()},
                ApiModels.error_response), 404
        except exc.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.expect(ApiModels.account_definition_request)
    @app.response(200, 'Account successfully updated.', ApiModels.account_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def put(self, id):
        data = request.json
        try:
            account = update_account(id, data)
            return marshal(account, ApiModels.account_definition_response), 200
        except AccountNotFoundException as e:
            return marshal(
                {'error': f'Account ID {e.account_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404
        except exec.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.response(204, 'account successfully deleted.')
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def delete(self, id):
        try:
            account = delete_account(id)
            return account, 204
        except AccountNotFoundException as e:
            return marshal(
                {'error': f'Account ID {e.account_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404
        except exec.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500


@ns_accounts.route('/<int:account_id>/malls')
class AccountMallsCollection(Resource):
    @app.response(200, 'Success ', ApiModels.mall_definition_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def get(self, account_id):
        if (Account.query.filter(Account.id == account_id).first() is not None):
            return marshal(
                Mall.query.filter(Mall.account_id == account_id).all(),
                ApiModels.mall_definition_response), 200
        else:
            return marshal(
                {'error': f'Account ID {account_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404


@ns_accounts.route('/<int:account_id>/units')
@app.response(404, 'account not found.')
class AccountUnitsCollection(Resource):
    @app.response(200, 'Success ', ApiModels.mall_definition_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def get(self, account_id):
        if (Account.query.filter(Account.id == account_id).first() is not None):
            return marshal(
                Unit.query.filter(Mall.account_id == account_id).filter(Unit.mall_id == Mall.account_id).all(),
                ApiModels.mall_definition), 200
        else:
            return marshal(
                {'error': f'Account ID {account_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404
