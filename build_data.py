"""
Offline build step: moved_games.csv -> data/games.parquet + data/meta.json.

    python build_data.py "W:/Portfolio Projects/1. Data-analysis-with-python-Projects/Video Games Console Sale Analysis"

Cleaning (as in the notebook): lowercase column names; "tbd" user scores become missing; rows without name, genre
or release year dropped; one duplicate (same name, platform and year) dropped; total_sales = sum of the regions.
Missing critic/user scores and ESRB ratings are kept as missing (not filled).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_RAW = Path("W:/Portfolio Projects/1. Data-analysis-with-python-Projects/Video Games Console Sale Analysis")
OUT = Path(__file__).parent / "data"


def main(raw: Path) -> None:
    OUT.mkdir(exist_ok=True)
    d = pd.read_csv(raw / "moved_games.csv")
    raw_shape = list(d.shape)
    d.columns = d.columns.str.lower()
    d.sample(50, random_state=7).to_parquet(OUT / "sample_games.parquet", index=False)
    tbd = int((d["user_score"] == "tbd").sum())
    d["user_score"] = pd.to_numeric(d["user_score"].replace("tbd", np.nan))
    missing_before = {k: int(v) for k, v in d.isna().sum().items()}
    d = d.dropna(subset=["name", "genre", "year_of_release"])
    d["year_of_release"] = d["year_of_release"].astype(int)
    dups = int(d.duplicated(subset=["name", "platform", "year_of_release"]).sum())
    d = d.drop_duplicates(subset=["name", "platform", "year_of_release"]).reset_index(drop=True)
    d["total_sales"] = d[["na_sales", "eu_sales", "jp_sales", "other_sales"]].sum(axis=1)
    d.to_parquet(OUT / "games.parquet", index=False)

    meta = {
        "built": date.today().isoformat(),
        "raw_shape": raw_shape,
        "rows": int(len(d)),
        "games": int(d["name"].nunique()),
        "platforms": int(d["platform"].nunique()),
        "years": [int(d["year_of_release"].min()), int(d["year_of_release"].max())],
        "tbd_user_scores": tbd,
        "missing_before": missing_before,
        "dropped_rows": raw_shape[0] - len(d) - dups,
        "duplicates": dups,
        "no_rating_share": float(d["rating"].isna().mean()),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RAW)
