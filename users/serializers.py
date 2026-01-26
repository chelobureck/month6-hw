from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import CustomUserModel


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            CustomUserModel.objects.get(username=username)
        except CustomUserModel.DoesNotExist:
            return username
        return ValidationError("User already exists!")
    