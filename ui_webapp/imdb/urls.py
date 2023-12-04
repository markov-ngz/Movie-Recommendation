from django.urls import path 

from .views import * 

app_name = 'imdb'

urlpatterns = [
    path('movies/<int:id_movie>',get_one_movie, name='one_movie'),
    path('movies',get_movies,name='all_movies'),
    path('actors/<int:actor_id>',get_one_actor, name='one_actor'),
    path('actors/',get_actors,name='all_actors'),
    path('directors/<int:actor_id>',get_one_director, name='one_directors'),
    path('directors/',get_directors,name='all_directors'),
    path('genres/<int:actor_id>',get_one_genre, name='one_genre'),
    path('genres/',get_genres,name='all_genres'),
    path('rec/',get_recommendations,name='get_rec'),
    path('rec/desc',get_recommendations_by_desc,name='get_rec_by_desc'),
    path('', home, name='home')
    # path('new/',views.new, name='new'),
    # path('<int:pk>/delete/', views.delete, name='delete'),
    # path('<int:pk>/edit/', views.edit, name='edit'),
    # path('', views.items, name='items')
]