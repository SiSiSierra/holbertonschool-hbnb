from flask_restx import Namespace, Resource, fields
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
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.marshal_with(amenity_model_get, code=200, as_list=True)
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities()


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model_get, code=200)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        new_data = api.payload
        facade.update_amenity(amenity_id, new_data)
        return {'id': amenity.id, 'name': amenity.name}
