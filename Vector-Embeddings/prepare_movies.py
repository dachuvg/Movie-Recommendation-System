import pandas as pd
import numpy as np
from ast import literal_eval

df1 = pd.read_csv('tmdb_5000_credits.csv/tmdb_5000_credits.csv')
df2 = pd.read_csv('./tmdb_5000_movies.csv/tmdb_5000_movies.csv')
df1.columns = ['id','title','cast','crew']
df= df2.merge(df1,on='title')


features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df[feature] = df[feature].apply(literal_eval)

# ---- Extract Director ----
def get_director(x):
    for i in x:
        if i.get('job') == 'Director':
            return i.get('name')
    return np.nan

df['director'] = df['crew'].apply(get_director)

# ---- Extract top 3 names per feature ----
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x if 'name' in i]
        return names[:3] if len(names) > 3 else names
    return []

features = ['cast', 'keywords', 'genres']
for feature in features:
    df[feature] = df[feature].apply(get_list)

# ---- Clean and normalize ----
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

# ---- Combine everything into metadata (including overview) ----
def create_metadata(x):
    return (
        (x['overview'] if isinstance(x['overview'], str) else '') + ' ' + 
        (' '.join([x['title']]) if isinstance(x['title'], str) else '') + ' ' +
        ' '.join(x['keywords']) + ' ' +
        ' '.join(x['cast']) + ' ' +
        (x['director'] if isinstance(x['director'], str) else '') + ' ' +
        ' '.join(x['genres'])
    ).strip()

df['metadata'] = df.apply(create_metadata, axis=1)
df.rename(columns={'id_y': 'movie_id'}, inplace=True)

df_final = df[['movie_id', 'title', 'metadata']].dropna(subset=['metadata'])

# Save for later use
df_final.to_pickle("movies_final.pkl")
print("✅ Saved movies_final.pkl with metadata")
