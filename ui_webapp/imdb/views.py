from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.db import connection
from django.core.paginator import Paginator
import requests, json
from .forms import RecommendationForm, InferenceForm
from .recom import request_recommendation, parse_recommendation

#---HOME--------------------------------------------------------------------------------------------------------------

@csrf_protect
@require_http_methods(["GET"])
def home(request):

    # id for the home page
    ids = [32994, 38683, 37341,33907]
    movies = []
    for id_movie in ids:
        movie = Movie.objects.filter(id_movie=id_movie)
        movies.append(movie[0])

    # actor for the home page 
    ids = [1357, 1183, 1803, 1442]
    actors = []
    for id_actor in ids:
        actor = Actor.objects.filter(id=id_actor)
        actors.append(actor[0])

    return render(
        request,
        'imdb/home.html',
        {
            'movies':movies,
            'actors':actors

        }
    )

#---RECOMMENDATIONS---------------------------------------------------------------------------------------------------

#---1. BY TITLE ---
@csrf_protect
@login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def get_recommendations(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RecommendationForm(request.POST)

        # whether the title is in the list or not
        # check whether it's valid:
        if form.is_valid():
 
            data_dic = json.loads(requests.post(url="http://localhost:8000/imdb/rec/",json=form.cleaned_data).text)

            # if movie requested not in db
            if data_dic['results'][0]['Recommendations'][0]['Rec_1']['title']== 'unknown_title':
                notinlist=True
                # redirects it to default page
                return render(request,'imdb/get_rec.html', {
                    'notinlist':notinlist,
                    'form':form
                }) 
            
            
            
            movie_form = Movie.objects.get(titre=form.cleaned_data['titles'])

            
            # getting imdb id from those films
            imdb_ids = []
            taux_recs = []
            
            j = 0
            i = 1
            while j < 5:
                
                imdb_id = data_dic['results'][0]['Recommendations'][j]['Rec_'+str(i)]['imdb_id']
                imdb_ids.append(imdb_id)
                taux_rec = data_dic['results'][0]['Recommendations'][j]['Rec_'+str(i)]['rec rate']
                taux_recs.append(taux_rec)
                i+=1
                j+=1

            movies = []

            i = 0
            for rec_imdb_id in imdb_ids:
                movie = Movie.objects.get(imdb_int=rec_imdb_id)
                movie.set_rec_rate(taux_recs[i])
                movies.append(movie)
                i+=1

            


            return render(request,
                          "imdb/display_rec.html", 
                          {"recommendations" :data_dic, 
                           'movie_form':movie_form,
                           'movies':movies,
                           'taux_recs':taux_recs,
                           })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecommendationForm()

    return render(request, "imdb/get_rec.html", {"form": form})

#---2. BY DESC ---
@csrf_protect
@login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def get_recommendations_by_desc(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InferenceForm(request.POST)

        # whether the title is in the list or not
        # check whether it's valid:
        if form.is_valid():

            data_dic = json.loads(requests.post(url="http://localhost:8000/imdb/rec/desc",json=form.cleaned_data).text)
                                 
            # getting imdb id from those films
            imdb_ids = []
            taux_recs = []
            
            j = 0
            i = 1
            while j < 5:
                
                imdb_id = data_dic['results'][0]['Recommendations'][j]['Rec_'+str(i)]['imdb_id']
                imdb_ids.append(imdb_id)
                taux_rec = data_dic['results'][0]['Recommendations'][j]['Rec_'+str(i)]['rec rate']
                taux_recs.append(taux_rec)
                i+=1
                j+=1

            movies = []

            i = 0
            for rec_imdb_id in imdb_ids:
                movie = Movie.objects.get(imdb_int=rec_imdb_id)
                movie.set_rec_rate(taux_recs[i])
                movies.append(movie)
                i+=1

            


            return render(request,
                          "imdb/display_rec.html", 
                          {"recommendations" :data_dic, 
                           'movies':movies,
                           'taux_recs':taux_recs,
                           })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InferenceForm()

    return render(request, "imdb/get_rec.html", {"form": form})
    

#---MOVIES------------------------------------------------------------------------------------------------------------

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_one_movie(request,id_movie):

    movie = get_object_or_404(Movie,id_movie=id_movie)

    title_type_list = {"titles":movie.titre}

    data_dic = request_recommendation(title_type_list)

    movies_recom = parse_recommendation(data_dic)


    # print(movies)
    return render(
        request,
        'imdb/movie.html',
        {
            'movie':movie,
            'movies_recom':movies_recom
        }
    )

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_movies(request):
    movies = Movie.objects.all()
    return render(
        request,
        'imdb/movies.html',
        {
            'movies':movies
        }
    )

#---ACTORS------------------------------------------------------------------------------------------------------------------

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_one_actor(request,actor_id):
    # DISPLAY ALL THE FILM THE ACTOR HAS PLAYED IN 
    actor = get_object_or_404(Actor,id=actor_id)

    actor_movies = actor.movies
    return render(request,
                  'imdb/actor.html',
                  {'actor':actor})


@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_actors(request):
    actors = Actor.objects.all()
    return render(
        request,
        'imdb/actors.html',
        {
            'actors':actors
        }
    )

#---DIRECTORS------------------------------------------------------------------------------------------------------------

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_one_director(request,actor_id):
    # TO EDIT : DISPLAY ALL THE FILM DIRECTED BY IT
    director = get_object_or_404(Director,id=actor_id)
    director_movies = director.movies

    return render(request,
                  'imdb/director.html',
                  {
                      'director':director
                  })

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_directors(request):
    directors = Director.objects.all()
    return render(
        request,
        'imdb/directors.html',
        {
            'directors':directors
        }
    )

#---GENRES----------------------------------------------------------------------------------------------------------------

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_one_genre(request,actor_id):
    #TO EDIT : display all the films that has the genre
    genre = get_object_or_404(Genre,id=actor_id)

    movies_p = Paginator(genre.movies,20)
    return render(request,
                  'imdb/genre.html',
                  {
                      'genre':genre,
                      'movies' : movies_p.page(1).object_list,
                  })

@csrf_protect
@require_http_methods(["GET"])
@login_required(login_url='/login')
def get_genres(request):
    genres = Genre.objects.all()
    return render(
        request,
        'imdb/genres.html',
        {
            'genres':genres
        }
    )