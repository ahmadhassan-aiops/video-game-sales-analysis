"""
What makes a video game sell? Planning 2017 campaigns for the online store Ice.
An interactive presentation of Ahmad Hassan's analysis. All data ships with the app.
"""

import streamlit as st

st.set_page_config(
    page_title="Video game sales | Ahmad Hassan",
    page_icon=":material/sports_esports:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from lib.ui import inject_css  # noqa: E402
from nav import PAGES  # noqa: E402

inject_css()
st.navigation(PAGES, position="top").run()
