"""Page registry, shared by app.py and pages that link to other pages."""

import streamlit as st

from views import findings, genres, method, platforms, regions, reviews

FINDINGS = st.Page(findings.render, title="Key findings", icon=":material/insights:", url_path="findings", default=True)
PLATFORMS = st.Page(platforms.render, title="Platforms", icon=":material/sports_esports:", url_path="platforms")
GENRES = st.Page(genres.render, title="Genres", icon=":material/category:", url_path="genres")
REGIONS = st.Page(regions.render, title="Regions", icon=":material/public:", url_path="regions")
REVIEWS = st.Page(reviews.render, title="Reviews & tests", icon=":material/reviews:", url_path="reviews")
METHOD = st.Page(method.render, title="Data & method", icon=":material/dataset:", url_path="method")

PAGES = [FINDINGS, PLATFORMS, GENRES, REGIONS, REVIEWS, METHOD]
