from django.contrib import admin
from films.models import DirectorModel, FilmModel, GenresModel, ReviewModel

@admin.register(FilmModel)
class FilmModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'director', 'rating'] 

@admin.register(GenresModel)
class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'name']

@admin.register(DirectorModel)
class DirectorModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'fio', 'brithday']

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'film', 'stars']
