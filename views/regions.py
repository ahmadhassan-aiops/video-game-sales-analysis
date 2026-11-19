"""Regions: top platforms, genres and ESRB ratings in North America, Europe and Japan."""

import pandas as pd
import streamlit as st

from lib import charts, data
from lib.ui import cap, chart, footer, header, insight, section


def _shares(r: pd.DataFrame, by: str, k: int = 6) -> pd.DataFrame:
    s = r.groupby(by)[list(data.REGIONS)].sum()
    s = s / s.sum()
    order = s.max(axis=1).sort_values(ascending=False).index[:k]
    return s.loc[order].rename(columns=data.REGIONS)


def render() -> None:
    r = data.games(data.RECENT)

    header("Regions", "Each region buys differently",
           f"Share of each region's {data.RECENT}-2016 sales by platform, genre and ESRB age rating. Bars of the same "
           "colour always mean the same region.")

    section("Platforms", "Share of the region's copies sold.")
    s = _shares(r, "platform", 7)
    chart(charts.grouped_bars(s.index, {c: s[c].values for c in s.columns}, hover_fmt=".1%",
                              ytitle="Share of the region's sales").update_yaxes(tickformat=".0%"))
    insight("North America leans Xbox (X360 is its top platform) and Europe leans PlayStation (PS4, PS3). "
            f"<b>Japan is a handheld market</b>: 3DS alone takes {s.loc['3DS', 'Japan']:.0%} of Japanese sales, and "
            "the PS Vita appears in Japan's top three but nowhere else.")

    section("Genres", "Share of the region's copies sold.")
    s = _shares(r, "genre", 7)
    chart(charts.grouped_bars(s.index, {c: s[c].values for c in s.columns}, hover_fmt=".1%",
                              ytitle="Share of the region's sales").update_yaxes(tickformat=".0%"))
    insight("North America and Europe look alike: action, shooters and sports. <b>Japan's top genre is "
            f"role-playing</b> ({s.loc['Role-Playing', 'Japan']:.0%}), and shooters are only {s.loc['Shooter', 'Japan']:.0%} "
            "of Japanese sales.")

    section("ESRB age ratings", "M = mature 17+, T = teen, E10+ = 10 and over, E = everyone.")
    rr = r.assign(rating=r["rating"].fillna("No rating"))
    s = _shares(rr, "rating", 6).reindex(["M", "E", "T", "E10+", "No rating"]).dropna(how="all")
    chart(charts.grouped_bars(s.index, {c: s[c].values for c in s.columns}, hover_fmt=".1%",
                              ytitle="Share of the region's sales").update_yaxes(tickformat=".0%"))
    insight(f"Mature-rated games lead in North America ({s.loc['M', 'North America']:.0%}) and Europe "
            f"({s.loc['M', 'Europe']:.0%}). In Japan <b>{s.loc['No rating', 'Japan']:.0%}</b> of sales are games "
            "with no ESRB rating at all.")
    cap("ESRB is the North American rating board, so games released only in Japan usually have no ESRB rating. "
        "Missing ratings there mostly mean \"Japan-only title\", not \"unrated\", so they are shown as their own "
        "group: leaving them out would understate how different Japan is.")

    footer()
