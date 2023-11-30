from django.contrib.auth.models import User
from rest_framework import serializers
from imdb.models import *

class ActorSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Actor
        fields = ('id','firstname','lastname','movies')

class DirectorSerializer(serializers.ModelSerializer):
        
    class Meta : 
        model = Director
        fields = ('id','name','movies')

class GenresSerializer(serializers.ModelSerializer):
        
    class Meta : 
        model = Genre
        fields = ('id','name','movies')

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id_movie',
                  'created_at',
                  'titre',
                  'img_url',
                  'desc_fr',
                  'desc_en',
                  'anecdote',
                  'rating_count',
                  'rating_content',
                  'year',
                  'imdb_int',
                  'actors',
                  'directors',
                  'genres',
                  ]



##############################################################################################
#LEGACY MODELS
#
# class ActorSerializer(serializers.ModelSerializer):

#     class Meta : 
#         model = Actor
#         fields = ('id','name',)

# class DirectorSerializer(serializers.ModelSerializer):
        
#     class Meta : 
#         model = Director
#         fields = ('id','name',)

# class ScenaristSerializer(serializers.ModelSerializer):
        
#     class Meta : 
#         model = Scenarist
#         fields = ('id','name',)

# class MovieSerializer(serializers.ModelSerializer):
    
#     actors = ActorSerializer(many= True)
#     directors = DirectorSerializer(many= True)
#     scenarists = ScenaristSerializer(many= True)

#     class Meta:
#         model = Movie
#         fields = ['id',
#                   'titre',
#                   'img_url',
#                   'description',
#                   'description_en',
#                   'anecdote',
#                   'rating_count',
#                   'rating_content',
#                   'year',
#                   'imdb_id',
#                   'actors',
#                   'directors',
#                   'scenarists']
    
#     # def get_or_create_actors(self,actors):
#     #     """
        
#     #     """
#     #     actor_ids = []
#     #     for actor in actors:
#     #         actor_instance , created = Actor.objects.get_or_create(pk = actor.get('id'), defaults = actor)
#     #         actor_ids.append(actor_instance.pk)
#     #     return actor_ids
    
#     # def create_or_update_actors(self,actors):
#     #     """
        
#     #     """
#     #     actor_ids = []
#     #     for actor in actors:
#     #         actor_instance , created = Actor.objects.update_or_create(pk = actor.get('id'), defaults = actor)
#     #         actor_ids.append(actor_instance.pk)
#     #     return actor_ids
    
#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
#         actors = validated_data.pop('actors',[])
#         directors = validated_data.pop('directors',[])
#         scenarists = validated_data.pop('scenarists',[])
#         movie = Movie.objects.create(**validated_data)
#         # movie.actors.set(self.get_or_create_actors(actors))
#         for actor_data in actors:
#             actor, created = Actor.objects.get_or_create(**actor_data)
#             movie.actors.add(actor)
        
#         for director_data in directors:
#             director, created = Director.objects.get_or_create(**director_data)
#             movie.directors.add(director)

#         for scenarist_data in scenarists:
#             scenarist, created = Scenarist.objects.get_or_create(**scenarist_data)
#             movie.scenarists.add(scenarist)

#         return movie
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         """
#         # actors = validated_data.pop('actors',[])
#         # instance.actors.set(self.create_or_update_actors(actors))

#         instance.titre = validated_data.get('titre', instance.titre)
#         instance.image_url = validated_data.get('image_url', instance.image_url)
#         instance.description = validated_data.get('description', instance.description)
#         instance.description_en = validated_data.get('description_en', instance.description_en)
#         instance.anecdote = validated_data.get('anecdote', instance.anecdote)
#         instance.rating_count = validated_data.get('rating_count', instance.rating_count)
#         instance.rating_content = validated_data.get('rating_content', instance.rating_content)
#         instance.year = validated_data.get('year', instance.year)
#         instance.imdb_id = validated_data.get('imdb_id', instance.imdb_id)

#         actors_data = validated_data.get('actors', instance.actors.all())
#         instance.actors.clear()  # Supprime les acteurs existants pour les remplacer

#         for actor_data in actors_data:
#             actor, created = Actor.objects.get_or_create(**actor_data)
#             instance.actors.add(actor)
        
        
#         directors_data = validated_data.get('directors', instance.directors.all())
#         instance.directors.clear()  # Supprime les acteurs existants pour les remplacer

#         for director_data in directors_data:
#             director, created = Director.objects.get_or_create(**director_data)
#             instance.directors.add(director)
        
#         scenarists_data = validated_data.get('scenarists', instance.scenarists.all())
#         instance.scenarists.clear()  # Supprime les acteurs existants pour les remplacer

#         for scenarist_data in scenarists_data:
#             scenarist, created = Scenarist.objects.get_or_create(**scenarist_data)
#             instance.scenarists.add(scenarist)
            
#         instance.save()
#         return instance
    