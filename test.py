from qair import app
import unittest

from qair.reservations.routes import payment

class QairTestCase(unittest.TestCase):
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/users/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_register(self):
        tester = app.test_client(self)
        response = tester.get('/users/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_forget_password(self):
        tester = app.test_client(self)
        response = tester.get('/users/forget_password', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_view_flights(self):
        tester = app.test_client(self)
        response = tester.get('/company/view-flight', content_type='html/text')
        self.assertEqual(response.status_code, 302)
        
    def test_create_route(self):
        tester = app.test_client(self)
        response = tester.get('/company/create-route', content_type='html/text')
        self.assertEqual(response.status_code, 302)
    
    def test_change_photos(self):
        tester = app.test_client(self)
        response = tester.get('/profiles/change-photos', content_type='html/text')
        self.assertEqual(response.status_code, 302)
        
    def test_notifications(self):
        tester = app.test_client(self)
        response = tester.get('/notifications/notifications', content_type='html/text')
        self.assertEqual(response.status_code, 404)
        

if __name__ == "__main__":
    unittest.main()