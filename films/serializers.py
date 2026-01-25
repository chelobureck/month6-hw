from rest_framework import serializers
from films.models import DirectorModel, FilmModel, GenresModel
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorModel
        fields = 'id fio'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenresModel
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genre = serializers.SerializerMethodField()


    class Meta:
        model = FilmModel
        fields = "id title director genre rating is_hit".split()

        # depth = 1 #самый легкий способ

    def get_genre(self, film):
        return film.genre_names


class FilmDetailSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    
    class Meta:
        model = FilmModel
        fields = "__all__"

class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=255)
    text = serializers.CharField(required=False)
    relaese_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField(default=True)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            DirectorModel.objects.get(id=director_id)
        except DirectorModel.DoesNotExist:
            raise ValidationError('Director is not exist')
        return director_id
    
    def validate_genres(self, genres):
        genres_from_db = GenresModel.objects.filter(id__in=genres)
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genres is not exist')
        return genres