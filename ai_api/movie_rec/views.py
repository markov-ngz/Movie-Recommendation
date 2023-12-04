
import pandas as pd
import numpy as np
import math
import re
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .recom import *
from .bert import *
from rest_framework.decorators import api_view

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def recommendation_random(request):
    """
    From a GET a request at this endpoint 
    Return a JSON Response with the recommendations for X movies ( default 5)
    """
    #----1. Check request -----------------------------------------------------------------------------------------

    # if the query parameter is not defined
    if not "count" in request.GET.keys():
        # get 5 random titles
        random_titles = np.random.choice(df['titre'], size=5)
    else:
       # parse the QP to only have decimals
        if re.findall('\d+',request.GET['count'])[0] != '':
            # get the query parameter's number of movies
            random_titles = np.random.choice(df['titre'], size=int(request.GET['count']))

    #----2. Get Recommendations -----------------------------------------------------------------------------------

    # containers
    rec = {'titre_'+str(i) : [] for i in range(1,6)}
    rec_taux = {str(i)+'_taux_recommendation' : [] for i in range(1,6)}
    rec_ids = {str(i)+'_imdb_id' : [] for i in range(1,6)}

    # movie Loop
    for title in random_titles:
        # get recommendation for one title
        imdb_ids, recommendations, similarities =  get_recommendations(title, cosine_matrix, indices,df)

        i = 1
        j = 1
        h = 1
        # append the 5 recommendations to the container
        for imdb_id in imdb_ids:
            rec_ids[str(h)+'_imdb_id'].append(imdb_id)
            h+=1
        for title_rec in recommendations :
            rec['titre_'+str(i)].append(title_rec)
            i+=1
        for similarity in similarities :
            rec_taux[str(j)+ '_taux_recommendation'].append(similarity)
            j+=1

    #----3. JSON response writing ---------------------------------------------------------------------------------


    # add global info to the response
    response_dict = {
        "counts":len(random_titles),
        "results":[]
    }
    j = 0
    # write the recommendations for the response ( ugly way )
    for title in random_titles: 
        i=1
        recs_details = []
        while i < 6:
            detail_rec_dict = {
                    "Rec_"+str(i):
                    {
                    "title":rec["titre_"+str(i)][j],
                    "imdb_id":int(rec_ids[str(i)+"_imdb_id"][j]),
                    "rec rate": round(float(rec_taux[str(i)+"_taux_recommendation"][j]),3)*100
                }
                }
            recs_details.append(detail_rec_dict)
            i+=1
        movie_dict_details = {
            "Recommendation for Movie":title,
            "Recommendations":recs_details
        }
        j+=1

        response_dict["results"].append(movie_dict_details)
    return JsonResponse(response_dict)

@csrf_exempt
@api_view(['POST'])
def recom_one(request):
    """
    From a given title in the body response ( json format ) 
    Return the recommendations 
    """
    #----1. Check request -----------------------------------------------------------------------------------------
    # str ( json )-> dict
    body = json.loads(request.body)

    # check if "titles" in body
    if not "titles" in body.keys():
        return JsonResponse({"message":"Error : Key 'titles' not found"})
    
    # ? list -> list
    if not isinstance(body["titles"], list):
        titles = [body["titles"]]
    else:
        titles = body["titles"]

    # str ? 
    if not all(isinstance(elem, str) for elem in titles):
        return JsonResponse({"message":"Error : All elements of the titles list, should be of type string"})
    
    #----2. Get Recommendations -----------------------------------------------------------------------------------
    # containers
    rec = {'titre_'+str(i) : [] for i in range(1,6)}
    rec_taux = {str(i)+'_taux_recommendation' : [] for i in range(1,6)}
    rec_ids = {str(i)+'_imdb_id' : [] for i in range(1,6)}

    # loop to append in containers
    for title in titles:
        imdb_ids, recommendations, similarities =  get_recommendations(title, cosine_matrix, indices,df)
        i = 1
        j = 1
        h = 1
        for imdb_id in imdb_ids:
            rec_ids[str(h)+'_imdb_id'].append(imdb_id)
            h+=1

        for title_rec in recommendations :
            rec['titre_'+str(i)].append(title_rec)
            i+=1
        for similarity in similarities :
            rec_taux[str(j)+ '_taux_recommendation'].append(similarity)
            j+=1

    #----3. JSON response writing ---------------------------------------------------------------------------------
    response_dict = {
        "counts":len(titles),
        "results":[]
    }
    j = 0
    for title in titles: 
        i=1
        recs_details = []
        while i < 6:
            detail_rec_dict = {
                    "Rec_"+str(i):
                    {
                    "title":rec["titre_"+str(i)][j],
                    "imdb_id":int(rec_ids[str(i)+"_imdb_id"][j]),
                    "rec rate":'%.2f' % (round(float(rec_taux[str(i)+"_taux_recommendation"][j]),3)*100)
                }
                }
            recs_details.append(detail_rec_dict)
            i+=1
        movie_dict_details = {
            "Recommendation for Movie":title,
            "Recommendations":recs_details
        }
        j+=1
        response_dict["results"].append(movie_dict_details)


    return JsonResponse(response_dict)


