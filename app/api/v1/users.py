from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import json

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
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        try:
            facade.get_user_by_email(user_data['email'])
            return {'error': 'Email already registered'}, 400
        except KeyError:
            pass

        try:
            new_user = facade.create_user(user_data)
            return {
                    'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email
                    }, 201
        except TypeError as err:
            return {'error': str(err)}, 400
        except ValueError as err:
            return {'error': str(err)}, 400

    # @api.response(200, 'OK')
    @api.marshal_with(user_model_get, code=200, as_list=True)
    def get(self):
        """ Get a list of all users """
        return facade.get_all_users()


@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model_get, code=200)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                }, 200

    @jwt_required
    @api.expect(user_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action.')
    @api.response(400, 'Invalid Input Data')
    def put(self, user_id):
        """Update user info by ID"""
        if get_jwt_identity() != user_id:
            return {'error': 'Unauthorized action.'}, 403
        new_data = api.payload
        if new_data.get['email'] is not None or new_data.get['password'] is \
                not None:
            return {'error': 'You cannot modify email or password'}, 403
        try:
            user = facade.get_user(user_id)
            facade.update_user(user_id, new_data)
            return {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                    }, 200
        except KeyError:
            return {'error': str(err)}, 400
