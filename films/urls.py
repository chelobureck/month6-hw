from django.urls import path
from films.views import GenreDetailAPIView, film_list_api_view, film_detail_api_view, GenreListAPIView, DirectorViewSet

urlpatterns = [
    path("", film_list_api_view),
    path("<int:film_id>/", film_detail_api_view),
    path("genres/", GenreListAPIView.as_view()),
    path('genres/<int:id>', GenreDetailAPIView.as_view()),
    path('directors/', DirectorViewSet.as_view({"get": "list", "post": "create"})),
    path("directors/<int:id>", DirectorViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}))
]
