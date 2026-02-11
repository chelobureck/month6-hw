from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUserModel
from users.serializers import UserCreateSerializer, UserAuthSerializer, CustomTokenObtainPairSerializer, UserVerifySerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken



class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class VerifyRegistrationAPIView(CreateAPIView):
	serializer_class = UserVerifySerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		is_staff = request.data.get('is_staff', False)
		user = serializer.verify_and_save(
			username=serializer.validated_data['username'],
			is_staff=is_staff
		)
		
		refresh = RefreshToken.for_user(user)
		return Response({
			'access': str(refresh.access_token),
			'refresh': str(refresh),
			'user_id': user.id
		}, status=status.HTTP_201_CREATED)
