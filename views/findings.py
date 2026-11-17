"""Landing page: what Ice should bet on in 2017, and why."""

import plotly.graph_objects as go
import streamlit as st

from lib import charts, data
from lib.ui import cap, finding, footer, header, method_card, recommendations, spotlight


def render() -> None:
    from nav import GENRES, METHOD, PLATFORMS, REGIONS, REVIEWS

    m = data.meta()
    r = data.games(data.RECENT)
    p = r.groupby(["year_of_release", "platform"])["total_sales"].sum().unstack()
    g = r.groupby("genre")["total_sales"].median().sort_values(ascending=False)
    jp = r.groupby(r["rating"].fillna("No rating"))["jp_sales"].sum()
    corr = {pl: r[r.platform == pl][["critic_score", "user_score", "total_sales"]].corr(method="spearman")
            for pl in ["PS4", "XOne"]}

    header(
        "Exploratory data analysis · statistics · Python",
        "What makes a video game sell? Planning 2017 for the online store Ice",
        f"Ice sells games worldwide and plans its 2017 advertising at the end of 2016. Using {m['rows']:,} game "
        f"releases from {m['years'][0]} to 2016, with sales by region, critic and user scores and age ratings, I "
        "looked for the platforms, genres and regional patterns most likely to pay off.",
        chips=[("code", "Python, pandas"), ("functions", "SciPy tests"), ("public", "NA, EU, Japan"),
               ("sports_esports", f"{m['platforms']} platforms")],
    )

    k = st.columns(4)
    k[0].metric("Game releases", f"{m['rows']:,}", border=True)
    k[1].metric("Platforms", m["platforms"], border=True)
    k[2].metric("Copies sold since 2012", f"{r['total_sales'].sum():,.0f}M", border=True)
    k[3].metric("Analysis window", f"{data.RECENT}-2016", border=True)

    pf = p.fillna(0)
    main = pf.sum().sort_values(ascending=False).index[:8]
    hi = {"PS4": charts.BLUE, "XOne": charts.ORANGE}
    fig = go.Figure()
    for pl in [x for x in main if x not in hi] + [x for x in hi if x in main]:
        fig.add_trace(go.Scatter(
            x=pf.index.astype(int), y=pf[pl].round(1), name=pl, mode="lines+markers",
            line=dict(color=hi.get(pl, charts.QUIET), width=3.5 if pl in hi else 1.8),
            marker=dict(size=7 if pl in hi else 5, line=dict(width=1.5, color=charts.SURFACE)),
            hovertemplate=f"{pl}: %{{y:.1f}}M<extra></extra>",
        ))
        if pl in hi:
            fig.add_annotation(x=2015, y=pf.loc[2015, pl], text=f"<b>{pl}</b>", showarrow=False, xanchor="left",
                               xshift=8, yshift=8, font=dict(color=hi[pl], size=13))
    charts.style(fig, height=380)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(title="Copies sold (millions)")
    fig.update_xaxes(dtick=1, tickformat="d")
    fig.add_vrect(x0=2015.5, x1=2016.3, fillcolor=charts.GRID, opacity=0.45, line_width=0, layer="below")
    fig.add_annotation(x=2015.9, y=1, yref="paper", text="2016: partial year", showarrow=False, yanchor="top",
                       font=dict(color=charts.INK_2, size=12))
    spotlight("The new generation is taking over",
              f"Copies sold per year on the eight biggest platforms since {data.RECENT}. <b>PS4</b> and <b>Xbox One</b> "
              "(highlighted) climbed every year to 2015 while the older consoles and handhelds (faint lines) faded: they are "
              "the platforms to back in 2017.", fig, key="spot")

    st.subheader("Key findings", anchor=False)
    a = st.columns(3)
    finding(a[0], "PS4 & Xbox One", "the only platforms still growing until 2015",
            "Bet on the new generation",
            f"PS4 sales rose to {p.loc[2015, 'PS4']:.0f}M copies in 2015 and Xbox One to {p.loc[2015, 'XOne']:.0f}M, while "
            "PS3, Xbox 360 and 3DS were all falling. Platforms last about 6 years, so these two lead 2017.",
            PLATFORMS, "Platforms", card_icon="videogame_asset")
    finding(a[1], f"{g.iloc[0] * 1000:,.0f}k", f"median copies per {g.index[0].lower()} game",
            "Shooters sell best per game",
            f"A typical shooter sells {g.iloc[0] / g['Action']:.1f}x a typical action game. Action has the most total "
            "sales only because it has by far the most releases.", GENRES, "Genres", card_icon="target")
    finding(a[2], f"{jp['No rating'] / jp.sum():.0%}", "of Japanese sales are games with no ESRB rating",
            "Japan is a different market",
            "Japan buys handhelds (3DS) and role-playing games; North America and Europe buy home consoles, action and "
            "shooters. ESRB is a North American rating, so many Japan-only titles don't have one.", REGIONS, "Regions", card_icon="travel_explore")
    b = st.columns(3)
    finding(b[0], f"{corr['PS4'].loc['critic_score', 'total_sales']:.2f}",
            "rank correlation of critic score with sales (PS4)",
            "Critics matter; user scores mostly don't",
            f"Higher critic scores go with higher sales on every platform checked. User scores show almost no link "
            f"on the main platforms ({corr['PS4'].loc['user_score', 'total_sales']:+.2f} on PS4).", REVIEWS, "Reviews", card_icon="reviews")
    finding(b[1], "No difference", "in average user score, Xbox One vs PC",
            "Platform doesn't change how users score",
            "A t-test finds no significant difference between Xbox One and PC user scores.", REVIEWS, "Hypothesis tests", card_icon="balance")
    finding(b[2], "Significant", "difference in user scores, Action vs Sports",
            "Sports games score lower with users",
            "Action games average about 6.8 out of 10 with users; Sports games about 5.5.", REVIEWS, "Hypothesis tests", card_icon="balance")

    st.subheader("What I would recommend for 2017", anchor=False)
    recommendations([
        ("videogame_asset", "Back PS4 and Xbox One", "Focus advertising on their titles, with 3DS only for Japan."),
        ("target", "Prioritise shooters, sports and platformers",
         "They sell best per title; be selective with action and adventure, where most releases sell little."),
        ("public", "Run separate campaigns for Japan", "Handheld and role-playing games, not the Western top sellers."),
        ("grade", "Feature critic scores", "They track sales; user scores mostly don't."),
    ])
    cap("Based on 2012-2016 data, with 2016 incomplete; recommendations are hypotheses to test, not forecasts.")
    method_card("<b>How this was done.</b> The sales table was cleaned (unknown user scores kept as missing), "
                "limited to 2012-2016 for current trends, and analysed by platform, genre and region, with "
                "correlation and hypothesis tests on the review scores.", METHOD,
                tools=["pandas", "SciPy", "Spearman correlation", "t-tests"])

    footer()
