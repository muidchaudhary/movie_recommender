import streamlit as st
import pandas as pd
st.title('Movie Recommender System')

import pickle
import requests

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

selected_movies = st.selectbox(
  "What movie do you like to watch ?",
  movies['title'].values)

similarity = pickle.load(open('similarity.pkl','rb'))

#Defining a function to call poster by hitting library (Request library required)
def fetch_poster(movie_id):
  api = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9354c19b178a3c5098f3ebd53bd68705'.format(movie_id))
  # will get a response from above now well convert those response to json
  data = api.json()
  return "https://image.tmdb.org/t/p/w500" + data['poster_path']
  # we have to add API image reader URL before the fetched poster path from json

def recommend(movie):
  movies_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movies_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

  #fetching poster through api
  recommended_movies = []
  recommended_movies_posters = []
  for i in movies_list:
    movie_id = movies.iloc[i[0]].id
    #fetch posters through API and will call our fetch_poster function
    recommended_movies.append(movies.iloc[i[0]].title)
    recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies,recommended_movies_posters

# RECOMMENDATION BUTTONS 5 MOVIES
if st.button('Recommend'):
    names,posters = recommend(selected_movies)
    #Displaying recommendations 5 movies and their posters using layout your columns from
    col1, col2, col3, col4, col5 = st.columns(5)
# PEHLE YAHAN HUMNE ST.HEADER USE LIYA USSKI WAJAH SE JAGAH KUM THI ABB st.text use karenge to accha naame dikhaga
    with col1:
      st.text(names[0])
      st.image(posters[0])

    with col2:
      st.text(names[1])
      st.image(posters[1])

    with col3:
      st.text(names[2])
      st.image(posters[2])

    with col4:
      st.text(names[3])
      st.image(posters[3])

    with col5:
      st.text(names[4])
      st.image(posters[4])

