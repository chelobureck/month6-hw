from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUserModel
from users.serializers import UserCreateSerializer, UserAuthSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
