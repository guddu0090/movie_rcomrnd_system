import streamlit as st
import pickle
import pandas as pd
import requests

# ---------- Poster Fetching Function ----------
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c69da02b2d8b3911e9e5db599957ad54&language=en-US'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# ---------- Load Data ----------
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies_df = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ---------- Recommendation Function ----------
def recommend(movie_title: str, k: int = 5):
    idx = movies_df[movies_df["title"] == movie_title].index[0]
    distances = similarity[idx]
    nearest = sorted(
        enumerate(distances), key=lambda x: x[1], reverse=True
    )[1 : k + 1]

    recommended_movies = []
    recommended_posters = []

    for i, _ in nearest:
        movie_id = movies_df.iloc[i].movie_id
        recommended_movies.append(movies_df.iloc[i].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ---------- Streamlit UI ----------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Pick a movie you like:",
    movies_df["title"].values,
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    st.subheader("You might also enjoy:")
    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
