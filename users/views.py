from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUserModel
from users.serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username'] # type: ignore
    password = serializer.validated_data['password'] # type: ignore

    user = CustomUserModel.objects.create_user(username=username, password=password) # type: ignore

    return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id}) # type: ignore


@api_view(['POST'])
def autherization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data) # type: ignore
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(status=status.HTTP_200_OK, data={"key": token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
