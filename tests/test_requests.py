#!/usr/bin/python3
import unittest
import json
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository


class RequestSetUp():
    
    def __init__(self):
        self.headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json'
                }
        self.user1 = {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'JaneDoe@mail.com',
                'password': '1nvisibl33'
                }
        self.user2 = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'JohnDoe@mail.com',
                'password': 'alsoinvis'
                }
        self.place1 = {
                'title': 'My House',
                'description': 'It is nice and big and cozy and good!!',
                'price': 50.99,
                'latitude': 80.4,
                'longitude': 110.5
                }


class RouteUserTest(unittest.TestCase):
    
    def setUp(self):
        self.url = '/api/v1/users/'
        self.h = RequestSetUp().headers
        self.u1 = RequestSetUp().user1
        self.u2 = RequestSetUp().user2
        app = create_app()
        app.testing = True
        self.client = app.test_client()
        facade.user_repo = InMemoryRepository()

    def POST(self, data):
        return self.client.post(
            path=self.url,
            headers=self.h,
            data=json.dumps(data)
            )

    def test_POST(self):
        response = self.POST(self.u1).json
        self.assertEqual(response['first_name'], self.u1['first_name'])
        self.assertEqual(response['last_name'], self.u1['last_name'])
        self.assertEqual(response['email'], self.u1['email'])
        with self.assertRaises(KeyError):
            response['password']
        self.assertTrue(type(response['id']) is str)

        self.url = f'/api/v1/users/{response['id']}'
        response2 = self.client.get(path=self.url, headers=self.h).json
        self.assertEqual(response2['first_name'], self.u1['first_name'])
        self.assertEqual(response2['id'], response['id'])
   
    def test_GET(self):
        self.POST(self.u1)
        response = self.client.get(path=self.url, headers=self.h)
        self.assertEqual(len(response.json), 1)
   
    def test_wrong_email(self):
        self.u1['email'] = 'notgood'
        response = self.POST(self.u1)
        self.assertEqual(400, response.status_code)
        self.u1['email'] = 5
        response = self.POST(self.u1)
        self.assertEqual(400, response.status_code)
        self.u1['email'] = "Good@mail.com"
        response = self.POST(self.u1)
        response = self.POST(self.u1)
        self.assertEqual(400, response.status_code)


class RoutePlaceTest(unittest.TestCase):

    def setUp(self):
        self.h = RequestSetUp().headers
        self.u1 = RequestSetUp().user1
        self.u2 = RequestSetUp().user2
        self.p1 = RequestSetUp().place1
        app = create_app()
        app.testing = True
        self.client = app.test_client()
        facade.user_repo = InMemoryRepository()
        facade.place_repo = InMemoryRepository()
        self.create_users()
        self.url = 'api/v1/places/'
    
    def POST(self, data):
        return self.client.post(
            path=self.url,
            headers=self.h,
            data=json.dumps(data)
            )

    def create_users(self):
        self.url = 'api/v1/users/'
        r = self.POST(self.u1)
        self.u1['id'] = r.json['id']
        r = self.POST(self.u2)
        self.u2['id'] = r.json['id']
        self.url = 'api/v1/auth/login'
        r = self.POST({'email': self.u1['email'], 'password': self.u1['password']})
        self.u1['token'] = r.json['access_token']

    def test_POST(self):
        response = self.POST(self.p1)
        self.assertEqual(response.status_code, 401) # No JWT
        self.h['Authorization'] = f"Bearer {self.u1['token']}"
        response = self.POST(self.p1)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
