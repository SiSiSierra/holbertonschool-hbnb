from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place_POST', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True, description='Latitude of the place'),
    'longitude': fields.Float(
        required=True, description='Longitude of the place'),
})

place_model_get = api.model('Place_GET', {
    'id': fields.String(description='ID of the place'),
    'title': fields.String(description='Name of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price of the place per night'),
    'latitude': fields.Float(description='Global latitude of the place'),
    'longitude': fields.Float(description='Global longitude of the place'),
    'owner': fields.Nested(user_model, description=\
            'Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description=\
            'List of amenity IDs this place hosts'),
})


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        data = request.json
        data['owner_id'] = current_user
        try:
            # Delegate handling to the facade layer
            new_place = facade.create_place(data)

            # Return serialized summary of the newly created object
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as err:
            # Catches domain validation errors
            # (e.g. negative price, out-of-bound coordinates, missing owner)
            return {'error': str(err)}, 400

    @api.marshal_with(place_model_get, code=200, as_list=True)
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        out = []
        for p in places:
            owner = facade.get_user(p.owner_id)
            out.append({
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'price': p.price,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'amenities': [{
                    'id': amenity,
                    'name': facade.get_amenity(amenity).name
                } for amenity in p.amenities]
            })
        return out, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model_get, code=200)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            owner = facade.get_user(place.owner_id)
        except KeyError as err:
            return {'err': str(err)}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            },
            'amenities': [{
                'id': amenity,
                'name': facade.get_amenity(amenity).name
            } for amenity in place.amenities]
        }, 200

    @jwt_required()
    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = get_jwt_identity()
        try:
            # Verify existence
            place = facade.get_place(place_id)
            owner = facade.get_user(place.owner_id)
            # Verify owner / admin
            if user_id != place.owner_id and not is_admin:
                return {'error': 'Unauthorised action.'}, 403
            # Update place
            updated_place = facade.update_place(place_id, api.payload)
            return {
                    'id': place.id,
                    'title': place.title,
                    'description': place.description,
                    'price': place.price,
                    'latitude': place.latitude,
                    'longitude': place.longitude,
                    'owner': {
                        'id': owner.id,
                        'first_name': owner.first_name,
                        'last_name': owner.last_name,
                        'email': owner.email
                    },
                    'amenities': [{
                        'id': amenity,
                        'name': facade.get_amenity(amenity).name
                    } for amenity in place.amenities]
            }, 200 
        except KeyError as err:
            return {'error': str(err)}, 404
        except (TypeError, ValueError) as err:
            return {'error': str(err)}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404

        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id if hasattr(r.user, 'id') else str(r.user)
        } for r in reviews], 200
