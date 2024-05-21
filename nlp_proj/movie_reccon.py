import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from ast import literal_eval
import warnings
warnings.filterwarnings('ignore')

df1 = pd.read_csv('dataset/tmdb_5000_credits.csv')
df2 = pd.read_csv('dataset/tmdb_5000_movies.csv')

#Merging both dataframes
df1.columns = ['id','title_x','cast','crew']
df2 = df2.merge(df1,on = 'id')


#Tfidf 
tfidf = TfidfVectorizer( stop_words='english' )
df2['overview'] = df2['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(df2['overview'])

#Calculating cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) #Linear kernel because binary attributes cosine sim is calculated like that

#Drop duplicate
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()
def get_recommendations(title,cosine_sim = cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx])) #Creates [(0,0.23),(1,0.31),(2,0.0)...]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #Sort in descending order of the similarity 
    sim_scores = sim_scores[1:11] #Consider only top 10 highest similarity movies
    movie_indices = [i[0] for i in sim_scores] 
    return df2['title'].iloc[movie_indices]

print(get_recommendations('The Godfather')) #tfidf


##################################################################################################################################

#Bag-of-Words

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval) #Literal_eval helps traverse the abstract syntax tree and accurate parse complex data of unknown origin into their respective datatypes 



def get_director(x):
    for i in x:
        if (i['job'] == 'Director'):
            return i['name']
    return np.nan



def get_list(x):
    if (isinstance(x,list)):
        names = [i['name'] for i in x]
        if len(names) > 3:
            return names[:3]
        return names
    return []


df2['director'] = df2['crew'].apply(get_director)
features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''



features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(clean_data)



def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)


#print(df2['soup'][0:1][1])
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])


cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])


print("\n")
print("------------------Bag-of-Words-------------------------------")
print(get_recommendations('The Godfather',cosine_sim2)) #Bag-of-Words



















