"""
Chart styling and builders (Plotly), shared by the analysis apps.

Colour rules: one colour per single-series chart; a highlight colour plus a
recessive grey when one part of the chart is the point; a one-hue light-to-dark
ramp for heatmaps; for comparisons, categorical slots in fixed order
(blue, orange, aqua) and never more than three series on one chart.
No colour ramps on bars, no pies, no dual axes.
"""

from __future__ import annotations

from typing import Sequence

import pandas as pd
import plotly.graph_objects as go

# Palette (validated reference palette, light mode)
BLUE = "#2a78d6"       # series 1 / highlight
ORANGE = "#eb6834"     # series 2
AQUA = "#1baf7a"       # series 3
SERIES = [BLUE, ORANGE, AQUA]
QUIET = "#c9d6e6"      # de-emphasised bars
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#fcfcfb"
SEQUENTIAL = [
    [0.0, "#f2f7fd"], [0.15, "#cde2fb"], [0.3, "#9ec5f4"], [0.45, "#6da7ec"],
    [0.6, "#3987e5"], [0.75, "#256abf"], [0.9, "#184f95"], [1.0, "#0d366b"],
]

FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
CONFIG = {"displayModeBar": False, "scrollZoom": False}


def style(fig: go.Figure, *, height: int = 360, title: str | None = None, legend: bool = False) -> go.Figure:
    fig.update_layout(
        height=height,
        title=dict(text=title, x=0, xanchor="left", font=dict(size=15, color=INK)) if title else None,
        font=dict(family=FONT, size=13, color=INK_2),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        margin=dict(l=8, r=16, t=48 if title else 16, b=8),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, xanchor="left", title=None),
        hoverlabel=dict(bgcolor="white", bordercolor=GRID, font=dict(family=FONT, color=INK, size=13)),
        bargap=0.25,
    )
    fig.update_xaxes(automargin=True, showgrid=False, linecolor=AXIS, ticks="", tickfont=dict(color=MUTED),
                     title_font=dict(color=INK_2))
    fig.update_yaxes(automargin=True, gridcolor=GRID, zeroline=False, linecolor=AXIS, tickfont=dict(color=MUTED),
                     title_font=dict(color=INK_2))
    return fig


def bars(
    x, y, *, highlight=None, horizontal: bool = False, hover: str, customdata=None,
    xtitle: str = "", ytitle: str = "", height: int = 360, title: str | None = None,
    text=None, color: str = BLUE,
) -> go.Figure:
    """Single-series bars. `highlight` is a boolean mask: True bars in `color`, the rest QUIET."""
    n = len(x)
    colors = color if highlight is None else [color if h else QUIET for h in highlight]
    fig = go.Figure(go.Bar(
        x=y if horizontal else x,
        y=x if horizontal else y,
        orientation="h" if horizontal else "v",
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        customdata=customdata,
        hovertemplate=hover + "<extra></extra>",
        text=text,
        textposition="outside" if text is not None else None,
        textfont=dict(color=INK_2, size=12),
        cliponaxis=False,
    ))
    style(fig, height=height, title=title)
    if horizontal:
        fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color=INK_2), title=ytitle)
        fig.update_xaxes(showgrid=True, gridcolor=GRID, title=xtitle)
        fig.update_layout(height=max(height, 26 * n + 60))
    else:
        fig.update_xaxes(title=xtitle)
        fig.update_yaxes(title=ytitle)
    return fig


