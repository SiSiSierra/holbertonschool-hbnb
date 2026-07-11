from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- USER METHODS -----

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        u = self.user_repo.get(user_id)
        if not u:
            raise KeyError("User not found")
        return u

    def get_user_by_email(self, email):
        u = self.user_repo.get_by_attribute('email', email)
        if not u:
            raise KeyError("User not found")
        return u

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    # ----- AMENITY METHODS -----

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # ----- PLACE METHODS -----

    def create_place(self, place_data):
        #Validate existence of given user
        owner = self.get_user(place_data.get('owner_id'))

        # Create the place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=place_data.get('owner_id')
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")
        return place

    def get_all_places(self):
        # 1. Fetch the entire collection list of stored places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)

        self.place_repo.update(place_id, place_data)
        return place

    # --- REVIEW METHODS ---
    def create_review(self, review_data):
        """ Create a new review object

        Params:
            review_data: Dict
                - text
                - rating
                - user_id
                - place_id

        Returns: Created review as dict, or error as dict, with HTTP code
        """
        # Verify user and place exist
        user = self.get_user(review_data.get('user_id'))
        place = self.get_place(review_data.get('place_id'))

        # Verify user isn't reviewing themselves
        if user.id == place.owner_id:
            return {'error': 'You cannot review your own place'}, 400
        
        # Verify user hasn't already reviewed this place
        for r in self.get_reviews_by_place(place.id):
            if r.user_id == user.id:
                return {'error': 'You have already reviewed this place'}, \
                        403

        # Create review
        new_review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(new_review)
        place.reviews.append(new_review.id)

        return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201


    def get_review(self, review_id):
        r = self.review_repo.get(review_id)
        if not r:
            raise KeyError("Review not found")
        return r

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)

        all_reviews = self.get_all_reviews()
        return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        """ Update a pre-existing review

        Params:
            review_id: UUID
            review_data: json
                - text
                - rating
                - user_id

        Returns: Review after updating as dict, or error as dict, with HTTP code
        """
        # Verify review exists
        review = self.get_review(review_id)
        
        # Verify the user changing is the user owning
        if review_data.get('user_id') != review.user_id:
            return {'error': 'Unauthorised action.'}, 403

        self.review_repo.update(review_id, review_data)
        return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
                }, 200

    def delete_review(self, review_id, user_id):
        """ Delete a review

        Params:
            review_id: UUID
            user_id: UUID

        Returns: Message or error describing outcome in dict, and HTTP code
        """
        # Verify review exists
        review = self.get_review(review_id)

        # Verify user deleting is the user owning
        if user_id != review.user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Remove review from associated place
        place = facade.get_place(review.place_id)
        place.reviews.remove(review_id)
        
        # Remove review from repo
        self.review_repo.delete(review_id)
        
        return {'message': 'Review delected successfully'}, 200
