from django.urls import path
from users.views import RegisterAPIView, VerifyRegistrationAPIView
from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view()),
    path('registration/verify/', VerifyRegistrationAPIView.as_view()),
    path('auth/google/', GoogleLoginAPIView.as_view()),
]
