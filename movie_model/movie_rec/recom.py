import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

#---STATIC FILES--------------------------------------------------------------------------------------------------------

# paths
csv_filepathname=os.environ['CSV_FILEPATH']
npy_filepathname=os.environ['NPY_FILEPATH']
npy_embeddings_filepathname = os.environ['NPY_EMB_FILEPATH']

df = pd.read_csv(csv_filepathname).drop(columns="Unnamed: 0")

features = df['features'].to_list() 


cosine_matrix = np.load(npy_filepathname)

embeddings_desc = np.load(npy_embeddings_filepathname)

indices = pd.Series(df.index, index=df['titre'])

#---RECOMMENDATIONS FOR A GIVEN TITLE-------------------------------------------------------------------------------------------------

def get_recommendations(title, cosine_sim, indices,df):
    """
    Fonction qui retourne les 10 films ayant la description la plus similaire à partir du title précisé
    """
    if title not in indices.index :
      return ([0 for i in range(1,6)],["unknown_title" for i in range(1,6)],[-1 for i in range(1,6)])
    #Obtenir l'index du film qui correspond au titre à l'aide de la clé de titre des index.
    idx = indices[indices.index == title].values[0]

    # trier les films à partir des "similarity scores"

    order_matrix=  np.sort(cosine_sim[idx])[::-1]

    L = []
    similarities = []

    for i in order_matrix[1:6]:
      similarities.append(i)
      index = np.where(cosine_sim[idx] == i)[0]
      # unstacking when one to many matching
      if len(index )> 1 :
            for j in index :
                        L.append(j[0])
      # or just adding it directly
      else :
            L.append(index[0])
    # dropping duplicates
    LL = list(dict.fromkeys(L))

    # renvoyer le top 10 des films similaires
    titles = [indices[indices.values == index].index[0] for index in LL]

    # 
    imdb_ids = [df[df.index == index].imdb_id.values[0] for index in LL]

    return imdb_ids, titles, similarities 

#---RECOMMENDATIONS FOR A GIVEN SENTENCE--------------------------------------------------------------------------------

def get_recommendations_by_desc(embeddings, embeddings_desc, indices,df):
    """
    Fonction qui retourne les 10 films ayant la description la plus similaire à partir du title précisé
    """

    full_tensor = np.vstack((embeddings_desc, embeddings))


    cosine_sim_desc = cosine_similarity(full_tensor)

    idx = len(cosine_sim_desc) - 1

    order_matrix=  np.sort(cosine_sim_desc[idx])[::-1]

    L = []
    similarities = []

    for i in order_matrix[1:6]:
      similarities.append(i)
      index = np.where(cosine_sim_desc[idx] == i)[0]
      # unstacking when one to many matching
      if len(index )> 1 :

                L.append(index[0])

      # or just adding it directly
      else :
            L.append(index[0])
    # dropping duplicates
    LL = list(dict.fromkeys(L))


    # renvoyer le top 10 des films similaires
    titles = [indices[indices.values == index].index[0] for index in LL]

    # 
    imdb_ids = [df[df.index == index].imdb_id.values[0] for index in LL]

    return imdb_ids, titles, similarities 