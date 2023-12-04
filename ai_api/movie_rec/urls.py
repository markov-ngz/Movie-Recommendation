from django.urls import path

from . import views

app_name= "movie_rec"
urlpatterns = [
    path("rec/random",views.recommendation_random, name="recommendation_random"),
    path("rec/",views.recom_one, name="recom_one"),
    path("rec/desc",views.recom_one_by_desc,name="recom_one_by_desc")
]