from django.urls import path
from users.views import autherization_api_view, registration_api_view  

urlpatterns = [
    path('registration/', registration_api_view), # type: ignore
    path('authorization/', autherization_api_view)
]
