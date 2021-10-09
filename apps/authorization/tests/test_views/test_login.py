import faker
from authorization.tests.factory import UserFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestLogin(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("token-auth-login")
        self.fake = faker.Faker()

        self.email = self.fake.email()
        self.password = self.fake.password()
        self.user = UserFactory.create(email=self.email, password=self.password)

    def test_login_with_full_valid_data(self):
        payload = {"email": self.email, "password": self.password}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("auth_token", response.data)
        self.assertTrue(Token.objects.filter(key=response.data["auth_token"]).exists())

    def test_login_with_invalid_email(self):
        payload = {"email": self.fake.email(), "password": self.password}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_password(self):
        payload = {"email": self.email, "password": self.fake.password()}

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_data(self):
        payload = {}

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 2)
