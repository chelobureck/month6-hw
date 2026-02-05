from django.urls import path
from users.views import RegisterAPIView
from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view()),
    path('auth/google/', GoogleLoginAPIView.as_view()),
]
