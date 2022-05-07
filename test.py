from qair import app
import unittest

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
        
    def test_base_route(self):
        client = app.test_client(self)
        url = '/admins/dashboard'
        response = client.get(url)
        assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()