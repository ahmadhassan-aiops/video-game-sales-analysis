"""Loads the prepared games table in data/ (built by build_data.py)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data"
REGIONS = {"na_sales": "North America", "eu_sales": "Europe", "jp_sales": "Japan"}
RECENT = 2012


@st.cache_data
def meta() -> dict:
    return json.loads((DATA / "meta.json").read_text(encoding="utf-8"))


@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_parquet(DATA / f"{name}.parquet")


@st.cache_data
def games(since: int | None = None) -> pd.DataFrame:
    g = table("games")
    return g if since is None else g[g["year_of_release"] >= since].reset_index(drop=True)
