from flask_restplus import fields
from digeiz_api.app import app


class ApiModels:
    account_definition_response = app.model('AccountResponseModel', {
        'id': fields.Integer(
            readOnly=True,
            description='The unique identifier of an Account',
            ),
        'name': fields.String(required=True, description='Account name'),
    })

    account_definition_request = app.model('AccountRequestModel', {
        'name': fields.String(required=True, description='Account name'),
    })

    mall_definition_response = app.model('MallResponseModel', {
        'id': fields.Integer(
            readOnly=True,
            description='The unique identifier of an Mall',
            ),
        'name': fields.String(required=True, description='Mall name'),
        'account_id': fields.String(required=True, description='Account Id'),
    })

    mall_definition_request = app.model('MallRequestModel', {
        'name': fields.String(required=True, description='Mall name'),
        'account_id': fields.String(required=True, description='Account id'),
    })

    unit_definition_response = app.model('UnitResponseModel', {
        'id': fields.Integer(
            readOnly=True,
            description='The unique identifier of an Unit',
            ),
        'name': fields.String(required=True, description='Unit name'),
        'mall_id': fields.String(required=True, description='mall id'),
    })

    unit_definition_request = app.model('UnitRequestModel', {
        'name': fields.String(required=True, description='Unit name'),
        'mall_id': fields.String(required=True, description='mall id'),
    })

    error_response = app.model('ErrorResponse', {
        'error': fields.String(attribute='error'),
        'requested_at': fields.String(attribute='requested_at'),
    })
