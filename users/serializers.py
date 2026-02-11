from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from users.models import CustomUserModel
from common.validators import validated_birthday
from django.core.cache import cache
from datetime import datetime
import uuid

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
            raise ValidationError("User already exists!")
        except CustomUserModel.DoesNotExist:
            return username
    
    def validate_phone_num(self, phone_num):
        if phone_num[:4] != '+996':
            raise ValidationError("Phone num incorrect")
        return phone_num
    
    def validate_birthday(self, birthday):
        return validated_birthday(birthday=birthday)
    
    def create(self, validated_data):
        cache_key = f"user_registration:{validated_data['username']}"
        cache.set(cache_key, {
            'username': validated_data['username'],
            'phone_num': validated_data['phone_num'],
            'birthday': str(validated_data['birthday']),
            'password': validated_data['password']
        }, timeout=300)
        
        return validated_data


class UserVerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    
    def validate_username(self, username):
        cache_key = f"user_registration:{username}"
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            raise ValidationError("Registration data not found or expired")
        
        return username
    
    def verify_and_save(self, username, is_staff=False):
        cache_key = f"user_registration:{username}"
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            raise ValidationError("Registration data not found or expired")
        
        if is_staff:
            birthday = datetime.strptime(cached_data['birthday'], '%Y-%m-%d').date()
            age = (datetime.now().date() - birthday).days // 365
            
            if age < 18:
                raise ValidationError("Staff must be at least 18 years old")
        
        user = CustomUserModel.objects.create_user(  # type: ignore
            username=cached_data['username'],
            password=cached_data['password'],
            phone_num=cached_data['phone_num'],
            birthday=cached_data['birthday'],
            is_staff=is_staff
        )
        
        cache.delete(cache_key)
        return user