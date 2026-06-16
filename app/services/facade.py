from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

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

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found.")

        # If your model needs owner_id, use owner_id=owner_id. 
        # If your model needs the whole user object, use owner=owner.
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner  
        )
        
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # 1. Fetch the place from the repository using its unique ID
        place = self.place_repo.get(place_id)
        
        # 2. Return the place object if found, or None if it doesn't exist
        if not place:
            return None
        return place

    def get_all_places(self):
        # 1. Fetch the entire collection list of stored places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        self.place_repo.update(place_id, place_data)
        return place
    
    # --- REVIEW METHODS ---
    def create_review(self, review_data):
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found.")
            
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found.")
            
        new_review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user=user,
            place=place
        )
        
        self.review_repo.add(new_review)
        
        # Sync the review reference to the targeted place
        if hasattr(place, 'reviews') and place.reviews is not None:
            place.reviews.append(new_review)
            
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        
        all_reviews = self.get_all_reviews()
        return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
            
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
            
        place = review.place
        if hasattr(place, 'reviews') and review in place.reviews:
            place.reviews.remove(review)
            
        return self.review_repo.delete(review_id)
