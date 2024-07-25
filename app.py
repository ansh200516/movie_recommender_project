import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
similarity=pickle.load(open('similarity.pkl', 'rb'))
def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]
    recommended_movies = []
    movie_poster=[]
    for i in movies_list:
        title = movie_list.iloc[i[0]].title
        movie_id=movie_list.iloc[i[0]].id
        if title not in recommended_movies:
            recommended_movies.append(title)
            movie_poster.append(fetch_poster(movie_id))
            if len(recommended_movies) == 5:
                break
    return recommended_movies,movie_poster
movie_list=pd.DataFrame(pickle.load(open('movies.pkl', 'rb')))
st.title('Movie Recommender System')
option=st.selectbox(
    "List of Movies",
    movie_list['title'].values
)
if st.button('Recommend'):
    recommendation,poster=recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendation[0])
        st.image(poster[0])
    with col2:
        st.text(recommendation[1])
        st.image(poster[1])

    with col3:
        st.text(recommendation[2])
        st.image(poster[2])
    with col4:
        st.text(recommendation[3])
        st.image(poster[3])
    with col5:
        st.text(recommendation[4])
        st.image(poster[4])