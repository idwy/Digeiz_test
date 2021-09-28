import logging

from flask import request
from flask_restplus import Resource, marshal
from digeiz_api.api.db_access_module import create_mall, delete_mall, update_mall
from digeiz_api.api.custom_exceptions import AccountNotFoundException, MallNotFoundException, current_time
from digeiz_api.api.ApiModels import ApiModels
from digeiz_api.app import app
from digeiz_api.database.models import Mall

log = logging.getLogger(__name__)

ns_malls = app.namespace('Malls', description='Operations related to Malls')


@ns_malls.route('/')
class MallCollection(Resource):

    @app.response(200, 'Success response ', ApiModels.mall_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    def get(self):
        try:
            return marshal(Mall.query.all(), ApiModels.mall_definition_response), 200
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.expect(ApiModels.mall_definition_request)
    @app.response(200, 'Mall successfully added.', ApiModels.mall_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def post(self):
        data = request.json
        try:
            mall = create_mall(data)
            return marshal(mall, ApiModels.mall_definition_response), 200
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


@ns_malls.route('/<int:id>')
class mallItem(Resource):
    @app.response(200, 'Success response ', ApiModels.mall_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    def get(self):
        try:
            return marshal(Mall.query.filter(Mall.id == id).one(), ApiModels.mall_definition_response), 200
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.expect(ApiModels.mall_definition_request)
    @app.response(200, 'Mall successfully updated.', ApiModels.mall_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def put(self, id):
        data = request.json
        try:
            mall = update_mall(id, data)
            return marshal(mall, ApiModels.mall_definition_response), 200
        except MallNotFoundException as e:
            return marshal(
                {'error': f'Mall ID {e.mall_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404
        except exec.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.response(204, 'Mall successfully deleted.')
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def delete(self, id):
        try:
            mall = delete_mall(id)
            return mall, 204

        except MallNotFoundException as e:
            return marshal(
                {'error': f'Mall ID {e.mall_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404

        except exec.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500

        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500
