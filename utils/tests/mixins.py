from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserDataMixin:
    USER_DATA = {
        "email": "testuser@gmail.com",
        "password": "admin",
        "first_name": "Test",
        "last_name": "User",
    }
    SUPERUSER_DATA = {
        "email": "testsuperuser@gmail.com",
        "password": "admin",
        "first_name": "Test",
        "last_name": "User",
    }


class CreateUserAndSuperuserMixin(UserDataMixin):
    def setUp(self):
        self.user = User.objects.create_user(**self.USER_DATA)
        self.superuser = User.objects.create_superuser(**self.SUPERUSER_DATA)
        self.supertoken = self.superuser.login()


class SetAuthCredentialsMixin:
    AUTHENTICATION_CREDENTIALS = "Token {}"

    def set_credentials(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.AUTHENTICATION_CREDENTIALS.format(token.key)
        )
