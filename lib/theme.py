"""This app's colours and icon. The page layout is shared by the analysis apps; the look is per app."""

ACCENT = "#c22d7c"      # charts and highlights (3:1 or more on the page background)
ACCENT_INK = "#a01f64"  # text in the accent colour (4.5:1 or more)
SERIES_2 = "#2a78d6"    # second series in comparisons
SERIES_3 = "#1baf7a"    # third series
ICON = "sports_esports"  # Material Symbols name for the hero badge
HERO_MOTIF = """"""  # extra CSS for the hero band, if any


def _mix(color: str, other: str, t: float) -> str:
    """Blend `color` towards `other` by t (0 = color, 1 = other)."""
    a = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


ACCENT_SOFT = _mix(ACCENT, "#ffffff", 0.92)   # callout and hero backgrounds
ACCENT_TINT = _mix(ACCENT, "#ffffff", 0.72)   # borders and decoration
QUIET = _mix(ACCENT, "#e4e4e0", 0.78)         # de-emphasised bars, same family as the accent
SEQUENTIAL = [  # one-hue light-to-dark ramp for heatmaps and the map
    [0.0, _mix(ACCENT, "#ffffff", 0.95)], [0.2, _mix(ACCENT, "#ffffff", 0.75)], [0.4, _mix(ACCENT, "#ffffff", 0.5)],
    [0.6, _mix(ACCENT, "#ffffff", 0.2)], [0.75, ACCENT], [0.9, _mix(ACCENT, "#000000", 0.3)],
    [1.0, _mix(ACCENT, "#000000", 0.55)],
]
