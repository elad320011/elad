import unittest
import requests

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:30007"

    def test_login_valid_credentials(self):
        # Test logging in with valid credentials
        data = {
            "email": "valid_user@example.com",
            "password": "valid_password"
        }
        response = requests.post(self.base_url + "/login", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.base_url + "/home")

    def test_login_invalid_credentials(self):
        # Test logging in with invalid credentials
        data = {
            "email": "invalid_user@example.com",
            "password": "invalid_password"
        }
        response = requests.post(self.base_url + "/login", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email or password.", response.content)

    def test_register_valid_data(self):
        # Test registering with valid data
        data = {
            "email": "new_user@example.com",
            "password": "new_password"
        }
        response = requests.post(self.base_url + "/register", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.base_url + "/login")

    def test_register_existing_user(self):
        # Test registering with an existing user
        data = {
            "email": "valid_user@example.com",
            "password": "valid_password"
        }
        response = requests.post(self.base_url + "/register", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A user with this email address already exists.", response.content)

    def test_home_page(self):
        # Test the home page
        response = requests.get(self.base_url + "/home")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"home page", response.content)

    def test_about_page(self):
        # Test the about page
        response = requests.get(self.base_url + "/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"contact page", response.content)

    def test_project_page(self):
        # Test the project page
        response = requests.get(self.base_url + "/project")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This Project", response.content)

if __name__ == '__main__':
    unittest.main()
