"""Reviews & tests: do review scores relate to sales, and the two user-score hypothesis tests."""

import pandas as pd
import streamlit as st
from scipy import stats

from lib import charts, data
from lib.ui import chart, footer, header, insight, md, note, section


def render() -> None:
    r = data.games(data.RECENT)

    header("Statistics", "Reviews and hypothesis tests",
           "Do critic and user scores go with higher sales? And do user scores differ between platforms or genres?")

    section("Review scores vs sales", "One platform at a time; each dot is a game.")
    a, b = st.columns(2)
    pl = a.selectbox("Platform", ["PS4", "XOne", "3DS", "PS3", "X360", "PC", "WiiU"], key="pl")
    score = b.segmented_control("Score", ["Critic score (0-100)", "User score (0-10)"], default="Critic score (0-100)",
                                key="score") or "Critic score (0-100)"
    col = "critic_score" if score.startswith("Critic") else "user_score"
    x = r[(r.platform == pl)].dropna(subset=[col])
    chart(charts.scatter(x[col], x["total_sales"], customdata=x[["name"]].values,
                         hover="<b>%{customdata[0]}</b><br>score %{x}<br>%{y:.2f}M copies",
                         xtitle=score, ytitle="Copies sold (millions, log scale)", trend=False)
          .update_yaxes(type="log", tickvals=[0.01, 0.03, 0.1, 0.3, 1, 3, 10], ticktext=["0.01", "0.03", "0.1", "0.3",
                                                                                     "1", "3", "10"]))
    rows = []
    for p in ["PS4", "XOne", "3DS", "PS3", "X360", "PC", "WiiU"]:
        y = r[r.platform == p]
        rows.append({"Platform": p, "Games": len(y),
                     "Critic score": y[["critic_score", "total_sales"]].corr(method="spearman").iloc[0, 1],
                     "User score": y[["user_score", "total_sales"]].corr(method="spearman").iloc[0, 1]})
    t = pd.DataFrame(rows)
    st.dataframe(t, hide_index=True, column_config={
        "Critic score": st.column_config.NumberColumn("Critic score vs sales", format="%.2f"),
        "User score": st.column_config.NumberColumn("User score vs sales", format="%.2f")})
    insight(f"Critic scores show a <b>moderate positive link</b> with sales on every platform (rank correlation "
            f"{t['Critic score'].min():.2f} to {t['Critic score'].max():.2f}). User scores show <b>little or none</b> on "
            f"most platforms ({(t['User score'].abs() < 0.25).sum()} of {len(t)} between -0.25 and +0.25); Wii U, with "
            f"few games, is the exception ({t.set_index('Platform').loc['WiiU', 'User score']:+.2f}). The sales axis is "
            "logarithmic because a few hits sell a hundred times more than a typical game.")
    note("The first version of the analysis computed these correlations after removing high-selling games as outliers, which "
         "removes the hits that matter most. Here every game is kept, and rank (Spearman) correlation limits the "
         "influence of extreme values instead.")

    alpha = st.select_slider("Significance level (α)", options=[0.01, 0.05, 0.10], value=0.05, key="alpha")

    def test(a_, b_, names, h0, h1):
        res = stats.ttest_ind(a_, b_, equal_var=False)
        k = st.columns(4)
        k[0].metric(f"{names[0]} average", f"{a_.mean():.2f}", border=True)
        k[1].metric(f"{names[1]} average", f"{b_.mean():.2f}", border=True)
        k[2].metric("Games", f"{len(a_)} vs {len(b_)}", border=True)
        k[3].metric("p-value (Welch's t-test)", f"{res.pvalue:.2g}", border=True)
        md(f"- **H₀:** {h0}\n- **H₁:** {h1}")
        verdict = "<b>Reject H₀</b>: the averages differ." if res.pvalue < alpha else \
            "<b>Do not reject H₀</b>: no significant difference."
        insight(f"{verdict} (α = {alpha:g}, p = {res.pvalue:.2g})")
        chart(charts.histograms({names[0]: a_, names[1]: b_}, bin_size=0.5, start=0, xtitle="User score (0-10)"))

    section("1. Xbox One vs PC user scores")
    us = r.dropna(subset=["user_score"])
    test(us.loc[us.platform == "XOne", "user_score"], us.loc[us.platform == "PC", "user_score"], ("Xbox One", "PC"),
         "Average user scores for Xbox One and PC games are the same.", "They differ.")
    section("2. Action vs Sports user scores")
    test(us.loc[us.genre == "Action", "user_score"], us.loc[us.genre == "Sports", "user_score"], ("Action", "Sports"),
         "Average user scores for Action and Sports games are the same.", "They differ.")

    footer()
