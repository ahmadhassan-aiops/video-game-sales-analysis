"""Genres: total sales vs sales per game."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, section


def render() -> None:
    r = data.games(data.RECENT)
    g = r.groupby("genre")["total_sales"].agg(total="sum", games="count", mean="mean", median="median")

    header("Genres", "Which genres pay off?",
           f"Genres compared on {data.RECENT}-2016 releases: total sales, number of games, and what a typical game "
           "sells.")

    measure = st.segmented_control("Rank genres by", ["Median copies per game", "Average copies per game",
                                                      "Total copies", "Number of games"],
                                   default="Median copies per game", key="m", label_visibility="collapsed") \
        or "Median copies per game"
    col, fmt = {"Median copies per game": ("median", ".2f"), "Average copies per game": ("mean", ".2f"),
                "Total copies": ("total", ",.0f"), "Number of games": ("games", ",")}[measure]
    s = g[col].sort_values(ascending=False)
    top3 = ["Shooter", "Sports", "Platform"]
    unit = "" if col == "games" else "M"
    chart(charts.bars(s.index, s.values, horizontal=True, highlight=s.index.isin(top3).tolist(),
                      customdata=g.loc[s.index, ["games"]].values,
                      hover=f"<b>%{{y}}</b><br>%{{x:{fmt}}}{unit}<br>%{{customdata[0]}} games",
                      xtitle=measure + (" (millions)" if unit else "")))
    if col in ("median", "mean"):
        insight("Per game, <b>Shooter, Sports and Platform</b> (highlighted) lead whether you use the average or the "
                "median. The median is the safer measure: it describes a typical release, while the average is "
                "pulled up by a few blockbusters.")
    elif col == "total":
        insight(f"By total sales <b>Action</b> leads ({g.loc['Action', 'total']:,.0f}M copies), but that comes from "
                f"{g.loc['Action', 'games']:,} releases, far more than any other genre.")
    else:
        insight("Action has by far the most releases. Lots of releases means lots of competition for each title.")

    section("Volume vs value", "Each dot is a genre: how many games, and what a typical one sells.")
    chart(charts.scatter(g["games"], g["median"], customdata=g.reset_index()[["genre"]].values,
                         hover="<b>%{customdata[0]}</b><br>%{x} games, median %{y:.2f}M copies",
                         xtitle="Games released, 2012-2016", ytitle="Median copies per game (millions)")
          .update_traces(marker=dict(size=14), text=g.index, textposition="top center", mode="markers+text",
                         textfont=dict(size=11)))
    insight(f"Adventure is the trap: {g.loc['Adventure', 'games']} releases but a median of only "
            f"{g.loc['Adventure', 'median'] * 1000:.0f}k copies. Shooter sits at the top: a moderate number of games, each selling "
            "the most.")

    footer()
