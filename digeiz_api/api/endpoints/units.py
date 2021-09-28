import logging

from flask import request
from flask_restplus import Resource, marshal
from digeiz_api.api.db_access_module import create_unit, delete_unit, update_unit
from digeiz_api.api.custom_exceptions import MallNotFoundException, UnitNotFoundException, current_time
from digeiz_api.api.ApiModels import ApiModels
from digeiz_api.app import app
from digeiz_api.database.models import Unit

log = logging.getLogger(__name__)

ns_units = app.namespace('Units', description='Operations related to Units')


@ns_units.route('/')
class UnitCollection(Resource):

    @app.response(200, 'Success response ', ApiModels.unit_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    def get(self):
        try:
            return marshal(Unit.query.all(), ApiModels.unit_definition_response), 200
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.expect(ApiModels.unit_definition_request)
    @app.response(200, 'Unit successfully added.', ApiModels.unit_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def post(self):
        data = request.json
        try:
            unit = create_unit(data)
            return marshal(unit, ApiModels.unit_definition_response), 200
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


@ns_units.route('/<int:id>')
class UnitItem(Resource):
    @app.response(200, 'Success response ', ApiModels.unit_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    def get(self, id):
        try:
            return marshal(Unit.query.filter(Unit.id == id).one(), ApiModels.unit_definition_response), 200
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.expect(ApiModels.unit_definition_request)
    @app.response(200, 'Unit successfully updated.', ApiModels.unit_definition_response)
    @app.response(500, 'Error response ', ApiModels.error_response)
    @app.response(404, 'DB result not found ', ApiModels.error_response)
    def put(self, id):
        data = request.json
        try:
            unit = update_unit(id, data)
            return marshal(unit, ApiModels.unit_definition_response), 200
        except UnitNotFoundException as e:
            return marshal(
                {'error': f'Mall ID {e.unit_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404
        except exec.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500
        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500

    @app.response(204, 'unit successfully deleted.')
    def delete(self, id):
        try:
            unit = delete_unit(id)
            return unit, 204

        except UnitNotFoundException as e:
            return marshal(
                {'error': f'Unit ID {e.unit_id} not found', 'requested_at': current_time()},
                ApiModels.error_response), 404

        except exec.SQLAlchemyError:
            return marshal(
                {'error': 'Undefined DB error', 'requested_at': current_time()},
                ApiModels.error_response), 500

        except:
            return marshal(
                {'error': 'Server error', 'requested_at': current_time()},
                ApiModels.error_response), 500
