#!/usr/bin/python3
import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestUserCreation(unittest.TestCase):

    def test_standard_creation(self):        
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.is_admin, False)  # Default value

class TestPlaceCreation(unittest.TestCase):

    user = User(first_name="Jonathon", last_name="Clus", email="jon.clus@holberton.com", password="password")

    def test_standard_creation(self):
        place = Place("Holberton", "It's cool", 20.0, -37.8174123, 144.9592932, self.user)
        self.assertEqual(place.title, "Holberton")
        self.assertEqual(place.description, "It's cool")
        self.assertEqual(place.price, 20.0)
        self.assertEqual(place.latitude, -37.8174123)
        self.assertEqual(place.longitude, 144.9592932)
        self.assertIs(place.owner, self.user)

class TestReviewCreation(unittest.TestCase):

    userReviewer = User(first_name="Sierra", last_name="Hunt", email="SierraHunt@protonmail.com", password="pswd1")
    userOwner = User(first_name="Jonathon", last_name="Clus", email="jon.clus@holberton.com", password="pswd2")
    place = Place("Holberton", "It's cool", 20.0, -37.8174123, 144.9592932, userOwner)

    def test_standard_creation(self):
        review = Review("Informative.", 4, self.place, self.userReviewer)
        self.assertEqual("Informative.", review.text)
        self.assertEqual(4, review.rating)
        self.assertIs(self.userReviewer, review.user)

class TestAmenityCreation(unittest.TestCase):

    def test_standard_creation(self):
        amenity = Amenity("Wi-Fi")
        self.assertEqual("Wi-Fi", amenity.name)

if __name__ == '__main__':
    unittest.main()
