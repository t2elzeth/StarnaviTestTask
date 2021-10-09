from authorization.models import User
from authorization.tests.factory import UserFactory
from django.test import TestCase
from rest_framework.authtoken.models import Token


class TestCreateUser(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory.create()

    def test_defaults(self):
        """Test initial values on user creation"""

        self.assertTrue(self.user.is_active, "User is not active by default")
        self.assertFalse(self.user.is_staff, "User must not be staff by default")
        self.assertIsNone(self.user.last_login, "User has not logged in yet")


class TestCreateSuperuser(TestCase):
    def setUp(self) -> None:
        self.superuser: User = User.objects.create_superuser(
            email="superuser@gmail.com", password="admin12345"
        )

    def test_defaults(self):
        """Test default values for superuser"""

        self.assertTrue(self.superuser.is_active, "Superuser must be active by default")
        self.assertTrue(self.superuser.is_staff, "Superuser must be staff by default")
        self.assertTrue(
            self.superuser.is_superuser,
            "Superuser must have field `is_superuser` set to True",
        )
        self.assertIsNone(self.superuser.last_login, "Superuser has not logged in yet")


class TestUserAuthorizationMethods(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory.create()
        self.token = self.user.login()

    def test_login(self):
        self.assertIsInstance(
            self.token, Token, ".login() method doesn't return a token instance"
        )
        self.assertEqual(
            self.token.user.id, self.user.id, "Token is created for the different user"
        )
        self.assertIsNotNone(self.user.last_login)

    def test_logout(self):
        self.user.logout()

        # Check if token still exists
        # noinspection PyTypeChecker
        self.assertRaises(Token.DoesNotExist, self.token.refresh_from_db)
