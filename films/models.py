from django.db import models



class DirectorModel(models.Model):
    fio = models.CharField(max_length=255)
    brithday = models.DateField()

    def __str__(self) -> str:
        return f'{self.fio}'


class GenresModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class FilmModel(models.Model):
    director = models.ForeignKey(DirectorModel, on_delete=models.CASCADE, null=True)
    genre = models.ManyToManyField(GenresModel, blank=True)
    title = models.CharField(max_length=255)
    text = models.CharField(null=True, blank=True)
    rating = models.FloatField()
    relaese_year = models.IntegerField()
    is_hit = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    @property
    def genre_names(self):
        return [i.name for i in self.genre.all()]
    
class ReviewModel(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=((i, i) for i in range(1, 11)), default=7) # type: ignore
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self) -> str:
        return f'{self.text}'
    

class TestModel(models.Model):
    test = models.CharField()