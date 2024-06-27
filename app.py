<<<<<<< HEAD
import streamlit as st 
import pickle
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=63e10fcf4b568a9bd6984e82e18ed77c&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


st.title('Movie Recommender System')

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

options = movies['title'].values
options=np.insert(options,0,'Select a movie')

movie_selected = st.selectbox(
    'Select the required movie',
    (options)
)

cosine_sim2=pickle.load(open('cosine_sim.pkl','rb'))
indices = pd.Series(movies.index,index=movies['title'])

def get_recommendation(title,cosine_sim2=cosine_sim2):
    idx=indices[title]
    rec_movies=[]
    rec_posters=[]
    sim_scores=list(enumerate(cosine_sim2[idx]))
    sim_scores=sorted(sim_scores,key=lambda x:x[1],reverse=True)
    sim_scores=sim_scores[1:11]
    for i in sim_scores:
        movie_id=movies['id'].iloc[i[0]]
        rec_posters.append(fetch_poster(movie_id))
        rec_movies.append(movies['title'].iloc[i[0]])
    return rec_movies , rec_posters   


if st.button('Recommend'):
    if movie_selected== 'Select a movie':
        st.write('Please select a valid option')
    else:    
        names,poster = get_recommendation(movie_selected)
        row1=st.columns(3)
        row2=st.columns(3)
        col1,col2,col3=st.columns(3)
        with col1:
            st.header(names[0])
            st.image(poster[0])
        with col2:
            st.header(names[1])
            st.image(poster[1])    
        with col3:
            st.header(names[2])
            st.image(poster[2])
        col4,col5,col6=st.columns(3)    
        with col4:
            st.header(names[3])
            st.image(poster[3])    
        with col5:
            st.header(names[4])
            st.image(poster[4])
        with col6:
            st.header(names[5])
=======
import streamlit as st 
import pickle
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=63e10fcf4b568a9bd6984e82e18ed77c&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


st.title('Movie Recommender System')

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

options = movies['title'].values
options=np.insert(options,0,'Select a movie')

movie_selected = st.selectbox(
    'Select the required movie',
    (options)
)

cosine_sim2=pickle.load(open('cosine_sim.pkl','rb'))
indices = pd.Series(movies.index,index=movies['title'])

def get_recommendation(title,cosine_sim2=cosine_sim2):
    idx=indices[title]
    rec_movies=[]
    rec_posters=[]
    sim_scores=list(enumerate(cosine_sim2[idx]))
    sim_scores=sorted(sim_scores,key=lambda x:x[1],reverse=True)
    sim_scores=sim_scores[1:11]
    for i in sim_scores:
        movie_id=movies['id'].iloc[i[0]]
        rec_posters.append(fetch_poster(movie_id))
        rec_movies.append(movies['title'].iloc[i[0]])
    return rec_movies , rec_posters   


if st.button('Recommend'):
    if movie_selected== 'Select a movie':
        st.write('Please select a valid option')
    else:    
        names,poster = get_recommendation(movie_selected)
        row1=st.columns(3)
        row2=st.columns(3)
        col1,col2,col3=st.columns(3)
        with col1:
            st.header(names[0])
            st.image(poster[0])
        with col2:
            st.header(names[1])
            st.image(poster[1])    
        with col3:
            st.header(names[2])
            st.image(poster[2])
        col4,col5,col6=st.columns(3)    
        with col4:
            st.header(names[3])
            st.image(poster[3])    
        with col5:
            st.header(names[4])
            st.image(poster[4])
        with col6:
            st.header(names[5])
>>>>>>> e37e3e6 (Fully implemented app)
            st.image(poster[5])       