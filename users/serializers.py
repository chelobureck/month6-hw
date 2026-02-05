from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from users.models import CustomUserModel
from common.validators import validated_birthday


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token['birthday'] = user.birthday
        return token


class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
    phone_num = serializers.CharField()
    birthday = serializers.DateField()

    def validate_username(self, username):
        try:
            CustomUserModel.objects.get(username=username)
            return ValidationError("User already exists!")
        except CustomUserModel.DoesNotExist:
            return username
    


    def validate_phone_num(self, phone_num):
        if phone_num[:4] != '+996':
            raise ValueError("Phone num incorrect")
        return phone_num
    def create(self, validated_data):
        return CustomUserModel.objects.create_user(**validated_data) # type: ignore