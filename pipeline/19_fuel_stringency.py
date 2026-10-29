"""
Step 19: non-seasonal confounders (round-2 item K6).
Controls:
  strin   Oxford stringency index (national, daily -> weekly mean), and d_strin (weekly change)
  fuel    local-currency oil price proxy: log Brent (USD) + log(local per USD), weekly change,
          lagged one week (pump prices adjust with a lag); flagged as a proxy for retail fuel
Specs re-run with [x, x*S, S] + base controls + holiday dummies + {d_strin, fuel, each x S}:
  eq. (1) state example, three signal versions, USD ETF, ex-lockdown
  eq. (1) dropping weeks with |d_strin| > 10 points
  volatility B2 spec + {d_strin, fuel}
  A4 2022 basket time series on the seasonally differenced factor + country-average d_strin, fuel
Outputs: results/tables/fuel_stringency.md, data_proc/stringency_weekly.csv
Run: py -I pipeline/19_fuel_stringency.py
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
P = os.path.join(ROOT, "data_proc"); RT = os.path.join(ROOT, "results", "tables"); RAW = os.path.join(ROOT, "data_raw")
LOCK = rb.LOCK
ISO3 = {"Turkey": "TUR", "Poland": "POL", "Brazil": "BRA", "South Africa": "ZAF", "India": "IND", "Saudi Arabia": "SAU", "Mexico": "MEX",
        "Indonesia": "IDN", "Thailand": "THA", "Egypt": "EGY", "Malaysia": "MYS", "Philippines": "PHL"}
md = ["# Fuel-price proxy and Oxford stringency controls\n"]

# ---------------- stringency
ox = pd.read_csv(os.path.join(RAW, "OxCGRT_compact_national.csv"), usecols=["CountryCode", "Date", "StringencyIndex_Average"], low_memory=False)
ox = ox[ox.CountryCode.isin(ISO3.values())].copy(); ox["date"] = pd.to_datetime(ox["Date"].astype(str), format="%Y%m%d")
inv = {v: k for k, v in ISO3.items()}; ox["country"] = ox.CountryCode.map(inv)
sw = ox.set_index("date").groupby("country")["StringencyIndex_Average"].resample("W-FRI").mean().rename("strin").reset_index()
sw["d_strin"] = sw.groupby("country")["strin"].diff(); sw.to_csv(os.path.join(P, "stringency_weekly.csv"), index=False)
md.append(f"Stringency: {sw.country.nunique()} countries, {sw.date.min().date()} to {sw.date.max().date()}; share of ex-lockdown weeks with |d_strin| > 10: {((sw.d_strin.abs() > 10) & ((sw.date < LOCK[0]) | (sw.date > LOCK[1]))).mean():.3f}")

# ---------------- fuel proxy
mk = rb.mk
fx = mk[mk.series == "fx"].pivot_table(index="date", columns="country", values="value").sort_index()
brent = mk[(mk.country == "GLOBAL") & (mk.series == "brent")].set_index("date")["value"].sort_index()
fuelw = []
for c in ISO3:
    if c not in fx: continue
    lp = (np.log(brent) + np.log(fx[c].reindex(brent.index).ffill())).resample("W-FRI").last().diff()
    fuelw.append(pd.DataFrame({"date": lp.index, "country": c, "fuel": lp.values}))
fuelw = pd.concat(fuelw); fuelw["fuel_l1"] = fuelw.groupby("country")["fuel"].shift(1)

# ---------------- panel
w = mt.prep().sort_values(["country", "date"]); w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]
w, HC = d12.add_holidays(w); w["mo"] = w["moy"].astype(str); w["log_vix_lvl"] = np.log(w["vix"])
w["F"] = w.groupby("date")["x_raw"].transform("mean")
w["x52"] = w.groupby("country")["x_raw"].shift(52); w["x_sd"] = (w["x_raw"] - w["x52"]); w["x_sd"] = w["x_sd"] / w["x_sd"].std()
w = w.merge(sw[["date", "country", "strin", "d_strin"]], on=["date", "country"], how="left").merge(fuelw, on=["date", "country"], how="left")
w["d_strin"] = w["d_strin"].fillna(0); w["strin"] = w.groupby("country")["strin"].ffill()
base = rb.exlock(w).copy()
CTRL = ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]
NEW = ["d_strin", "fuel_l1"]


def state(d, x, extra_new=(), fe=("cy", "sm")):
    d = d.dropna(subset=[x, "ret_etf_f1"] + list(extra_new)).copy().reset_index(drop=True)
    d["sm"] = "S" + d["S_vix25"].astype(int).astype(str) + "_" + d["moy"].astype(str)
    ctrl = CTRL + list(extra_new)
    for c in ctrl: d[c + "_S"] = d[c] * d["S_vix25"]
    return d12.fit(d, "ret_etf_f1", [("x", d[x]), ("xS", d[x] * d["S_vix25"]), ("S", d["S_vix25"])], list(fe), ctrl + [c + "_S" for c in ctrl] + HC + ["log_vix_lvl"])


md.append("\n## Eq. (1), USD ETF, ex-lockdown, holiday dummies, with and without stringency change and lagged local-currency oil price (each also x S)\n\n| signal | controls | n | calm | t | inter | t |\n|---|---|---:|---:|---:|---:|---:|")
for lab, x in (("actual", "x_raw"), ("lag-52 placebo", "x52"), ("seasonal diff", "x_sd")):
    for clab, ex in (("baseline", ()), ("+ stringency + fuel", NEW)):
        r = state(base, x, ex); md.append(f"| {lab} | {clab} | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} | {r['b_xS']:.3f} | {r['t_xS']:.2f} |")
dd = base[base.d_strin.abs() <= 10]
r = state(dd, "x_raw", NEW); md.append(f"| actual | + controls, drop weeks with abs(d_strin) > 10 | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} | {r['b_xS']:.3f} | {r['t_xS']:.2f} |")
r = state(base, "x_raw", NEW + ["strin"]); md.append(f"| actual | + controls + stringency level | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} | {r['b_xS']:.3f} | {r['t_xS']:.2f} |")
# coefficient on the new controls themselves (actual spec)
d = base.dropna(subset=["x_raw", "ret_etf_f1"] + NEW).copy().reset_index(drop=True); d["sm"] = "S" + d["S_vix25"].astype(int).astype(str) + "_" + d["moy"].astype(str)
ctrl = CTRL + NEW
for c in ctrl: d[c + "_S"] = d[c] * d["S_vix25"]
r = d12.fit(d, "ret_etf_f1", [("x", d["x_raw"]), ("xS", d["x_raw"] * d["S_vix25"]), ("S", d["S_vix25"]), ("d_strin", d["d_strin"]), ("fuel_l1", d["fuel_l1"]), ("d_strin_S", d["d_strin"] * d["S_vix25"]), ("fuel_S", d["fuel_l1"] * d["S_vix25"])],
            ["cy", "sm"], [c for c in CTRL] + [c + "_S" for c in CTRL] + HC + ["log_vix_lvl"])
md.append(f"\nControls' own coefficients (actual spec): d_strin {r['b_d_strin']:.4f} (t {r['t_d_strin']:.2f}), d_strin x S {r['b_d_strin_S']:.4f} (t {r['t_d_strin_S']:.2f}); fuel_l1 {r['b_fuel_l1']:.3f} (t {r['t_fuel_l1']:.2f}), fuel x S {r['b_fuel_S']:.3f} (t {r['t_fuel_S']:.2f}). Correlation of x with d_strin: {base[['x_raw','d_strin']].corr().iloc[0,1]:.3f}; with fuel_l1: {base[['x_raw','fuel_l1']].corr().iloc[0,1]:.3f}")

# ---------------- volatility B2 + new controls
VC = ["lrv_etf", "lrv_etf_m4", "lrv_etf_m13", "log_vix_lvl", "ret_em", "d_vix"]
md.append("\n## Volatility (B2 spec) with stringency and fuel\n\n| controls | n | x | t |\n|---|---:|---:|---:|")
for clab, ex in (("baseline + holidays", ()), ("+ stringency + fuel", NEW)):
    d = base.dropna(subset=["lrv_etf_f1", "x_raw"] + list(ex)).copy().reset_index(drop=True)
    r = d12.fit(d, "lrv_etf_f1", [("x", d["x_raw"])], ["cy", "mo"], VC + HC + list(ex)); md.append(f"| {clab} | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} |")

# ---------------- A4 2022 time series with country-average controls
raw = rb.W[rb.W.country.isin(rb.MAIN)][["date", "country", "ret_etf_f1"]].rename(columns={"ret_etf_f1": "rr"})
wb = w.merge(raw, on=["date", "country"], how="left")
bk = wb.groupby("date").agg(F=("F", "first"), S=("S_vix25", "first"), r=("rr", "mean"), ret_em=("ret_em", "first"), d_vix=("d_vix", "first"), brent=("ret_brent", "first"),
                            dxy=("d_dxy", "first"), us10=("d_us10y", "first"), lvix=("log_vix_lvl", "first"), d_strin=("d_strin", "mean"), fuel_l1=("fuel_l1", "mean")).join(wb.groupby("date")[HC].mean()).dropna(subset=["F", "r"])
bk["F52"] = bk["F"].shift(52); ex_ = bk[(bk.index < LOCK[0]) | (bk.index > LOCK[1])]; sd_ex = (ex_["F"] - ex_["F52"]).std(); bk["F_sd"] = (bk["F"] - bk["F52"]) / sd_ex
ex_ = bk[(bk.index < LOCK[0]) | (bk.index > LOCK[1])]
md.append("\n## A4 basket time series on the seasonally differenced factor, with holiday shares, stringency and fuel (HAC 4)\n\n| sample | controls | n | F calm | t | F x S | t |\n|---|---|---:|---:|---:|---:|---:|")
def ts(d, newc):
    d = d.dropna(subset=["F_sd"] + newc); cols = [d["F_sd"], d["F_sd"] * d.S, d.S, d.ret_em, d.d_vix, d.brent, d.dxy, d.us10, d.lvix] + [d[h] for h in HC] + [d[c] for c in newc] + [d[c] * d.S for c in newc]
    X = sm.add_constant(np.column_stack(cols)); m = sm.OLS(100 * d.r.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4}); return len(d), m.params[1], m.tvalues[1], m.params[2], m.tvalues[2]
for s_, d in (("2022", ex_[ex_.index.year == 2022]), ("ex-lockdown", ex_), ("2021", ex_[ex_.index.year == 2021])):
    for clab, nc in (("holidays only", []), ("+ stringency + fuel", ["d_strin", "fuel_l1"])):
        n, b1, t1, b2, t2 = ts(d, nc); md.append(f"| {s_} | {clab} | {n} | {b1:.2f} | {t1:.2f} | {b2:.2f} | {t2:.2f} |")
txt = "\n".join(md); open(os.path.join(RT, "fuel_stringency.md"), "w", encoding="utf-8").write(txt); print(txt)