def grouped_bars(
    categories, series: dict[str, Sequence], *, hover_fmt: str = ",", unit: str = "",
    xtitle: str = "", ytitle: str = "", horizontal: bool = False, height: int = 380,
) -> go.Figure:
    """Up to three series side by side (fixed slot order)."""
    assert len(series) <= 3, "fold extra series into 'Other' or facet"
    fig = go.Figure()
    for (name, values), color in zip(series.items(), SERIES):
        fig.add_trace(go.Bar(
            name=name,
            x=values if horizontal else categories,
            y=categories if horizontal else values,
            orientation="h" if horizontal else "v",
            marker=dict(color=color, line=dict(width=0), cornerradius=3),
            hovertemplate=f"<b>%{{{'y' if horizontal else 'x'}}}</b><br>{name}: "
                          f"%{{{'x' if horizontal else 'y'}:{hover_fmt}}}{unit}<extra></extra>",
        ))
    style(fig, height=height, legend=True)
    fig.update_layout(barmode="group", bargap=0.2, bargroupgap=0.08)
    if horizontal:
        fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color=INK_2), title=ytitle)
        fig.update_xaxes(showgrid=True, gridcolor=GRID, title=xtitle)
        fig.update_layout(height=max(height, 30 * len(categories) * len(series) // 2 + 80))
    else:
        fig.update_xaxes(title=xtitle)
        fig.update_yaxes(title=ytitle)
    return fig


def stacked_bars(categories, parts: dict[str, Sequence], *, colors: Sequence[str], hover_fmt: str = ",",
                 unit: str = "", xtitle: str = "", ytitle: str = "", height: int = 380) -> go.Figure:
    """Parts of a whole (e.g. base fee + overage). Colours passed explicitly so meaning stays fixed."""
    fig = go.Figure()
    for (name, values), color in zip(parts.items(), colors):
        fig.add_trace(go.Bar(
            name=name, x=categories, y=values,
            marker=dict(color=color, line=dict(width=2, color=SURFACE)),
            hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:{hover_fmt}}}{unit}<extra></extra>",
        ))
    style(fig, height=height, legend=True)
    fig.update_layout(barmode="stack")
    fig.update_xaxes(title=xtitle)
    fig.update_yaxes(title=ytitle)
    return fig


def lines(x, series: dict[str, Sequence], *, hover_fmt: str = ",", unit: str = "", ytitle: str = "",
          xtitle: str = "", height: int = 360, markers: bool = True) -> go.Figure:
    """One to three lines on one axis with a unified hover."""
    assert len(series) <= 3
    fig = go.Figure()
    for (name, y), color in zip(series.items(), SERIES):
        fig.add_trace(go.Scatter(
            x=x, y=y, name=name, mode="lines+markers" if markers else "lines",
            line=dict(color=color, width=2.5), marker=dict(size=8, line=dict(width=2, color=SURFACE)),
            hovertemplate=f"{name}: %{{y:{hover_fmt}}}{unit}<extra></extra>",
        ))
    style(fig, height=height, legend=len(series) > 1)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title=xtitle, showspikes=True, spikecolor=AXIS, spikethickness=1, spikedash="solid")
    fig.update_yaxes(title=ytitle)
    return fig


def histograms(groups: dict[str, Sequence], *, bins: int | None = None, xtitle: str = "", unit: str = "",
               percent: bool = True, height: int = 360, bin_size: float | None = None, start: float | None = None) -> go.Figure:
    """Distributions for up to three groups, side by side and normalised so different group sizes compare fairly."""
    assert len(groups) <= 3
    fig = go.Figure()
    for (name, values), color in zip(groups.items(), SERIES):
        xbins = dict(size=bin_size, start=start) if bin_size else None
        fig.add_trace(go.Histogram(
            x=list(values), name=name, nbinsx=bins, xbins=xbins,
            histnorm="percent" if percent else None,
            marker=dict(color=color, line=dict(width=0)),
            hovertemplate=f"{name}<br>%{{x}}{unit}: %{{y:.1f}}{'%' if percent else ''}<extra></extra>",
        ))
    style(fig, height=height, legend=len(groups) > 1)
    fig.update_layout(barmode="group", bargap=0.12, bargroupgap=0.05)
    fig.update_xaxes(title=xtitle)
    fig.update_yaxes(title="Share of the group" if percent else "Count", ticksuffix="%" if percent else "")
    return fig


