"""Shared page furniture: CSS, headers, insight callouts, chart wrapper, footer."""

from __future__ import annotations

import html

import streamlit as st

from lib.charts import CONFIG
from lib.site import DATA_CREDIT, LEARN_URL, NOTEBOOK_URL

CSS = """
<style>
:root { --ink:#0b0b0b; --ink-2:#52514e; --muted:#6f6d68; --line:#e1e0d9; --blue:#2a78d6; --blue-soft:#eef4fc;
        --warn:#8a5a00; --warn-soft:#fdf6e7; }
.block-container { padding-top: 4.5rem; max-width: 1180px; }
h1, h2, h3 { color: var(--ink); letter-spacing: -0.01em; }
.kicker { font-size: .78rem; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; color: var(--blue); margin: 0 0 .25rem; }
.lead { font-size: 1.08rem; color: var(--ink-2); max-width: 760px; line-height: 1.6; margin: .25rem 0 1.25rem; }
.insight { background: var(--blue-soft); border-left: 3px solid var(--blue); border-radius: 0 10px 10px 0;
           padding: .85rem 1.1rem; color: var(--ink); font-size: .98rem; line-height: 1.55; margin: .25rem 0 1.5rem; }
.note { background: var(--warn-soft); border-left: 3px solid #eda100; border-radius: 0 10px 10px 0;
        padding: .75rem 1.1rem; color: var(--ink); font-size: .95rem; line-height: 1.55; margin: .25rem 0 1.25rem; }
.big { font-size: 2.1rem; font-weight: 700; color: var(--ink); line-height: 1.1; margin: 0; }
.big-label { color: var(--muted); font-size: .85rem; margin: .1rem 0 .6rem; }
.card-title { font-weight: 650; color: var(--ink); font-size: 1.02rem; margin: 0 0 .35rem; }
.card-text { color: var(--ink-2); font-size: .95rem; line-height: 1.55; margin: 0 0 .5rem; }
.verdict { font-weight: 650; }
.footer { color: var(--muted); font-size: .85rem; border-top: 1px solid var(--line); padding-top: 1rem; margin-top: 2.5rem; }
.footer a { color: var(--ink-2); }
[data-testid="stMetricValue"] { font-weight: 700; }
</style>
"""


def esc(text: str) -> str:
    """Escape $ so Streamlit markdown does not read amounts like $20 ... $70 as a LaTeX formula."""
    return text.replace("$", r"\$")


def md(text: str) -> None:
    st.markdown(esc(text))


def cap(text: str) -> None:
    st.caption(esc(text))


def inject_css() -> None:
    st.html(CSS)


def header(kicker: str, title: str, lead: str) -> None:
    st.html(f'<p class="kicker">{html.escape(kicker)}</p>')
    st.title(title, anchor=False)
    st.html(f'<p class="lead">{lead}</p>')


def insight(text: str) -> None:
    """Callout with the takeaway of the chart above. `text` may contain <b>."""
    st.html(f'<div class="insight">{text}</div>')


def note(text: str) -> None:
    """Amber callout for a caveat or a correction to the original analysis."""
    st.html(f'<div class="note">{text}</div>')


def chart(fig, key: str | None = None) -> None:
    st.plotly_chart(fig, theme=None, config=CONFIG, key=key)


def section(title: str, question: str | None = None) -> None:
    st.subheader(title, anchor=False)
    if question:
        cap(question)


def finding(col, big: str, big_label: str, title: str, text: str, page=None, link_label: str = "") -> None:
    with col.container(border=True, height="stretch"):
        st.html(
            f'<p class="big">{big}</p><p class="big-label">{big_label}</p>'
            f'<p class="card-title">{title}</p><p class="card-text">{text}</p>'
        )
        if page is not None:
            st.page_link(page, label=link_label, icon=":material/arrow_forward:")


def footer() -> None:
    st.html(
        '<div class="footer">Analysis by <b>Ahmad Hassan</b>, AI Engineer · '
        f'<a href="{NOTEBOOK_URL}" target="_blank">Notebook on GitHub</a> · '
        f'<a href="{LEARN_URL}" target="_blank">Learn with Ahmad</a><br>{DATA_CREDIT}</div>'
    )
