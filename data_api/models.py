# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actors(models.Model):
    name = models.CharField(max_length=256)
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actors'


class ActorsMovies(models.Model):
    imdb_id = models.CharField(max_length=256)
    actor = models.ForeignKey(Actors, models.DO_NOTHING)
    movies = models.ForeignKey('Movies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actors_movies'


class Directors(models.Model):
    name = models.CharField(max_length=256)
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'directors'


class DirectorsMovies(models.Model):
    imdb_id = models.CharField(max_length=256)
    director = models.ForeignKey(Directors, models.DO_NOTHING)
    movies = models.ForeignKey('Movies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'directors_movies'


class Genres(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'genres'


class GenresMovies(models.Model):
    genre = models.ForeignKey(Genres, models.DO_NOTHING)
    imdb_id = models.CharField(max_length=256)
    movies = models.ForeignKey('Movies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres_movies'


class Movies(models.Model):
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

    class Meta:
        managed = False
        db_table = 'movies'


class Scenarists(models.Model):
    name = models.CharField(max_length=256)
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenarists'


class ScenaristsMovies(models.Model):
    imdb_id = models.CharField(max_length=256)
    scenarist = models.ForeignKey(Scenarists, models.DO_NOTHING)
    movies = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenarists_movies'
