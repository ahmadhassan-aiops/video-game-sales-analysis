"""Data & method: the sales table, cleaning decisions, analysis window, and limits."""

import pandas as pd
import streamlit as st

from lib import data
from lib.site import NOTEBOOK_URL
from lib.ui import footer, header, md, section


def render() -> None:
    m = data.meta()
    mb = m["missing_before"]

    header(
        "Data & method",
        "How the analysis was done",
        "The data, the cleaning decisions, why the analysis focuses on 2012-2016, and the limits. The full Python "
        f'work is in the <a href="{NOTEBOOK_URL}" target="_blank">original notebook</a>.',
    )

    section("The data")
    md(f"**{m['raw_shape'][0]:,} rows**, one per game and platform, released {m['years'][0]}-{m['years'][1]}.")
    st.table(pd.DataFrame([
        ("name, platform, year_of_release, genre", "The game and where and when it was released"),
        ("na_sales, eu_sales, jp_sales, other_sales", "Copies sold, in millions, by region"),
        ("critic_score", "Critics' average score, 0-100"),
        ("user_score", "Users' average score, 0-10 (or \"tbd\")"),
        ("rating", "ESRB age rating (E, E10+, T, M, ...)"),
    ], columns=["Columns", "Meaning"]), hide_index=True, border="horizontal")
    with st.expander("Look at the raw data (50 random rows)"):
        st.dataframe(data.table("sample_games"), hide_index=True, height=320)

    section("Cleaning decisions")
    st.table(pd.DataFrame([
        ("Column names", "Mixed case", "Lowercased"),
        ("User score \"tbd\"", f"{m['tbd_user_scores']:,} games: score to be determined",
         "Treated as missing, so the column becomes numeric"),
        ("Missing name, genre or year", f"{mb['year_of_release']} without a year, {mb['name']} without a name",
         f"Dropped ({m['dropped_rows']} rows, under 2%)"),
        ("Duplicates", f"{m['duplicates']} game with the same name, platform and year twice", "Dropped"),
        ("Missing scores and ratings", f"Critic score missing for {mb['critic_score']:,} games, ESRB rating for "
         f"{mb['rating']:,}", "Kept as missing: filling them would invent reviews. Ratings are shown as \"No rating\""),
        ("Total sales", "Not in the data", "Added as the sum of the four regions"),
    ], columns=["Item", "What was found", "How it was handled"]), hide_index=True, border="horizontal")

    section("Why 2012-2016")
    md("Platforms last about six years, so sales from the 2000s describe consoles nobody is buying games for in "
       "2017. 2012-2016 covers the current generation's launch (PS4, Xbox One in 2013) and the previous one's "
       "decline. **2016 is incomplete**, so trends are read from 2012-2015.")

    section("Changes from the original notebook")
    md("- Genre comparison uses the **median** copies per game alongside the average (same top three).\n"
       "- Review-score correlations keep **all games**, including hits, and use rank correlation.\n"
       "- **3DS is not counted as a rising platform**: its sales fell every year from 2013.\n"
       "- **Missing ESRB ratings are shown** as their own group, which reveals the Japan-only titles.")

    section("Limits of this data")
    md("- **Copies, not revenue.** Prices and digital sales are not included.\n"
       "- **2016 incomplete**, and nothing after it.\n"
       "- **Scores exist for only about half the games**, mostly the better-known ones.\n"
       "- **Descriptive, not causal.** High critic scores go with high sales, but marketing budgets may drive both.")

    section("How this app is built")
    md("Python, pandas, SciPy and Plotly in a Streamlit app. `build_data.py` cleans the CSV once into a Parquet "
       f"file that ships with the app. Data built on {m['built']}.")

    footer()
