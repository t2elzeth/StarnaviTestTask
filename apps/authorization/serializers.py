from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]

    def create(self, validated_data: dict):
        """Create user"""
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    auth_token = serializers.CharField(source="key", read_only=True)

    default_error_messages = {
        "invalid_credentials": "Unable to log in with provided credentials.",
        "inactive_account": "User account is disabled.",
    }

    def validate(self, data):
        password = data.get("password")
        params = {"email": data.get("email")}
        self.user = authenticate(
            request=self.context.get("request"), password=password, **params
        )
        if not self.user:
            self.user = User.objects.get_object_or_none(**params)
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return data
        self.fail("invalid_credentials")

    def create(self, validated_data):
        return self.user.login()


class UserActivitySerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    last_active = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    class Meta:
        model = User
        fields = ["last_login", "last_active"]
