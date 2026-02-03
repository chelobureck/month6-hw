from django.urls import path
from users.views import  RegisterAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view()),
    
]
