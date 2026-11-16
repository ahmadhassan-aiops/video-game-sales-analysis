"""Platforms: releases over time, platform lifecycles, and which platforms are rising for 2017."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, note, section


def render() -> None:
    d = data.games()
    r = data.games(data.RECENT)

    header("Platforms", "Which platforms will matter in 2017?",
           "Platforms rise and fall in cycles. The long history shows how long a cycle lasts; the last five years "
           "show where each platform is in its cycle.")

    section("Games released per year", "All platforms, 1980-2016.")
    rel = d.groupby("year_of_release")["name"].nunique()
    chart(charts.bars(rel.index.astype(str), rel.values, highlight=(rel.index >= data.RECENT).tolist(),
                      hover="%{x}<br><b>%{y:,}</b> games released", ytitle="Games released").update_xaxes(nticks=14))
    insight(f"Releases grew through the 1990s and 2000s, peaked in {rel.idxmax()} ({rel.max():,} games), then fell. "
            f"The analysis uses {data.RECENT}-2016 (highlighted), which reflects today's platforms.")

    section("Platform lifecycles", "Total copies sold per year for the six best-selling platforms of all time.")
    top = d.groupby("platform")["total_sales"].sum().nlargest(6).index
    life = d[d.platform.isin(top)].groupby(["year_of_release", "platform"])["total_sales"].sum().unstack().fillna(0)
    life = life[life.index >= 1994]
    pick = st.multiselect("Platforms", list(top), default=list(top[:3]), max_selections=3, key="life")
    if pick:
        chart(charts.lines(life.index.astype(str), {p: life[p].round(1) for p in pick}, hover_fmt=",.1f", unit="M",
                           ytitle="Copies sold (millions)", markers=False))
    span = d.groupby("platform")["year_of_release"].agg(lambda s: s.max() - s.min())
    insight(f"A platform typically sells for about <b>{span.median():.0f} years</b> from first to last release "
            "(PC is the exception at over 30). Sales rise for 3-5 years, peak, then fade as the next generation "
            "arrives.")

    section(f"Where each platform stands, {data.RECENT}-2016", "Copies sold per year, recent platforms.")
    p = r.groupby(["year_of_release", "platform"])["total_sales"].sum().unstack().fillna(0)
    order = p.sum().sort_values(ascending=False).index[:8]
    heat = p[order].T.round(1)
    heat.columns = heat.columns.astype(str)
    chart(charts.heatmap(heat, hover="%{y}, %{x}<br><b>%{z:.1f}M</b> copies", colorbar="Millions", text_fmt=".0f",
                         height=380))
    insight("<b>PS4 and Xbox One</b> grew every year to 2015: the rising generation. <b>PS3 and Xbox 360</b> peaked "
            "in 2012-2013 and are fading out. <b>3DS</b> has fallen every year since 2013 and is past its peak.")
    note("Every platform looks lower in 2016 because the 2016 data is incomplete, so judge trends by 2012-2015 and "
         "read 2016 as a partial year.")

    section("Sales per game, by platform", f"{data.RECENT}-2016. The box shows the middle half of games; dots are hits.")
    mains = list(order[:6])
    clip = st.toggle("Zoom in on the typical game (hits go off the top)", value=True, key="clip")
    groups = {pl: r.loc[r.platform == pl, "total_sales"] for pl in mains}
    fig = charts.boxes(groups, ytitle="Copies sold per game (millions)", points=True, color=charts.BLUE)
    if clip:
        fig.update_yaxes(range=[0, 2.5])  # whiskers stay at 1.5 x IQR; hits above are off-scale
    chart(fig)
    med = r[r.platform.isin(mains)].groupby("platform")["total_sales"].median().sort_values(ascending=False)
    insight(f"The typical game sells well under a million copies everywhere; the median is highest on "
            f"{med.index[0]} ({med.iloc[0]:.2f}M) and {med.index[1]} ({med.iloc[1]:.2f}M). A handful of hits on each "
            "platform sell many times more.")

    footer()
