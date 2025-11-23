from Library_API.New_app import create_app
from App.blueprint.models import db
import unittest

class TestMember(unittest.TestCase): #TestCase is given by python to allow you to test stuff
    def setUp(self): #this makes each test to be tested seperately
        self.New_app = create_app("TestingConfig") #creates fresh simulation of new routes
        with self.New_app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.New_app.test_client() #create test client to to simulate request

    def test_create_member(self):
        #defines the payload or data being sent
        member_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1900-01-01",
            "password": "123"
        }
        
        #defines the route and the type of method, also giving the payload from the one init above
        response = self.client.post('/', json=member_payload) #sends the request
        self.assertEqual(response.status_code, 201)#What is expected when your code is tested, in this case the status code
        self.assertEqual(response.json['name'], "John Doe") #Major thing that is expected, in this case name