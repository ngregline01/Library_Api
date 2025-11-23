from App.blueprint import create_app
from App.blueprint.models import db, Member
from datetime import datetime
from App.utils.util import encode_token
import unittest


class TestMember(unittest.TestCase):

    def setUp(self):
        self.New_app = create_app('TestingConfig')
        #Member needs to be added as dummy because you need a member in order to login
        self.member = Member(name="test_user", email="test@email.com", DOB=datetime.strptime("1900-01-01", "%Y-%m-%d").date() , password='test')#creates an instance of member
        with self.New_app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.member) #add the member dummy that was created
            db.session.commit()#saves or commit the member on the database
        self.token = encode_token(1)
        self.client = self.New_app.test_client()

#previous test cases

    def test_login_member(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'Success')
        return response.json['token']


    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/members/login', json=credentials) #give the posting route and type
        self.assertEqual(response.status_code, 400) #what major thing you expect based on your test case
        self.assertEqual(response.json['message'], 'Invalid email or password!')

    def test_update_member(self):
        update_payload = {
            "name": "Peter",
            "phone": "",
            "email": "",
            "password": ""
        }

        headers = {'Authorization': "Bearer " + self.test_login_member()}

        response = self.client.put('/members/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'test@email.com')