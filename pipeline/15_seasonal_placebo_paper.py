"""
Step 15: core tables for the data-and-methods paper.

A. Seasonality diagnosis: autocorrelation at lags 1, 4, 52 of the weekly congestion innovation
   (raw, weekday-adjusted) at city, country and factor level; share of variance explained by
   week-of-year means (in-sample R2 of a week-of-year regression); same for Google workplaces.
B. Single-country "naive" regressions in the style of the prior literature, for each of the 12
   countries: next-week local-index (and USD ETF) return on the country's congestion innovation,
   with own return and global controls, HAC(4). Three versions: (i) actual signal, (ii) 52-week
   lagged signal (placebo), (iii) real-time seasonally differenced signal x_t - x_{t-52}.
   Report the count of |t| > 1.96 across countries in each version, pooled panel versions too.
C. The state-interaction example (eq. 3 of v2) under (i)-(iii), USD ETF, panel.
D. Google validation ex-lockdown: correlation of weekly innovations by country, ex-lockdown and
   post-2021-07.
E. Volatility: country innovation and next-week log RV under (i)-(iii).
Outputs: results/tables/table_methods_paper.md (+ CSVs)
Run: py -I pipeline/15_seasonal_placebo_paper.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
mt = importlib.import_module("10_main_tables")
d12 = importlib.import_module("12_decisive_reestimation")
P = os.path.join(ROOT, "data_proc"); RT = os.path.join(ROOT, "results", "tables")
md = ["# Core tables for the data-and-methods paper\n"]
LOCK = rb.LOCK


def exlock(d):
    return d[(d.date < LOCK[0]) | (d.date > LOCK[1])]


def ac(s, lag):
    s = s.dropna(); return s.autocorr(lag) if len(s) > lag + 10 else np.nan


def woy_r2(s):
    s = s.dropna(); woy = s.index.isocalendar().week.astype(int)
    m = s.groupby(woy.values).transform("mean"); return 1 - ((s - m) ** 2).sum() / ((s - s.mean()) ** 2).sum()


w = mt.prep().sort_values(["country", "date"])
w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]; w, HC = d12.add_holidays(w)
w["F"] = w.groupby("date")["x_raw"].transform("mean"); w["log_vix_lvl"] = np.log(w["vix"])
raw = rb.W[rb.W.country.isin(rb.MAIN)][["date", "country", "ret_etf_f1", "ret_idx_f1"]].rename(columns={"ret_etf_f1": "rr_etf", "ret_idx_f1": "rr_idx"})
w = w.merge(raw, on=["date", "country"], how="left")
w["x52"] = w.groupby("country")["x_raw"].shift(52); w["x_sd"] = w["x_raw"] - w["x52"]
w["x_sd"] = w.groupby("country")["x_sd"].transform(lambda s: s / s.std())
base = exlock(w)

# ---------------- A. seasonality diagnosis
cityw = pd.read_csv(os.path.join(P, "city_daily.csv"), parse_dates=["date"])
cityw = cityw[cityw.country.isin(rb.MAIN)].set_index("date").groupby(["country", "city"])["log_c_dowadj"].resample("W-FRI").mean().reset_index()
cityw["innov"] = cityw.groupby(["country", "city"])["log_c_dowadj"].transform(lambda s: s - s.rolling(4).mean().shift(1))
rows = []
for (c, ci), g in cityw.groupby(["country", "city"]):
    s = g.set_index("date")["innov"]; s = s[(s.index < LOCK[0]) | (s.index > LOCK[1])]
    rows.append({"level": "city", "name": f"{c}/{ci}", "ac1": ac(s, 1), "ac4": ac(s, 4), "ac52": ac(s, 52), "woy_r2": woy_r2(s)})
for c, g in base.groupby("country"):
    s = g.set_index("date")["x_raw"]; rows.append({"level": "country", "name": c, "ac1": ac(s, 1), "ac4": ac(s, 4), "ac52": ac(s, 52), "woy_r2": woy_r2(s)})
Fs = base.groupby("date")["F"].first(); rows.append({"level": "factor", "name": "EM factor", "ac1": ac(Fs, 1), "ac4": ac(Fs, 4), "ac52": ac(Fs, 52), "woy_r2": woy_r2(Fs)})
gpath = os.path.join(P, "google_mobility_daily.csv")
if os.path.exists(gpath):
    g = pd.read_csv(gpath, parse_dates=["date"]); gw = g.set_index("date").groupby("country")["gm_work"].resample("W-FRI").mean().reset_index()
    gw["innov"] = gw.groupby("country")["gm_work"].transform(lambda s: s - s.rolling(4).mean().shift(1))
    for c, gg in gw.groupby("country"):
        s = gg.set_index("date")["innov"]; s = s[(s.index < LOCK[0]) | (s.index > LOCK[1])]
        rows.append({"level": "google_country", "name": c, "ac1": ac(s, 1), "ac4": ac(s, 4), "ac52": ac(s, 52), "woy_r2": woy_r2(s)})
    gF = gw.set_index("date").groupby("date")["innov"].mean(); gF = gF[(gF.index < LOCK[0]) | (gF.index > LOCK[1])]
    rows.append({"level": "google_factor", "name": "Google factor", "ac1": ac(gF, 1), "ac4": ac(gF, 4), "ac52": ac(gF, 52), "woy_r2": woy_r2(gF)})
A = pd.DataFrame(rows); A.to_csv(os.path.join(RT, "table_seasonality_diag.csv"), index=False)
md.append("## A. Seasonality diagnosis of weekly innovations (ex-lockdown): autocorrelations and share of variance explained by week-of-year\n\n| level | n | mean ac(1) | mean ac(4) | mean ac(52) | share ac(52) > 0.2 | mean week-of-year R2 |\n|---|---:|---:|---:|---:|---:|---:|")
for lev, g in A.groupby("level", sort=False):
    md.append(f"| {lev} | {len(g)} | {g.ac1.mean():.2f} | {g.ac4.mean():.2f} | {g.ac52.mean():.2f} | {(g.ac52 > 0.2).mean():.2f} | {g.woy_r2.mean():.2f} |")
md.append("\nCountry detail (congestion): " + "; ".join(f"{r['name']} ac52={r['ac52']:.2f}" for _, r in A[A.level == "country"].iterrows()))

# ---------------- B. single-country naive regressions
CTRL = ["ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]


def naive(d, tgt, x, own):
    d = d.dropna(subset=[tgt, x, own] + CTRL)
    if len(d) < 40: return np.nan, np.nan, len(d)
    X = sm.add_constant(d[[x, own] + CTRL].values); m = sm.OLS(d[tgt].values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    return m.params[1], m.tvalues[1], len(d)


md.append("\n## B. Single-country regressions of next-week return on the country congestion innovation (HAC 4), ex-lockdown\n\n| country | target | actual b | t | 52-wk placebo b | t | real-time seasonal diff b | t |\n|---|---|---:|---:|---:|---:|---:|---:|")
Brows = []
for tgt, own, tname in (("rr_idx", "ret_idx", "local index"), ("rr_etf", "ret_etf", "USD ETF")):
    for c, g in base.groupby("country"):
        g = g.copy(); g["y"] = g[tgt] * 100
        a = naive(g, "y", "x_raw", own); p = naive(g, "y", "x52", own); s = naive(g, "y", "x_sd", own)
        Brows.append({"country": c, "target": tname, "b_act": a[0], "t_act": a[1], "b_pl": p[0], "t_pl": p[1], "b_sd": s[0], "t_sd": s[1], "n_act": a[2], "n_pl": p[2]})
        if not np.isnan(a[1]):
            md.append(f"| {c} | {tname} | {a[0]:.3f} | {a[1]:.2f} | {p[0]:.3f} | {p[1]:.2f} | {s[0]:.3f} | {s[1]:.2f} |")
B = pd.DataFrame(Brows); B.to_csv(os.path.join(RT, "table_single_country.csv"), index=False)
for tname in ("local index", "USD ETF"):
    bb = B[B.target == tname].dropna(subset=["t_act"])
    md.append(f"\n{tname}: countries with |t|>1.96: actual {int((bb.t_act.abs()>1.96).sum())}/{len(bb)}, placebo {int((bb.t_pl.abs()>1.96).sum())}/{len(bb)}, seasonal-diff {int((bb.t_sd.abs()>1.96).sum())}/{len(bb)}; mean |t|: {bb.t_act.abs().mean():.2f} / {bb.t_pl.abs().mean():.2f} / {bb.t_sd.abs().mean():.2f}")

# pooled unconditional panel versions (country x month FE, week cluster), percent returns
md.append("\n### Pooled panel, next-week return (%) on signal, country x month FE, week-clustered\n\n| target | version | n | b | t |\n|---|---|---:|---:|---:|")
for tgt, own, tname in (("rr_idx", "ret_idx", "local index"), ("rr_etf", "ret_etf", "USD ETF")):
    for ver, x in (("actual", "x_raw"), ("52-wk placebo", "x52"), ("seasonal diff", "x_sd")):
        d = base.dropna(subset=[tgt, x, own] + CTRL).copy(); d["y"] = 100 * d[tgt]
        r = d12.fit(d, "y", [("x", d[x])], ["cm"], [own] + CTRL)
        md.append(f"| {tname} | {ver} | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} |")

# ---------------- C. the state-interaction example under the three versions
md.append("\n## C. The state-dependent specification (eq. 3, USD ETF, SD units, full FE and controls) under the three signal versions\n\n| version | n | x calm | t | x x S | t |\n|---|---:|---:|---:|---:|---:|")
for ver, x in (("actual (raw)", "x_raw"), ("52-wk placebo", "x52"), ("real-time seasonal diff", "x_sd")):
    d = base.dropna(subset=[x]).copy(); d["sm"] = "S" + d["S_vix25"].astype(int).astype(str) + "_" + d["moy"].astype(str)
    ctrl = ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]
    for c in ctrl: d[c + "_S"] = d[c] * d["S_vix25"]
    r = d12.fit(d, "ret_etf_f1", [("x", d[x]), ("xS", d[x] * d["S_vix25"]), ("S", d["S_vix25"])], ["cy", "sm"], ctrl + [c + "_S" for c in ctrl] + HC + ["log_vix_lvl"])
    md.append(f"| {ver} | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} | {r['b_xS']:.3f} | {r['t_xS']:.2f} |")
# like-for-like actual on the placebo sample
d = base.dropna(subset=["x52"]).copy(); d["sm"] = "S" + d["S_vix25"].astype(int).astype(str) + "_" + d["moy"].astype(str)
for c in ctrl: d[c + "_S"] = d[c] * d["S_vix25"]
r = d12.fit(d, "ret_etf_f1", [("x", d["x_raw"]), ("xS", d["x_raw"] * d["S_vix25"]), ("S", d["S_vix25"])], ["cy", "sm"], ctrl + [c + "_S" for c in ctrl] + HC + ["log_vix_lvl"])
md.append(f"| actual, placebo sample | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} | {r['b_xS']:.3f} | {r['t_xS']:.2f} |")

# ---------------- D. Google validation by country, ex-lockdown and post-2021-07
if os.path.exists(gpath):
    gw["gm_innov"] = gw["innov"]; wg = w.merge(gw[["date", "country", "gm_innov"]], on=["date", "country"], how="inner")
    md.append("\n## D. Correlation of weekly innovations, congestion vs Google workplaces mobility\n\n| country | all overlap | ex-lockdown | post-2021-07 |\n|---|---:|---:|---:|")
    for c, g in wg.groupby("country"):
        a = g[["x_raw", "gm_innov"]].corr().iloc[0, 1]; e = exlock(g)[["x_raw", "gm_innov"]].corr().iloc[0, 1]; p = g[g.date >= "2021-07-01"][["x_raw", "gm_innov"]].corr().iloc[0, 1]
        md.append(f"| {c} | {a:.2f} | {e:.2f} | {p:.2f} |")
    md.append(f"| pooled | {wg[['x_raw','gm_innov']].corr().iloc[0,1]:.2f} | {exlock(wg)[['x_raw','gm_innov']].corr().iloc[0,1]:.2f} | {wg[wg.date>='2021-07-01'][['x_raw','gm_innov']].corr().iloc[0,1]:.2f} |")

# ---------------- E. volatility under three versions
md.append("\n## E. Next-week log realized variance (USD ETF) on the country signal, HAR + log VIX, country x year + month FE\n\n| version | n | b | t |\n|---|---:|---:|---:|")
for ver, x in (("actual", "x_raw"), ("52-wk placebo", "x52"), ("seasonal diff", "x_sd")):
    d = base.dropna(subset=[x, "lrv_etf_f1"]).copy(); d["mo"] = d["moy"].astype(str)
    r = d12.fit(d, "lrv_etf_f1", [("x", d[x])], ["cy", "mo"], ["lrv_etf", "lrv_etf_m4", "lrv_etf_m13", "log_vix", "ret_em", "d_vix"])
    md.append(f"| {ver} | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} |")

txt = "\n".join(md); open(os.path.join(RT, "table_methods_paper.md"), "w", encoding="utf-8").write(txt); print(txt)
