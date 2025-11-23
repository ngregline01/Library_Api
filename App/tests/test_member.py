from App.blueprint import create_app
from App.blueprint.models import db
import unittest

class TestMember(unittest.TestCase):
    def setUp(self):
        self.New_app = create_app("TestingConfig")
        with self.New_app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.New_app.test_client()

    def test_create_member(self):
        member_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1900-01-01",
            "password": "123"
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):
        member_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"  
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    