#-- RECOMMENDATIONS BY DESC-----------------------------------------------------------------------------------------------
@csrf_exempt
@api_view(['POST'])
def recom_one_by_desc(request):
    """
    From a given description for an HTTP POST request
    Compute the embeddings, compare with existing cosine similarity matrix
    Return the recommendations 
    """

    #----1. Check request -----------------------------------------------------------------------------------------

    # str ( json )-> dict
    body = json.loads(request.body)

    if not "description" in body.keys():
        return JsonResponse({"message":"Error : Key 'description' not found"})
    
    if not isinstance(body["description"], list):
        desc = [body["description"]]
    else:
        desc = body["description"]

    if not all(isinstance(elem, str) for elem in desc):
        return JsonResponse({"message":"Error : All elements of the description list, should be of type string"})
    
    if len(desc) > 1:
        return JsonResponse({"message":"Error : Only one description is allowed for one request"})
    
    #----2. Get Recommendations -----------------------------------------------------------------------------------

    # compute the embeddings
    embeddings = preprocess(desc, MODEL,MAX_LENGTH,MODEL_TYPE,BATCH_SIZE)

    # recommendations
    imdb_ids, recommendations, similarities =  get_recommendations_by_desc(embeddings, embeddings_desc, indices,df)

    # containers
    rec = {'titre_'+str(i) : [] for i in range(1,6)}
    rec_taux = {str(i)+'_taux_recommendation' : [] for i in range(1,6)}
    rec_ids = {str(i)+'_imdb_id' : [] for i in range(1,6)}

    # counters
    i = 1
    j = 1
    h = 1

    for imdb_id in imdb_ids:
        rec_ids[str(h)+'_imdb_id'].append(imdb_id)
        h+=1

    for title_rec in recommendations :
        rec['titre_'+str(i)].append(title_rec)
        i+=1
    for similarity in similarities :
        rec_taux[str(j)+ '_taux_recommendation'].append(similarity)
        j+=1


    #----3. JSON response writing ---------------------------------------------------------------------------------


    response_dict = {
        "counts":len(desc),
        "results":[]
    }
    j = 0
    i=1
    recs_details = []
    while i < 6:
        detail_rec_dict = {
                "Rec_"+str(i):
                {
                "title":rec["titre_"+str(i)][j],
                "imdb_id":int(rec_ids[str(i)+"_imdb_id"][j]),
                "rec rate":'%.2f' % (round(float(rec_taux[str(i)+"_taux_recommendation"][j]),3)*100)
            }
            }
        recs_details.append(detail_rec_dict)
        i+=1
    movie_dict_details = {
        "Recommendation for the given description":desc,
        "Recommendations":recs_details
    }
    response_dict["results"].append(movie_dict_details)


    return JsonResponse(response_dict)