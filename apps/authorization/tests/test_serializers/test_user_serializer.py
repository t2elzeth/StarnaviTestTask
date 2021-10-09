from authorization.models import User
from authorization.serializers import UserSerializer
from authorization.tests.factory import UserFactory
from django.test import TestCase


class TestUserSerializerCreate(TestCase):
    def setUp(self) -> None:
        self.first_name = "First name"
        self.last_name = "Last name"
        self.email = "myusermail@gmail.com"
        self.password = "admin12345"

    def test_create_user_with_full_valid_data(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertFalse(serializer.errors)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.email, self.email)

    def test_create_with_only_required_data(self):
        data = {"email": self.email, "password": self.password}

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertFalse(serializer.errors)
        self.assertIsNotNone(user.id)
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)
        self.assertEqual(user.email, self.email)

    def test_create_without_password(self):
        """
        Test when trying to create without specifying password
        """
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
        self.assertEqual(len(serializer.errors.keys()), 1)
        self.assertIn("password", serializer.errors)

    def test_create_without_email(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
        self.assertEqual(len(serializer.errors.keys()), 1)
        self.assertIn("email", serializer.errors)

    def test_create_with_empty_data(self):
        data = {}

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
        self.assertEqual(len(serializer.errors.keys()), 2)
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)


class TestUserSerializerSerializedData(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory.create()

    def test_serializer_user_instance(self):
        serialized_data = UserSerializer(instance=self.user).data

        expected_data = {
            "id": self.user.id,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
        }

        self.assertIsInstance(serialized_data, dict)
        self.assertTrue(serialized_data)
        self.assertEqual(serialized_data, expected_data)
