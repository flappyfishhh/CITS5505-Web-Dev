import unittest
from app import app, db
from app.model import User, Tag, Request, Response, post_tag

class BasicTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        with app.app_context():
            user = User(user_name='testuser', email='test@example.com')
            user.set_password('testpassword')
            self.assertFalse(user.check_password('wrongpassword'))
            self.assertTrue(user.check_password('testpassword'))
            db.session.add(user)
            db.session.commit()

    def test_user_repr(self):
        with app.app_context():
            user = User(user_id=1, user_name='testuser')
            self.assertEqual(str(user), '<User 1,testuser>')

    def test_create_request_and_response(self):
        with app.app_context():
            user = User(user_name='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            request = Request(request_title="My Request", request_content="This is a test request", author=user)
            db.session.add(request)
            db.session.commit()

            response = Response(response_content="This is a test response", contributor=user, request_id=request.request_id)
            db.session.add(response)
            db.session.commit()

            self.assertIn(response, user.response_contributor)
            self.assertEqual(response.request_id, request.request_id)

    def test_delete_request(self):
        with app.app_context():
            user = User(user_name='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            request = Request(request_title="My Request", request_content="This is a test request", author=user)
            db.session.add(request)
            db.session.commit()

            db.session.delete(request)
            db.session.commit()

            self.assertIsNone(db.session.get(Request, request.request_id))

    def test_delete_response(self):
        with app.app_context():
            user = User(user_name='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            request = Request(request_title="My Request", request_content="This is a test request", author=user)
            db.session.add(request)
            db.session.commit()

            response = Response(response_content="This is a test response", user_id=user.user_id, request_id=request.request_id)
            db.session.add(response)
            db.session.commit()

            db.session.delete(response)
            db.session.commit()

            self.assertIsNone(db.session.get(Response, response.response_id))

if __name__ == '__main__':
    unittest.main()
