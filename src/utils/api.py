import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"
PLACEHOLDER_IMAGE = "https://placehold.co/500x750/333/FFFFFF?text=No+Poster"


def fetch_poster(movie_id: int) -> str:
    if not TMDB_API_KEY:
        st.warning("TMDB_API_KEY not set in environment.")
        return PLACEHOLDER_IMAGE
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return POSTER_BASE_URL + poster_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
    return PLACEHOLDER_IMAGE
