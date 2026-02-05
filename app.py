import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b8c831a51bc453aedddd67fc6efd6aa9"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()   # HTTP error check
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return ""
    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        return ""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict  = pickle.load(open('movie_dict.pkl', 'rb'))
similarity  = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Search for a movie or select from the dropdown",
    movies['title'].values
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:  # <-- check empty or not
                st.image(posters[i])
            else:
                st.write("Poster not available")
