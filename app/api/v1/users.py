from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
import json
import re

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User_POST', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'),
    'email': fields.String(
        required=True,
        description='Email of the user'),
    'password': fields.String(
        required=True,
        description='Password of the user')
})

user_model_get = api.model('User_GET', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})


@api.route('/')
class UserList(Resource):
    @api.marshal_with(user_model_get, code=200, as_list=True)
    def get(self):
        """ Get a list of all users """
        return facade.get_all_users()

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'No authorization provided')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user, admin only"""

        if not get_jwt().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        user_data = api.payload
        try:
            facade.get_user_by_email(user_data['email'])
            return {'error': 'Email already registered'}, 400
        except KeyError:
            pass
        # Validate e-mail format
        valid_email_regex = \
            '^(\\w|\\.|\\_|\\-)+[@](\\w|\\_|\\-|\\.)+[.]\\w{2,3}$'
        if not re.search(valid_email_regex, user_data['email']):
            return {'error': "email must be in a valid e-mail format"}, 400
        try:
            new_user = facade.create_user(user_data)
            return {
                    'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email
                    }, 201
        except (TypeError, ValueError) as err:
            return {'error': str(err)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model_get, code=200)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            return {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                    }, 200
        except KeyError as err:
            return {'error': str(err)}, 404

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'Invalid Input Data')
    @api.response(401, 'No Authorization provided')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user info by ID, admin only"""

        if not get_jwt().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        try:
            user = facade.get_user(user_id)
            facade.update_user(user_id, api.payload)
            return {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                    }, 200
        except KeyError:
            return {'error': str(err)}, 400

