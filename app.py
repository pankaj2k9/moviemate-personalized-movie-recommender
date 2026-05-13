'''
Author: Pankaj Kumar Pramanik
Email: pkp2.me2k9@gmail.com
Date: 2026-May-13
'''

import pandas as pd
import streamlit as st

from src.recommender import load_data, recommend

st.set_page_config(layout="wide")
st.header("Movie Recommender System Using Machine Learning")

movies, similarity = load_data()
movie_list = movies["title"].values

selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    with st.spinner("Finding recommendations..."):
        names, posters, years, ratings = recommend(selected_movie, movies, similarity)

    if names:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i])
                st.caption(f"Year: {int(years[i]) if pd.notna(years[i]) else 'N/A'}")
                st.caption(f"Rating: {ratings[i]:.1f} ⭐")
