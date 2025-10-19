from auth import app
import unittest

class FkasketTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_login_success(self):
        response = self.client.post('/login', json={
            "username": "admin",
            "password": "secret"  # Зверни увагу на пароль "secret"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Login successful"})

    def test_login_failure(self):
        response = self.client.post('/login', json={
            "username": "wrong",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Invalid credentials"})

if __name__ == '__main__':
    unittest.main()