def boxes(groups: dict[str, Sequence], *, ytitle: str = "", unit: str = "", height: int = 380,
          horizontal: bool = False, color: str | None = None, points: bool = False) -> go.Figure:
    """Box plots. Up to three groups get series colours; more groups share one colour."""
    fig = go.Figure()
    many = len(groups) > 3
    for i, (name, values) in enumerate(groups.items()):
        c = color or (BLUE if many else SERIES[i])
        fig.add_trace(go.Box(
            **({"x": list(values)} if horizontal else {"y": list(values)}), name=name,
            marker=dict(color=c, size=4), line=dict(color=c, width=1.5), fillcolor="rgba(0,0,0,0)",
            boxpoints="outliers" if points else False,
            hoverinfo="skip" if not points else None,
        ))
    style(fig, height=height)
    if horizontal:
        fig.update_xaxes(title=ytitle, showgrid=True, gridcolor=GRID)
        fig.update_yaxes(autorange="reversed", tickfont=dict(color=INK_2))
    else:
        fig.update_yaxes(title=ytitle)
        fig.update_xaxes(tickfont=dict(color=INK_2))
    return fig


def scatter(x, y, *, hover: str, customdata=None, xtitle: str = "", ytitle: str = "", height: int = 420,
            color: str = BLUE, log_x: bool = False, trend: bool = False) -> go.Figure:
    fig = go.Figure(go.Scattergl(
        x=x, y=y, mode="markers", customdata=customdata,
        marker=dict(color=color, size=8, opacity=0.6, line=dict(width=0.5, color=SURFACE)),
        hovertemplate=hover + "<extra></extra>",
    ))
    if trend:
        import numpy as np
        xs, ys = np.asarray(x, float), np.asarray(y, float)
        ok = ~(np.isnan(xs) | np.isnan(ys))
        if ok.sum() > 2:
            k, b = np.polyfit(np.log10(xs[ok]) if log_x else xs[ok], ys[ok], 1)
            gx = np.linspace(xs[ok].min(), xs[ok].max(), 50)
            gy = k * (np.log10(gx) if log_x else gx) + b
            fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color=INK_2, width=2, dash="dot"),
                                     hoverinfo="skip", name="Trend"))
    style(fig, height=height)
    fig.update_xaxes(title=xtitle, type="log" if log_x else None, showgrid=True, gridcolor=GRID)
    fig.update_yaxes(title=ytitle)
    return fig


def heatmap(z: pd.DataFrame, *, hover: str, colorbar: str = "", height: int = 360, text_fmt: str | None = None) -> go.Figure:
    fig = go.Figure(go.Heatmap(
        z=z.values, x=[str(c) for c in z.columns], y=[str(i) for i in z.index],
        colorscale=SEQUENTIAL, xgap=2, ygap=2,
        texttemplate=f"%{{z:{text_fmt}}}" if text_fmt else None, textfont=dict(size=11),
        colorbar=dict(title=dict(text=colorbar, side="top"), thickness=10, outlinewidth=0, tickfont=dict(color=MUTED)),
        hovertemplate=hover + "<extra></extra>",
    ))
    style(fig, height=height)
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color=INK_2))
    return fig


def vline(fig: go.Figure, x, label: str, bottom: bool = False) -> go.Figure:
    fig.add_vline(x=x, line=dict(color=INK_2, width=1.5, dash="dot"))
    fig.add_annotation(x=x, y=0 if bottom else 1, yref="paper", text=label, showarrow=False, xanchor="left", xshift=6,
                       yanchor="bottom" if bottom else "top", font=dict(color=INK_2, size=12), bgcolor=SURFACE)
    return fig


def hline(fig: go.Figure, y, label: str) -> go.Figure:
    fig.add_hline(y=y, line=dict(color=INK_2, width=1.5, dash="dot"))
    fig.add_annotation(x=1, xref="paper", y=y, text=label, showarrow=False, xanchor="right",
                       yanchor="bottom", font=dict(color=INK_2, size=12), bgcolor=SURFACE)
    return fig
