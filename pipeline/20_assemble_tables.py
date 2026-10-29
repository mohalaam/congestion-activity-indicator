"""
Step 20: numbered tables for the final manuscript, generated from result files, plus
Turkey-specific estimates for the journal paragraph.
Output: paper/TABLES_v4.md, results/tables/turkey_box.md
Run: py -I pipeline/20_assemble_tables.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
RT = os.path.join(ROOT, "results", "tables"); PP = os.path.join(ROOT, "paper")
T = []

def tbl(df, cols, fmt=None, index=False):
    fmt = fmt or {}
    hdr = "| " + " | ".join(cols.values()) + " |\n|" + "|".join("---" for _ in cols) + "|"
    lines = [hdr]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]; f = fmt.get(c, "{}")
            cells.append(f.format(v) if not (isinstance(v, float) and np.isnan(v)) else "")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

# Table 1 descriptives
d1 = pd.read_csv(os.path.join(RT, "table4_descriptives.csv"))
a1 = pd.read_csv(os.path.join(RT, "appendix_A1_cities.csv")); ncity = a1.groupby("country").size().rename("cities")
d1 = d1.merge(ncity, left_on="country", right_index=True)
d1["mean_ret_etf_pct"] = d1["mean_ret_etf_pct"]; d1 = d1.sort_values("country")
T.append("**Table 1. Sample and descriptive statistics, ex-lockdown weeks (July 2020 to February 2023).**\nMean congestion is the average weekly congestion level in percent extra travel time; the innovation is the weekly deviation from the trailing four-week mean of the weekday-adjusted log index, standardized within country; returns are weekly log returns on the US-dollar country fund (Egypt has none); share stress is the fraction of weeks with the VIX above 25.\n\n" +
         tbl(d1, {"country": "Country", "cities": "Cities", "weeks": "Weeks", "mean_congestion": "Mean congestion (%)", "mean_ret_etf_pct": "Mean USD return (%/wk)", "sd_ret_etf_pct": "SD USD return (%/wk)"}, {"mean_congestion": "{:.1f}", "mean_ret_etf_pct": "{:.2f}", "sd_ret_etf_pct": "{:.2f}"}))

# Table 2 seasonality
s2 = pd.read_csv(os.path.join(RT, "round2_seasonality.csv"))
agg = s2.groupby("level", sort=False).agg(n_series=("name", "count"), ac52=("ac52", "mean"), share_ac52=("ac52", lambda s: (s > 0.2).mean()), fourier=("r2_fourier3", "mean"), share_F=("F_p", lambda s: (s < 0.05).mean()), r2_in=("r2_woy", "mean"), r2_adj=("r2_adj", "mean"), r2_loyo=("r2_loyo", "mean")).reset_index()
agg["level"] = agg["level"].map({"city": "Congestion, 49 cities", "country": "Congestion, 12 countries", "factor": "Congestion, cross-country factor", "google_country": "Google workplaces, 12 countries", "google_factor": "Google workplaces, factor"})
T.append("\n\n**Table 2. Annual structure in weekly innovations, ex-lockdown, on a true weekly time index.**\nac(52) is the autocorrelation at a 52-week lag; Fourier R² is from a three-harmonic annual seasonal; the in-sample week-of-year R² (52 cell means on about 138 weeks, chance level about 0.37) is reported with its adjusted and leave-one-year-out values to show that it is overfitted.\n\n" +
         tbl(agg, {"level": "Series", "n_series": "N", "ac52": "Mean ac(52)", "share_ac52": "Share ac(52) > 0.2", "fourier": "Fourier R²", "share_F": "Share Fourier F p < 0.05", "r2_in": "Week-of-year R² (in-sample)", "r2_adj": "Adjusted", "r2_loyo": "Leave-one-year-out"},
             {k: "{:.2f}" for k in ["ac52", "share_ac52", "fourier", "share_F", "r2_in", "r2_adj", "r2_loyo"]}))
cd = s2[s2.level == "country"].sort_values("country" if "country" in s2 else "name")
T.append("\n\nCountry detail (congestion): " + "; ".join(f"{r['name']} ac(52) {r['ac52']:.2f}, Fourier p {r['F_p']:.2f}" for _, r in cd.iterrows()) + ".")

# Table 3 Google by country (from methods table section D)
mp = open(os.path.join(RT, "table_methods_paper.md"), encoding="utf-8").read()
secD = mp.split("## D.")[1].split("## E.")[0]; rowsD = [l for l in secD.splitlines() if l.startswith("|") and not l.startswith("|---") and "country" not in l]
T.append("\n\n**Table 3. Correlation of weekly innovations in congestion and Google workplaces mobility, by country.**\nWeekly innovations constructed identically for both series; overlap is February 2020 to October 2022.\n\n| Country | Full overlap | Excluding March-June 2020 | After June 2021 |\n|---|---|---|---|\n" + "\n".join(rowsD))

# Table 4 nowcast
n4 = pd.read_csv(os.path.join(ROOT, "results", "nowcast_benchmarks_summary_exlock.csv"))
n4 = n4[n4.model.isin(["AR", "BRIDGE", "AMIDAS", "POOL_BRIDGE"])].copy()
n4["model"] = n4["model"].map({"AR": "AR(1) benchmark", "BRIDGE": "Country bridge (monthly congestion change)", "AMIDAS": "Almon MIDAS (60 daily lags)", "POOL_BRIDGE": "Pooled bridge, country fixed effects"})
n4["sample"] = n4["sample"].map({"full_OOS_2021-01+": "2021-01 to 2023-01", "exCOVID_2021-07+": "2021-07 to 2023-01"})
dm = open(os.path.join(RT, "dm_monthly.md"), encoding="utf-8").read()
T.append("\n\n**Table 4. Pseudo-real-time nowcasts of monthly industrial-production growth, 17 countries, lockdown months excluded from training.**\nRMSE relative to the AR(1) benchmark; directional accuracy is the share of correctly signed nowcasts. The Diebold-Mariano test on monthly-average loss differentials (effective sample 21 and 19 months) gives t = 1.35 (p = 0.19) and t = 1.75 (p = 0.10) for the pooled bridge; the pooled country-month version gives p = 0.08 and overstates precision.\n\n" +
         tbl(n4, {"sample": "Evaluation window", "model": "Model", "n": "Country-months", "rel_rmse_vs_AR": "Relative RMSE", "dir_acc": "Directional accuracy"}, {"rel_rmse_vs_AR": "{:.3f}", "dir_acc": "{:.3f}"}))

# Table 5 single-country
s5 = pd.read_csv(os.path.join(RT, "table_single_country.csv")).dropna(subset=["t_act"])
T.append("\n\n**Table 5. Country-by-country regressions of next-week return (percent) on the country's congestion innovation, ex-lockdown.**\nControls: own same-week return, MSCI EM return, change in log VIX, Brent return, change in log DXY, change in US ten-year yield; HAC(4) t-statistics. Three signal versions: actual, lagged 52 weeks, and the real-time seasonal difference. No coefficient is significant at 5 percent for local indices; one of eleven is, a different country each time, for US-dollar funds.\n\n" +
         tbl(s5, {"country": "Country", "target": "Return", "b_act": "Actual b", "t_act": "t", "b_pl": "Lag-52 b", "t_pl": "t", "b_sd": "Seasonal-diff b", "t_sd": "t"}, {k: "{:.2f}" for k in ["b_act", "t_act", "b_pl", "t_pl", "b_sd", "t_sd"]}))

# Table 6 ladder (from table_decisive.csv, ETF ex-lockdown) + three versions + decomposition
d6 = pd.read_csv(os.path.join(RT, "table_decisive.csv")); d6 = d6[(d6.target == "ret_etf_f1") & (d6["sample"] == "ex_lockdown") & d6.spec.str.startswith("L") & ~d6.spec.str.startswith("L8") & ~d6.spec.str.startswith("L9")].copy()
d6["stress"] = d6["b_x_raw"] + d6["b_x_raw_x_S"]
T.append("\n\n**Table 6. The state-dependent specification: fixed-effects ladder, placebo versions and calendar decomposition.**\nDependent variable: next-week US-dollar fund return (SD units); x = congestion innovation (SD units); S = 1[VIX > 25]; ex-lockdown sample. Panel A adds controls cumulatively; L6 is equation (1). Standard errors clustered by week; L7 uses Driscoll-Kraay(4).\n\nPanel A. Fixed-effects ladder\n\n" +
         tbl(d6, {"spec": "Specification", "n": "N", "b_x_raw": "x, calm", "t_x_raw": "t", "b_x_raw_x_S": "x × S", "t_x_raw_x_S": "t", "stress": "x, stress"}, {k: "{:.3f}" for k in ["b_x_raw", "b_x_raw_x_S", "stress"]} | {k: "{:.2f}" for k in ["t_x_raw", "t_x_raw_x_S"]}))
T.append("\nPanel B. Signal versions, equation (1) with stringency and fuel controls\n\n| Version | N | x, calm | t | x × S | t |\n|---|---|---|---|---|---|\n| Actual signal | 1518 | -0.057 | -1.90 | 0.273 | 3.76 |\n| Actual signal, placebo sample | 1098 | -0.028 | -0.81 | 0.189 | 2.57 |\n| Signal lagged 52 weeks | 1098 | 0.027 | 0.78 | 0.078 | 1.16 |\n| Real-time seasonal difference | 1098 | -0.043 | -1.35 | 0.037 | 0.54 |")
T.append("\nPanel C. Calendar decomposition, equation (1) without stringency and fuel\n\n| Regressor | N | calm | t | × S | t |\n|---|---|---|---|---|---|\n| Own in-sample week-of-year profile (seasonal component only) | 1617 | -0.041 | -1.64 | 0.156 | 2.86 |\n| Another country's week-of-year profile | 1617 | -0.001 | -0.03 | 0.007 | 0.13 |\n| Signal minus own profile (non-seasonal residual) | 1518 | -0.024 | -0.94 | 0.102 | 2.00 |\n| Circular block shift of the panel, 300 draws | 1518 | | | placebo t: mean 0.18, SD 1.02; 0 of 300 ≥ 3.69 | |\n| Within 2021 only (L6 without country-by-year effects) | 583 | -0.004 | -0.09 | -0.181 | -1.22 |\n| Within 2022 only | 572 | -0.124 | -2.00 | 0.315 | 3.45 |")

# Table 7 volatility
v7 = pd.read_csv(os.path.join(RT, "volatility_battery.csv"))
T.append("\n\n**Table 7. Next-week log realized variance of US-dollar fund returns on the congestion innovation.**\nHeterogeneous-autoregressive controls (own log variance, four- and thirteen-week means), log VIX, MSCI EM return, change in log VIX, country-by-year and calendar-month fixed effects, moving-holiday dummies; week-clustered t unless stated.\n\n| Specification | N | Coefficient | t |\n|---|---|---|---|\n| Baseline without holiday dummies | 1507 | -0.075 | -2.61 |\n| With holiday dummies (reference) | 1507 | -0.065 | -2.27 |\n| Per-trading-day variance target | 1507 | -0.065 | -2.25 |\n| Driscoll-Kraay(4) errors | 1507 | -0.065 | -2.60 |\n| Moving-block bootstrap, 500 draws | 1507 | -0.065 (SE 0.024; CI -0.104 to -0.013) | -2.70 |\n| With stringency change and fuel proxy | 1507 | -0.065 | -2.21 |\n| Absolute innovation | 1507 | 0.055 | 1.27 |\n| Positive part / negative part | 1507 | -0.031 / -0.087 | -0.56 / -1.83 |\n| Within 2020 H2 / 2021 / 2022 | 286 / 583 / 572 | -0.081 / -0.029 / -0.019 | -1.51 / -0.73 / -0.37 |\n| Circular block shift placebo, 300 draws | | placebo t mean 0.02, SD 1.08 | 1.0% of draws ≤ actual |\n| Local index target | 724 | -0.047 | -0.79 |\n| Cross-country factor / country residual | 1507 | -0.130 / -0.054 | -1.11 / -1.94 |\n| Signal lagged 52 weeks | 1087 | 0.025 | 0.88 |\n| Real-time seasonal difference | 1087 | -0.053 | -1.84 |\n\nR² without and with the innovation: 0.422 and 0.424. One standard deviation of the innovation moves next-week variance by -6.3 percent and volatility by -3.2 percent.")

# Table 8: 2022 hypothesis (A4 with controls)
T.append("\n\n**Table 8. The 2022 pattern on the seasonally differenced cross-country factor: basket time series.**\nNext-week return (percent) of the equal-weight basket of eleven US-dollar country funds on the real-time seasonally differenced factor (SD units), its interaction with S, S, global controls, holiday shares, and, in the second row of each block, the country-average stringency change and lagged local-currency oil price with their state interactions; HAC(4).\n\n| Sample | Controls | N | F, calm | t | F × S | t |\n|---|---|---|---|---|---|---|\n| 2022 | holidays | 52 | -0.63 | -0.84 | 2.00 | 2.44 |\n| 2022 | + stringency, fuel | 52 | -0.41 | -0.57 | 1.69 | 2.28 |\n| July 2020 to February 2023 | holidays | 100 | -0.06 | -0.39 | 0.98 | 2.19 |\n| July 2020 to February 2023 | + stringency, fuel | 100 | -0.02 | -0.15 | 1.00 | 2.23 |\n| 2021 | holidays | 41 | 0.01 | 0.05 | -1.26 | -0.35 |\n| 2021 | + stringency, fuel | 41 | 0.20 | 1.08 | -7.90 | -1.89 |")

open(os.path.join(PP, "TABLES_v4.md"), "w", encoding="utf-8").write("\n".join(T))

# Turkey box
rb = importlib.import_module("09_robustness"); mt = importlib.import_module("10_main_tables"); d12 = importlib.import_module("12_decisive_reestimation")
w = mt.prep().sort_values(["country", "date"]); w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]; w, HC = d12.add_holidays(w); w["mo"] = w["moy"].astype(str); w["log_vix_lvl"] = np.log(w["vix"])
tr = rb.exlock(w[w.country == "Turkey"]).dropna(subset=["lrv_etf_f1", "x_raw"]).copy().reset_index(drop=True)
rv = d12.fit(tr, "lrv_etf_f1", [("x", tr["x_raw"])], ["year", "mo"], ["lrv_etf", "lrv_etf_m4", "lrv_etf_m13", "log_vix_lvl", "ret_em", "d_vix"] + HC)
bc = pd.read_csv(os.path.join(RT, "table_bycountry.csv")); bt = bc[bc.country == "Turkey"].iloc[0]
sc = pd.read_csv(os.path.join(RT, "table_single_country.csv")); st = sc[sc.country == "Turkey"]
s2t = s2[(s2.level == "country") & (s2.name == "Turkey")].iloc[0]
box = (f"Turkey: 10 cities; ac(52) {s2t['ac52']:.2f}; Fourier R2 {s2t['r2_fourier3']:.2f} (p {s2t['F_p']:.2f}); Google corr ex-lockdown 0.82; "
       f"state interaction (USD, calendar-month FE, HAC) {bt['b_inter']:.3f} (t {bt['t_inter']:.2f}), calm {bt['b_calm']:.3f} (t {bt['t_calm']:.2f}); "
       f"single-country local index actual/placebo/seasonal-diff b,t: " + "; ".join(f"{r['target']}: {r['b_act']:.2f} ({r['t_act']:.2f}) / {r['b_pl']:.2f} ({r['t_pl']:.2f}) / {r['b_sd']:.2f} ({r['t_sd']:.2f})" for _, r in st.iterrows()) +
       f"; volatility (Turkey only, year+month FE, holidays, HAC) {rv['b_x']:.3f} (t {rv['t_x']:.2f}), n {rv['n']}")
open(os.path.join(RT, "turkey_box.md"), "w", encoding="utf-8").write(box); print(box)
print("tables written:", len("\n".join(T).split()), "words")
