import os
import pickle

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.utils.api import fetch_poster

load_dotenv()

ARTIFACTS_PATH = os.getenv("ARTIFACTS_PATH", "artifacts")


def load_data() -> tuple[pd.DataFrame, object]:
    try:
        movies_dict = pickle.load(open(f"{ARTIFACTS_PATH}/movie_dict.pkl", "rb"))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open(f"{ARTIFACTS_PATH}/similarity.pkl", "rb"))
        return movies, similarity
    except FileNotFoundError:
        st.error("Model files not found. Run the data processing notebook first.")
        st.stop()


def recommend(movie: str, movies: pd.DataFrame, similarity) -> tuple[list, list, list, list]:
    try:
        index = movies[movies["title"] == movie].index[0]
    except IndexError:
        st.error("Movie not found in dataset. Select another one.")
        return [], [], [], []

    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])

    names, posters, years, ratings = [], [], [], []
    for i, _ in distances[1:6]:
        movie_id = movies.iloc[i].movie_id
        posters.append(fetch_poster(movie_id))
        names.append(movies.iloc[i].title)
        years.append(movies.iloc[i].year)
        ratings.append(movies.iloc[i].vote_average)

    return names, posters, years, ratings
