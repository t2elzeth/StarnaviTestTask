from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestSignup(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("user-signup")
        self.first_name = "First"
        self.last_name = "Last"
        self.email = "useremail@gmail.com"
        self.password = "admin12345"

    def test_signup_using_full_valid_data(self):
        payload = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_using_required_data(self):
        payload = {"email": self.email, "password": self.password}

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_without_email(self):
        payload = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_without_password(self):
        payload = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_empty_data(self):
        payload = {}

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
