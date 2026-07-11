#!/usr/bin/python3
import unittest
import json
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository
from flask_jwt_extended import get_jwt_identity

class RequestSetUp():
    """Class with pre-defined data to use in tests
    Create an instance in setUp() of each test

    Attributes:
        h (headers): dict
        u1 (user1): dict
        u2 (user2): dict
        p1 (place1): dict
        r1 (review1): dict

    Functions:
        post(url(str), thing(dict))
        post_things(url(str), things(list(dict)))
        auth_user(user(dict))
    """

    def __init__(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()
        facade.user_repo = InMemoryRepository()
        facade.place_repo = InMemoryRepository()
        facade.review_repo = InMemoryRepository()
        facade.amenity_repo = InMemoryRepository()
        self.admin = {
                'first_name': 'admin',
                'last_name': 'user',
                'email': 'admin@user.com',
                'password': 'HBNB',
                'is_admin': True
                }
        facade.create_user(self.admin)
        self.h = {
                'Content-Type': 'application/json',
                'accept': 'application/json',
                                }
        self.h['Authorization'] = f'Bearer {self.auth_user(self.admin)}'
        self.u1 = {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'JaneDoe@mail.com',
                'password': '1nvisibl33'
                }
        self.u2 = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'JohnDoe@mail.com',
                'password': 'alsoinvis'
                }
        self.p1 = {
                'title': 'My House',
                'description': 'It is nice and big and cozy and good!!',
                'price': 50.99,
                'latitude': 80.4,
                'longitude': 110.5
                }
        self.r1 = {
                'text': 'It is indeed cozy',
                'rating': 4
                }

    def post(self, url, thing):
        return self.client.post(
                path=f'api/v1/{url}',
                headers=self.h,
                data=json.dumps(thing)
                )

    def post_things(self, url, things):
        l = []
        for t in things:
            r = self.client.post(
                    path=f'api/v1/{url}',
                    headers=self.h,
                    data=json.dumps(t)
                    )
            l.append(r)
        return l

    def auth_user(self, user):
        r = self.client.post(
                path='api/v1/auth/login',
                headers=self.h,
                data=json.dumps(user)
                )
        return r.json['access_token']

class RouteUserTest(unittest.TestCase):
    
    def setUp(self):
        self.tools = RequestSetUp()

    def testUserPOST(self):
        response = self.tools.post('users/', self.tools.u1).json
        self.assertEqual(response['first_name'], self.tools.u1['first_name'])
        self.assertEqual(response['last_name'], self.tools.u1['last_name'])
        self.assertEqual(response['email'], self.tools.u1['email'])
        with self.assertRaises(KeyError):
            response['password']
        self.assertTrue(type(response['id']) is str)

        self.url = f'/api/v1/users/{response['id']}'
        response2 = self.tools.client.get(path=self.url, headers=self.tools.h).json
        self.assertEqual(response2['first_name'], self.tools.u1['first_name'])
        self.assertEqual(response2['id'], response['id'])
   
    def testUserGET(self):
        r = self.tools.post_things('users/', (self.tools.u1, self.tools.u2))
        response = self.tools.client.get(path='/api/v1/users/', headers=self.tools.h)
        self.assertEqual(len(response.json), 3)
   
    def test_wrong_email(self):
        self.tools.u1['email'] = 'notgood'
        response = self.tools.post('users/', self.tools.u1)
        self.assertEqual(400, response.status_code)
        self.tools.u1['email'] = 5
        response = self.tools.post('users/', self.tools.u1)
        self.assertEqual(400, response.status_code)
        self.tools.u1['email'] = "Good@mail.com"
        response = self.tools.post('users/', self.tools.u1)
        response = self.tools.post('users/', self.tools.u1)
        self.assertEqual(400, response.status_code)


class RoutePlaceTest(unittest.TestCase):

    def setUp(self):
        self.tools = RequestSetUp()
        self.tools.post_things('users/', (self.tools.u1, self.tools.u2))

    def testPlacePOST(self):
        token = self.tools.auth_user(self.tools.u1)
        self.tools.h['Authorization'] = f"Bearer {token}"
        response = self.tools.post('places/', self.tools.p1)
        self.assertEqual(response.status_code, 201)
        places = self.tools.client.get('api/v1/places/', headers=self.tools.h)
        self.assertEqual(len(places.json), 1)
        self.assertEqual(places.json[0]['title'], 'My House')


class RouteReviewTest(unittest.TestCase):

    def setUp(self):
        self.tools = RequestSetUp()
        r = self.tools.post_things('users/', (self.tools.u1, self.tools.u2))
        self.tools.h['Authorization'] = f'Bearer {self.tools.auth_user(self.tools.u1)}'
        self.placeid = self.tools.post('places/', self.tools.p1).json['id']
    
    def testReviewPOST(self):
        self.tools.r1['place_id'] = self.placeid
        r = self.tools.post('reviews/', self.tools.r1)
        self.assertEqual(r.status_code, 400) # Same user from setup who made place
        token = self.tools.auth_user(self.tools.u2)
        self.tools.h['Authorization'] = f'Bearer {token}'
        r = self.tools.post('reviews/', self.tools.r1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.tools.client.get('api/v1/reviews/', headers=self.tools.h).json[0]['id'], r.json['id'])
        r = self.tools.client.get(f'api/v1/reviews/{r.json["id"]}', headers=self.tools.h).json
        self.assertEqual(r['rating'], 4)
        self.assertEqual(r['text'], 'It is indeed cozy')


if __name__ == "__main__":
    unittest.main()
