import json
import requests
from .models import Movie
def request_recommendation(form_cleaned_data:dict)->dict:
    """
    Send a request to get the recommendations for the given titles
    """
    return json.loads(requests.post(url="http://localhost:8000/imdb/rec/",json=form_cleaned_data).text)

def parse_recommendation(data_dic:dict)->list:
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
    
    return movies