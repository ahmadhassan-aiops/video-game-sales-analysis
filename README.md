# What makes a video game sell? Planning 2017 for the online store Ice

An interactive presentation of an exploratory data analysis by **Ahmad Hassan** (AI Engineer). 16,443 game
releases (1980-2016) with sales by region, critic and user scores and ESRB ratings, analysed to plan the
online store Ice's 2017 advertising.

- **Key findings** and recommendations for 2017.
- **Platforms**: releases over time, platform lifecycles, where each platform stands, sales per game.
- **Genres**: total sales vs sales per game (median and mean), volume vs value.
- **Regions**: platform, genre and ESRB-rating mix in North America, Europe and Japan.
- **Reviews & tests**: critic and user scores vs sales, and two Welch t-tests on user scores.
- **Data & method**: cleaning decisions, the 2012-2016 window, changes from the original notebook, limits.

Original notebook: [AIOPS-Portfolio-Projects / Video Games Console Sale Analysis](https://github.com/ahmadhassan-aiops/AIOPS-Portfolio-Projects/tree/main/1.%20Data-analysis-with-python-Projects/Video%20Games%20Console%20Sale%20Analysis)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Rebuild the data: `python build_data.py "path/to/Video Games Console Sale Analysis"` (folder with `moved_games.csv`).

Structure: `app.py` (entry), `nav.py` (pages), `views/` (one module per page), `lib/` (data loading, charts, UI),
`build_data.py` (CSV to Parquet), `data/` (shipped with the app), `Dockerfile` (port 7860).
