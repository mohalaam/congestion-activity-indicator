"""
Step 01: clean the archived daily TomTom panel (2019-12-30 to 2023-02-14) and build
city-level and country-level daily congestion indices for the study sample.

Inputs : data_raw/tomtom_trafic_index.csv  (country, city, date, congestion, diffRatio)
Outputs: data_proc/city_daily.csv          cleaned city panel with adjustments
         data_proc/country_daily.csv       population-weighted country index
         data_proc/country_weekly.csv, country_monthly.csv
         data_proc/panel_summary.json      coverage diagnostics
Run:  py -I pipeline/01_build_congestion_panel.py
"""
import json
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data_raw", "tomtom_trafic_index.csv")
OUT = os.path.join(ROOT, "data_proc")
os.makedirs(OUT, exist_ok=True)

# Main sample (12 EM countries) and secondary panel. Population weights (metro, millions,
# approximate 2020 UN/national figures) are used to aggregate cities to a country index.
MAIN = {
    "Turkey": {"Istanbul": 15.5, "Ankara": 5.7, "Izmir": 4.4, "Bursa": 3.1, "Antalya": 2.5,
               "Adana": 2.2, "Konya": 2.2, "Gaziantep": 2.1, "Mersin": 1.9, "Kayseri": 1.4},
    "Poland": {"Warsaw": 1.8, "Krakow": 0.8, "Lodz": 0.7, "Wroclaw": 0.64, "Poznan": 0.53,
               "Gdansk, Gdynia and Sopot": 0.75, "Katowice urban area": 2.0, "Szczecin": 0.4,
               "Lublin": 0.34, "Bydgoszcz": 0.35, "Bialystok": 0.3, "Bielsko-Biala": 0.17},
    "Brazil": {"Sao Paulo": 22.0, "Rio de Janeiro": 13.5, "Belo Horizonte": 6.0, "Brasilia": 4.6,
               "Porto Alegre": 4.3, "Recife": 4.1, "Fortaleza": 4.1, "Salvador": 3.9, "Curitiba": 3.7},
    "South Africa": {"Johannesburg": 5.8, "Cape Town": 4.7, "Durban": 3.9, "Pretoria": 2.6,
                     "Bloemfontein": 0.8, "East London": 0.8},
    "India": {"Mumbai": 20.4, "New Delhi": 30.3, "Bengaluru": 12.3, "Pune": 6.6},
    "Saudi Arabia": {"Riyadh": 7.5, "Jeddah": 4.7},
    "Mexico": {"Mexico City": 21.8},
    "Indonesia": {"Jakarta": 10.8},
    "Thailand": {"Bangkok": 10.5},
    "Egypt": {"Cairo": 20.9},
    "Malaysia": {"Kuala Lumpur": 7.8},
    "Philippines": {"Manila": 13.9},
}
SECONDARY = {
    "Chile": {"Santiago": 6.8}, "Colombia": {"Bogota": 10.9}, "Peru": {"Lima": 10.7},
    "Argentina": {"Buenos Aires": 15.2}, "Hungary": {"Budapest": 1.8},
    "Romania": {"Bucharest": 1.8}, "Greece": {"Athens": 3.2, "Thessaloniki": 1.0},
}


def main():
    d = pd.read_csv(RAW, parse_dates=["date"])
    d["country"] = d["country"].replace({"Türkiye": "Turkey"})
    weights = {}
    group = {}
    for grp, dic in (("main", MAIN), ("secondary", SECONDARY)):
        for c, cities in dic.items():
            for city, w in cities.items():
                weights[(c, city)] = w
                group[(c, city)] = grp
    d = d[[(c, ci) in weights for c, ci in zip(d["country"], d["city"])]].copy()
    d["weight"] = [weights[(c, ci)] for c, ci in zip(d["country"], d["city"])]
    d["group"] = [group[(c, ci)] for c, ci in zip(d["country"], d["city"])]

    # Basic cleaning: congestion is a percentage (0-200+). Drop impossible values, flag gaps.
    d = d.sort_values(["country", "city", "date"])
    d.loc[(d["congestion"] < 0) | (d["congestion"] > 300), "congestion"] = np.nan
    full_idx = pd.date_range(d["date"].min(), d["date"].max(), freq="D")
    frames = []
    for (c, ci), g in d.groupby(["country", "city"]):
        g = g.set_index("date").reindex(full_idx)
        g["country"], g["city"] = c, ci
        g["weight"], g["group"] = weights[(c, ci)], group[(c, ci)]
        g["missing"] = g["congestion"].isna().astype(int)
        g["congestion"] = g["congestion"].interpolate(limit=3)  # fill gaps up to 3 days
        frames.append(g.rename_axis("date").reset_index())
    d = pd.concat(frames, ignore_index=True)

    # Calendar features and weekday adjustment: congestion relative to the city's
    # same-weekday mean over a trailing 52-week window (log ratio), robust to level shifts.
    d["dow"] = d["date"].dt.dayofweek
    d["log_c"] = np.log(d["congestion"].clip(lower=1))

    def wk_adj(g):
        g = g.sort_values("date").copy()
        base = g.groupby("dow")["log_c"].transform(lambda s: s.rolling(52, min_periods=8).mean().shift(1))
        g["log_c_dowadj"] = g["log_c"] - base
        # Simple detrended level: deviation from trailing 365-day mean
        g["log_c_detr"] = g["log_c"] - g["log_c"].rolling(365, min_periods=60).mean().shift(1)
        return g
    d = d.groupby(["country", "city"], group_keys=False).apply(wk_adj)
    d.to_csv(os.path.join(OUT, "city_daily.csv"), index=False)

    # Country aggregation (population-weighted means of levels and adjusted logs)
    def wavg(g, col):
        m = g[col].notna()
        return np.average(g.loc[m, col], weights=g.loc[m, "weight"]) if m.any() else np.nan
    rows = []
    for (c, dt_), g in d.groupby(["country", "date"]):
        rows.append({"country": c, "date": dt_, "group": g["group"].iloc[0],
                     "n_cities": int(g["congestion"].notna().sum()),
                     "congestion": wavg(g, "congestion"),
                     "log_c": wavg(g, "log_c"),
                     "log_c_dowadj": wavg(g, "log_c_dowadj"),
                     "log_c_detr": wavg(g, "log_c_detr"),
                     "diffRatio": wavg(g, "diffRatio")})
    cd = pd.DataFrame(rows).sort_values(["country", "date"])
    cd.to_csv(os.path.join(OUT, "country_daily.csv"), index=False)
    num = ["congestion", "log_c", "log_c_dowadj", "log_c_detr", "diffRatio"]
    cw = cd.set_index("date").groupby("country")[num].resample("W-FRI").mean().reset_index()
    cm = cd.set_index("date").groupby("country")[num].resample("M").mean().reset_index()
    cw.to_csv(os.path.join(OUT, "country_weekly.csv"), index=False)
    cm.to_csv(os.path.join(OUT, "country_monthly.csv"), index=False)

    summ = {
        "date_min": str(d["date"].min().date()), "date_max": str(d["date"].max().date()),
        "n_days": int(d["date"].nunique()), "n_cities": int(d.groupby(["country", "city"]).ngroups),
        "countries": sorted(d["country"].unique().tolist()),
        "missing_share_by_country": d.groupby("country")["missing"].mean().round(4).to_dict(),
        "mean_congestion_by_country": cd.groupby("country")["congestion"].mean().round(2).to_dict(),
    }
    json.dump(summ, open(os.path.join(OUT, "panel_summary.json"), "w"), indent=2)
    print(json.dumps(summ, indent=2))


if __name__ == "__main__":
    main()
