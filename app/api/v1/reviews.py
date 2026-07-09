from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    def post(self):
        """Register a new review"""
        data = request.json
        data['user_id'] = get_jwt_identity()
        
        # Create the review
        try:
            return(facade.create_review(data))
        except ValueError as err:
            return {'error': str(err)}, 400
        except KeyError as err:
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
        data = request.json
        data['user_id'] = get_jwt_identity()
        # Update review
        try:
            return facade.update_review(review_id, data)
        except ValueError as err:
            return {'error': str(err)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""

        # Verify review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Only the owning user can delete a review
        current_user = get_jwt_identity()
        if review.user != current_user:
            return {'error': 'Only the user who created the review can delete \
                    it'}, 403

        # Delete review
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
