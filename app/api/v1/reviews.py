from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review_POST', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_model_get = api.model('Review_GET', {
    'id': fields.String(description="Review ID"),
    'text': fields.String(description="Text of the review"),
    'rating': fields.Integer(description="Rating of the place (1-5)"),
    'user_id': fields.String(description="User ID that made the review"),
    'place_id': fields.String(description="Place ID of the review's subject")
})

review_model_put = api.model("Review_PUT", {
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating of the place (1-5)")
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorised action.')
    @api.response(404, 'Item not found')
    def post(self):
        """Register a new review"""
        data = api.payload
        data['user_id'] = get_jwt_identity() 
        # Create the review
        try:
            # Verify user / place exists
            user = facade.get_user(data.get('user_id'))
            place = facade.get_place(data.get('place_id'))
            # Verify place not owned by user
            if user.id == place.owner_id:
                return {'error': 'You cannot review your own place'}, 400
            review = facade.create_review(data)
            return {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                    }, 201
        except KeyError as err:
            return {'error': str(err)}, 404
        except (ValueError, TypeError) as err:
            return {'error': str(err)}, 400

    @api.marshal_with(review_model_get, code=200, as_list=True)
    def get(self):
        """Retrieve a list of all reviews"""
        return facade.get_all_reviews()


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model_get, code=200)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200
        except KeyError as err:
            return {'error': str(err)}, 404

    @jwt_required()
    @api.expect(review_model_put, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorised action.')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        data = api.payload
        # Update review
        try:
            # Existence validation
            review = facade.get_review(review_id)
            # Same-user / admin validation
            if user_id != review.user_id and not is_admin:
                return {'error': 'Unauthorized action'}, 403
            facade.update_review(review_id, data)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200
        except KeyError as err:
            return {'error': str(err)}, 404
        except (ValueError, TypeError) as err:
            return {'error': str(err)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        # Delete review
        try:
            # Verify review exists
            review = facade.get_review(review_id)
            # Same-user / admin validation
            if user_id != review.user_id and not is_admin:
                return {'error': 'Unauthorized action'}, 403
            facade.delete_review(review_id)
            return {'message': 'Review deleted'}
        except KeyError as err:
            return {'error': str(err)}, 404
