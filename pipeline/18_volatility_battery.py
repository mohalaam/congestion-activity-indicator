"""
Step 18: volatility battery (round-2 item K3).
Target: next-week log realized variance of USD country-fund returns (and local index).
Baseline (v3 Table 7): x on lrv_f1 with own lrv, 4- and 13-week means, log VIX, MSCI EM return,
dVIX, country x year and calendar-month FE, week-clustered SE.
Battery:
  B1  baseline (signed x)                      B2  + moving-holiday dummies
  B3  per-trading-day variance target          B4  Driscoll-Kraay(4) errors on B2
  B5  moving-block bootstrap SE (8 wk, 500)    B6  |x| instead of x
  B7  x split into positive and negative parts B8  by year: 2020H2, 2021, 2022
  B9  circular block shift placebo (300)       B10 local index target, B2 spec
  B11 factor F and residual e, B2 spec         B12 52-week lag placebo and seasonal diff, B2 spec
  B13 economic size: R2 increment and SD of fitted contribution
Outputs: results/tables/volatility_battery.md, volatility_battery.csv
Run: py -I pipeline/18_volatility_battery.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
rng = np.random.default_rng(18)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
mt = importlib.import_module("10_main_tables")
d12 = importlib.import_module("12_decisive_reestimation")
P = os.path.join(ROOT, "data_proc"); RT = os.path.join(ROOT, "results", "tables")
LOCK = rb.LOCK
md = ["# Volatility battery (next-week log realized variance)\n"]
rows = []

w = mt.prep().sort_values(["country", "date"]); w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]
w, HC = d12.add_holidays(w); w["mo"] = w["moy"].astype(str); w["log_vix_lvl"] = np.log(w["vix"])
w["F"] = w.groupby("date")["x_raw"].transform("mean"); w["e"] = w["x_raw"] - w["F"]
w["x52"] = w.groupby("country")["x_raw"].shift(52); w["x_sd"] = (w["x_raw"] - w["x52"]); w["x_sd"] = w["x_sd"] / w["x_sd"].std()
w["abs_x"] = w["x_raw"].abs(); w["x_pos"] = w["x_raw"].clip(lower=0); w["x_neg"] = w["x_raw"].clip(upper=0)
# trading days per week from daily ETF prices
mk = rb.mk
for name, series in (("etf", "etf_usd"), ("idx", "index")):
    px = mk[mk.series == series].pivot_table(index="date", columns="country", values="value").sort_index()
    nd = np.log(px).diff().notna().resample("W-FRI").sum().stack().rename(f"nd_{name}").reset_index().rename(columns={"level_1": "country"})
    w = w.merge(nd, on=["date", "country"], how="left")
    w[f"lrv_{name}_pd_f1"] = w.groupby("country")[f"lrv_{name}"].shift(-1) - np.log(w.groupby("country")[f"nd_{name}"].shift(-1).replace(0, np.nan))
base = rb.exlock(w)
CTRL = {"etf": ["lrv_etf", "lrv_etf_m4", "lrv_etf_m13", "log_vix_lvl", "ret_em", "d_vix"], "idx": ["lrv_idx", "lrv_idx_m4", "lrv_idx_m13", "log_vix_lvl", "ret_em", "d_vix"]}


def vol(d, xs, tgt="lrv_etf_f1", ctrl=None, fe=("cy", "mo"), extra=(), dk=None):
    d = d.dropna(subset=[tgt] + xs).copy().reset_index(drop=True)
    ctrl = list(ctrl or CTRL["etf"]) + list(extra)
    return d12.fit(d, tgt, [(x, d[x]) for x in xs], list(fe), ctrl, dk_lags=dk)


def add(label, r, keys=("x_raw",)):
    rec = {"spec": label, "n": r["n"]}
    for k in keys:
        rec[f"b_{k}"] = r.get(f"b_{k}", np.nan); rec[f"t_{k}"] = r.get(f"t_{k}", np.nan)
    rows.append(rec); return rec


md.append("| spec | n | coefficient(s) | t |\n|---|---:|---|---|")
def line(label, r, keys=("x_raw",)):
    md.append(f"| {label} | {r['n']} | " + "; ".join(f"{k}: {r[f'b_{k}']:.3f}" for k in keys) + " | " + "; ".join(f"{r[f't_{k}']:.2f}" for k in keys) + " |")

r = vol(base, ["x_raw"]); add("B1 baseline, signed x", r); line("B1 baseline, signed x", r)
r = vol(base, ["x_raw"], extra=HC); add("B2 + holiday dummies", r); line("B2 + holiday dummies", r)
r = vol(base, ["x_raw"], tgt="lrv_etf_pd_f1", extra=HC); add("B3 per-trading-day variance + holidays", r); line("B3 per-trading-day variance + holidays", r)
r = vol(base, ["x_raw"], extra=HC, dk=4); add("B4 Driscoll-Kraay(4), B2 spec", r); line("B4 Driscoll-Kraay(4), B2 spec", r)
# B5 block bootstrap on B2
d0 = base.dropna(subset=["lrv_etf_f1", "x_raw"] + CTRL["etf"]).copy()
weeks = np.array(sorted(d0.date.unique())); byw = {t: g for t, g in d0.groupby("date")}; boots = []
for b in range(500):
    starts = rng.integers(0, len(weeks) - 8 + 1, size=int(np.ceil(len(weeks) / 8))); sel = np.concatenate([weeks[s:s + 8] for s in starts])[:len(weeks)]
    try: boots.append(vol(pd.concat([byw[t] for t in sel]), ["x_raw"], extra=HC)["b_x_raw"])
    except Exception: pass
boots = np.array(boots); pt = vol(base, ["x_raw"], extra=HC)["b_x_raw"]
md.append(f"| B5 moving-block bootstrap (8 wk, {len(boots)} draws), B2 spec | {d0.shape[0]} | x_raw: {pt:.3f}; boot SE {boots.std():.3f}; 95% CI [{np.percentile(boots,2.5):.3f}, {np.percentile(boots,97.5):.3f}] | {pt/boots.std():.2f} |")
rows.append({"spec": "B5 block bootstrap", "n": d0.shape[0], "b_x_raw": pt, "t_x_raw": pt / boots.std()})
r = vol(base, ["abs_x"], extra=HC); add("B6 |x|", r, ("abs_x",)); line("B6 |x| (resolution of uncertainty)", r, ("abs_x",))
r = vol(base, ["x_pos", "x_neg"], extra=HC); add("B7 split", r, ("x_pos", "x_neg")); line("B7 x+ and x- separately", r, ("x_pos", "x_neg"))
for lab, d in (("2020 H2", base[(base.date >= "2020-07-01") & (base.date <= "2020-12-31")]), ("2021", base[base.year == "2021"]), ("2022", base[base.year == "2022"])):
    try:
        r = vol(d, ["x_raw"], fe=("country", "mo"), extra=HC); add(f"B8 {lab}", r); line(f"B8 within {lab} (country + month FE)", r)
    except Exception as ex: md.append(f"| B8 {lab} | failed {ex} | | |")
# B9 circular shift
Fw = base.pivot_table(index="date", columns="country", values="x_raw"); wk = Fw.index; look0 = Fw.stack().to_dict(); ts = []
act = vol(base, ["x_raw"], extra=HC)["t_x_raw"]
for k in range(300):
    sh = int(rng.integers(8, len(wk) - 8)); Fs = pd.DataFrame(np.roll(Fw.values, sh, axis=0), index=wk, columns=Fw.columns); look = Fs.stack().to_dict()
    dp = base.copy(); dp["x_raw"] = [look.get((t, c), np.nan) for t, c in zip(dp.date, dp.country)]
    try: ts.append(vol(dp, ["x_raw"], extra=HC)["t_x_raw"])
    except Exception: pass
ts = np.array(ts)
md.append(f"| B9 circular block shift placebo (300) | | actual t {act:.2f}; placebo mean {ts.mean():.2f}, SD {ts.std():.2f} | share <= actual {(ts <= act).mean():.3f} |")
r = vol(base, ["x_raw"], tgt="lrv_idx_f1", ctrl=CTRL["idx"], extra=HC); add("B10 local index", r); line("B10 local index target, B2 spec", r)
r = vol(base, ["F", "e"], extra=HC); add("B11 F and e", r, ("F", "e")); line("B11 factor F and residual e, B2 spec", r, ("F", "e"))
r = vol(base, ["x52"], extra=HC); add("B12 lag-52 placebo", r, ("x52",)); line("B12 52-week lag placebo, B2 spec", r, ("x52",))
r = vol(base, ["x_sd"], extra=HC); add("B12 seasonal diff", r, ("x_sd",)); line("B12 real-time seasonal difference, B2 spec", r, ("x_sd",))
# B13 economic size
d = base.dropna(subset=["lrv_etf_f1", "x_raw"] + CTRL["etf"]).copy().reset_index(drop=True)
X0 = pd.concat([d[CTRL["etf"] + HC], pd.get_dummies(d["cy"]).astype(float), pd.get_dummies(d["mo"]).astype(float)], axis=1)
m0 = sm.OLS(d["lrv_etf_f1"].values, X0.values).fit(); m1 = sm.OLS(d["lrv_etf_f1"].values, pd.concat([d[["x_raw"]], X0], axis=1).values).fit()
md.append(f"\nB13 economic size: R2 {m0.rsquared:.3f} without x vs {m1.rsquared:.3f} with x (increment {m1.rsquared-m0.rsquared:.4f}); SD of next-week log RV {d['lrv_etf_f1'].std():.2f}; a 1-SD x moves it by {m1.params[0]:.3f} log points = {100*(np.exp(m1.params[0])-1):.1f}% of variance, {100*(np.exp(m1.params[0]/2)-1):.1f}% of volatility.")
pd.DataFrame(rows).to_csv(os.path.join(RT, "volatility_battery.csv"), index=False)
txt = "\n".join(md); open(os.path.join(RT, "volatility_battery.md"), "w", encoding="utf-8").write(txt); print(txt)
