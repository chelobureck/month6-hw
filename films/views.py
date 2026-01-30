from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from films.models import FilmModel, GenresModel, DirectorModel
from films.serializers import FilmListSerializer, FilmDetailSerializer, FilmValidateSerializer, GenreSerializer, DirectorSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class DirectorViewSet(ModelViewSet):
    queryset = DirectorModel.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class GenreDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = GenresModel.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'id'

class GenreListAPIView(ListCreateAPIView):
    queryset = GenresModel.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination

class FilmListAPIView(ListCreateAPIView):
    queryset = FilmModel.objects.all()
    serializer_class = FilmListSerializer
    pagination_class = PageNumberPagination


# @api_view(['GET', 'POST'])
# def film_list_api_view(request):
#     """
#     получает фильмы с бд в виде QuerySet
#     переформатирует в Serialize
#     """
#     if request.method == 'GET':
#         films = FilmModel.objects.select_related('director').prefetch_related('reviews', 'genre').all()

#         data = FilmListSerializer(films, many=True).data

#         return Response(data=data, status=status.HTTP_200_OK)
#     if request.method == "POST":
#         serializer = FilmValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, 
#                             data=serializer.errors)
#         title = serializer.validated_data.get('title') # type: ignore
#         text = serializer.validated_data.get('text') # type: ignore
#         relaese_year = serializer.validated_data.get('relaese_year') # type: ignore
#         rating = serializer.validated_data.get('rating') # type: ignore
#         is_hit = serializer.validated_data.get('is_hit') # type: ignore
#         director_id = serializer.validated_data.get("director_id") # type: ignore
#         genres = serializer.validated_data.get("genres") # type: ignore

#         film = FilmModel.objects.create(
#             title=title,
#             text=text,
#             relaese_year=relaese_year,
#             rating=rating,
#             is_hit=is_hit,
#             director_id=director_id
#         )
#         film.genre.set(genres) # type: ignore

#         return Response(status=status.HTTP_201_CREATED, data=FilmDetailSerializer(film).data)


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, film_id):
    try:
        film = FilmModel.objects.get(id=film_id)
    except FilmModel.DoesNotExist:
        return Response(data={
            'error': 'film hot found!'
        }, status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data

        return Response(data=data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = FilmValidateSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        film.title = serializer.validated_data.get("title") # type: ignore
        film.text = serializer.validated_data.get("text") # type: ignore
        film.relaese_year = serializer.validated_data.get("relaese_year") # type: ignore
        film.rating = serializer.validated_data.get("rating") # type: ignore
        film.is_hit = serializer.validated_data.get("is_hit") # type: ignore
        film.director_id = serializer.validated_data.get("director_id") #type: ignore
        film.genre.set(serializer.validated_data.get("genres")) # type: ignore
        film.save()
        return Response(status=status.HTTP_201_CREATED, data=FilmDetailSerializer(film).data)
    
    if request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)