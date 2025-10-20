import pandas as pd
import os
from ast import literal_eval
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
import requests

df1 = pd.read_csv('tmdb_5000_credits.csv/tmdb_5000_credits.csv')
df2 = pd.read_csv('./tmdb_5000_movies.csv/tmdb_5000_movies.csv')
df1.columns = ['id','title','cast','crew']
df= df2.merge(df1,on='title')


features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df[feature] = df[feature].apply(literal_eval)


def get_director(x):
    for i in x:
        if i.get('job') == 'Director':
            return i.get('name')
    return np.nan

df['director'] = df['crew'].apply(get_director)


def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x if 'name' in i]
        return names[:3] if len(names) > 3 else names
    return []

features = ['cast', 'keywords', 'genres']
for feature in features:
    df[feature] = df[feature].apply(get_list)


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    elif isinstance(x, str):
        return str.lower(x.replace(" ", ""))
    else:
        return ''

features = ['title', 'cast', 'director', 'keywords', 'genres']
for feature in features:
    df[feature] = df[feature].apply(clean_data)


def create_metadata(x):
    title_weight = 2
    director_weight = 2 
    genre_weight = 3
    
    return (
        (x['overview'] if isinstance(x['overview'], str) else '') + ' ' +
        (' '.join([x['title']]*title_weight) if isinstance(x['title'], str) else '') + ' ' +
        ' '.join(x['keywords']) + ' ' +
        ' '.join(x['cast']) + ' ' +
        (x['director']*director_weight if isinstance(x['director'], str) else '') + ' ' +
        ' '.join(x['genres']*genre_weight)
    ).strip()

df['metadata'] = df.apply(create_metadata, axis=1)
df.rename(columns={'id_y': 'movie_id'}, inplace=True)

df_final = df[['movie_id', 'title', 'metadata']].dropna(subset=['metadata'])
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

texts = df_final['metadata'].tolist()
metas = [{"title": t} for t in df_final['title']]

vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metas)
vectorstore.save_local("movie_vectorstore")

print("✅ Vector store built and saved at:", "movie_vectorstore")
