from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade
import json

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity_POST', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_model_get = api.model('Amenity_GET', {
    'id': fields.String,
    'name': fields.String
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'No authorization provided')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        try:
            amenity = facade.create_amenity(api.payload)
            return {
                    'id': amenity.id,
                    'name': amenity.name
                    }
        except (TypeError, ValueError) as err:
            return {'err': str(err)}, 400


    @api.marshal_with(amenity_model_get, code=200, as_list=True)
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities()


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model_get, code=200)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return {
                'id': amenity.id,
                'name': amenity.name
                }
        except KeyError as err:
            return {'error': str(err)}, 404
        

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @api.response(401, 'No authorization provided')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        new_data = api.payload
        try:
            facade.get_amenity(amenity_id)
            amenity = facade.update_amenity(amenity_id, new_data)
            return {
                    'id': amenity.id,
                    'name': amenity.name
                    }
        except KeyError as err:
            return {'error': str(err)}, 404
        except Exception as err:
            return {'error': str(err)}, 400
