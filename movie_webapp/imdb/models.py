from django.db import models

class Movie(models.Model):

    id_movie = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=256, blank=True, null=True)
    img_url = models.CharField(max_length=256, blank=True, null=True)
    desc_fr = models.TextField(blank=True, null=True)
    desc_en = models.TextField(blank=True, null=True)
    anecdote = models.TextField(blank=True, null=True)
    rating_content = models.CharField(max_length=256, blank=True, null=True)
    year = models.CharField(max_length=256, blank=True, null=True)
    imdb_int = models.IntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    recommendation_rate = None

    actors_matching = models.ManyToManyField(
        'Actor',
        through = 'ActorsMovies',

    )

    directors_matching = models.ManyToManyField(
        'Director',
        through = 'DirectorsMovies',

    )

    genres_matching = models.ManyToManyField(
        'Genre',
        through = 'GenresMovies',
    )

    @property
    def actors(self):

        actors_list = self.actors_matching.all()

        

        serializable_actors = [
            {
                "id":actor.id,
                "name":actor.name
            }
            for actor in actors_list
        ]
        return serializable_actors

    @property
    def directors(self):

        directors_list = self.directors_matching.all()

        serializable_directors = [
            {
                "id":director.id,
                "name":director.name
            }
            for director in directors_list
        ]
        return serializable_directors
    
    @property
    def genres(self):

        genres_list = self.genres_matching.all()

        serializable_genres = [
            {
                "id":genre.id,
                "name":genre.name
            }
            for genre in genres_list
        ]
        return serializable_genres
    
    class Meta:
        managed = False
        db_table = 'movies'
    
    def set_rec_rate(self,rate:float):
        self.recommendation_rate = rate

    def __str__(self) -> str:
        return self.titre


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)
    movies_matching = models.ManyToManyField(
        'Movie',
        through = 'ActorsMovies',

    )

    @property
    def movies(self):

        movies_list = self.movies_matching.all()

        serializable_movies = [
            {
                "id":movie.id_movie,
                "titre":movie.titre,
                "img_url":movie.img_url
            }
            for movie in movies_list
        ]
        return movies_list

    class Meta:
        managed = False
        db_table = 'actors'
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class ActorsMovies(models.Model):
    imdb_id = models.CharField(max_length=256)
    actor = models.ForeignKey(Actor, models.DO_NOTHING)
    movies = models.ForeignKey(Movie, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actors_movies'


class Director(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)
    movies_matching = models.ManyToManyField(
        'Movie',
        through = 'DirectorsMovies',

    )

    @property
    def movies(self):

        movies_list = self.movies_matching.all()

        serializable_movies = [
            {
                "id":movie.id_movie,
                "titre":movie.titre,
                "img_url":movie.img_url
            }
            for movie in movies_list
        ]
        return movies_list

    class Meta:
        managed = False
        db_table = 'directors'
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class DirectorsMovies(models.Model):
    imdb_id = models.CharField(max_length=256)
    director = models.ForeignKey(Director, models.DO_NOTHING)
    movies = models.ForeignKey(Movie, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'directors_movies'


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    movies_matching = models.ManyToManyField(
        'Movie',
        through = 'GenresMovies',

    )

    @property
    def movies(self):

        movies_list = self.movies_matching.all()

        serializable_movies = [
            {
                "id":movie.id_movie,
                "titre":movie.titre,
                "img_url":movie.img_url
            }
            for movie in movies_list
        ]
        return movies_list

    class Meta:
        managed = False
        db_table = 'genres'
    
    def __str__(self):
        return self.name


class GenresMovies(models.Model):
    
    genre = models.ForeignKey(Genre, models.DO_NOTHING)
    imdb_id = models.CharField(max_length=256)
    movies = models.ForeignKey(Movie, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres_movies'




class Scenarist(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenarists'
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class ScenaristsMovies(models.Model):
    imdb_id = models.CharField(max_length=256)
    scenarist = models.ForeignKey(Scenarist, models.DO_NOTHING)
    movies = models.ForeignKey(Movie, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenarists_movies'