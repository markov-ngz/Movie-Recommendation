from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns

from . import views 

app_name = 'imdb'

urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='movies'),
    path('movies/<int:pk>', views.MovieDetail.as_view()),
    path('actors/', views.ActorList.as_view()),
    path('actors/<int:pk>',views.ActorDetail.as_view()),
    path('directors/', views.DirectorList.as_view()),
    path('directors/<int:pk>',views.DirectorDetail.as_view()),
    path('genres/', views.GenreList.as_view()),
    path('genres/<int:pk>',views.GenreDetail.as_view()),
    path('movies/request', views.MovieRequest.as_view(), name='movie_request')
]

urlpatterns = format_suffix_patterns(urlpatterns)