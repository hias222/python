import unittest
from ..app import app, db
import json

class TestCreateUserAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        payload = {'username': 'apiuser', 'email': 'apiuser@example.com'}
        response = self.client.post('/users', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['username'], 'apiuser')
        self.assertEqual(data['email'], 'apiuser@example.com')
        self.assertIn('guid', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_create_user_missing_fields(self):
        response = self.client.post('/users', data=json.dumps({'username': 'noemail'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()