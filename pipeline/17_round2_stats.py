"""
Step 17: round-2 statistics.
1. Seasonality diagnostics per series on a TRUE weekly time index (lockdown weeks set to NaN,
   not removed): in-sample week-of-year R2, adjusted R2, leave-one-year-out R2 (profile fitted
   on the other years), Fourier seasonal (3 harmonics) R2 and F-test p-value, ac(52).
2. Attenuation bound by Monte Carlo: under H_news (returns respond to the actual signal x, which
   is treated as entirely news) simulate y = b*x + b2*x*S + noise calibrated to the observed
   actual-on-placebo-sample fit, then estimate the interaction with (a) actual x, (b) x lagged 52,
   (c) real-time seasonal difference; report expected ratios (b)/(a) and (c)/(a) and compare to
   observed 0.082/0.189 and 0.049/0.189. Also under H_seasonal (returns respond only to the
   in-sample week-of-year component of x) to show what a pure calendar effect would produce.
3. Calendar-preserving placebo: replace each country's x by (i) its own in-sample week-of-year
   mean (pure seasonal component), (ii) another country's week-of-year profile (rotated), and
   (iii) the circular block shift (persistence-preserving, calendar-breaking) already run.
4. Reconcile the 2022 anchor: basket time-series regression on the seasonally differenced
   factor under one standardization (SD of F_sd over the ex-lockdown sample), with and without
   holiday-share dummies; report the number to carry into the pre-registration.
Outputs: results/tables/round2_stats.md, round2_seasonality.csv
Run: py -I pipeline/17_round2_stats.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

warnings.filterwarnings("ignore")
rng = np.random.default_rng(2026)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
mt = importlib.import_module("10_main_tables")
d12 = importlib.import_module("12_decisive_reestimation")
P = os.path.join(ROOT, "data_proc"); RT = os.path.join(ROOT, "results", "tables")
LOCK = rb.LOCK
md = ["# Round-2 statistics\n"]

# ------------------------------------------------------------------ 1. seasonality on a time index
def season_stats(s):
    """s: weekly series indexed by Friday dates, NaN where excluded. Returns dict."""
    s = s.copy(); full = pd.date_range(s.index.min(), s.index.max(), freq="W-FRI"); s = s.reindex(full)
    v = s.dropna(); n = len(v)
    if n < 60:
        return None
    woy = v.index.isocalendar().week.astype(int).values; yr = v.index.year.values
    # in-sample week-of-year R2 and adjusted
    m = pd.Series(v.values).groupby(woy).transform("mean").values
    sst = ((v.values - v.values.mean()) ** 2).sum(); r2 = 1 - ((v.values - m) ** 2).sum() / sst
    k = len(np.unique(woy)); adj = 1 - (1 - r2) * (n - 1) / max(n - k, 1)
    # leave-one-year-out
    pred = np.full(n, np.nan)
    for y in np.unique(yr):
        tr = yr != y; te = yr == y
        prof = pd.Series(v.values[tr]).groupby(woy[tr]).mean()
        pred[te] = pd.Series(woy[te]).map(prof).values
    ok = ~np.isnan(pred); loyo = 1 - ((v.values[ok] - pred[ok]) ** 2).sum() / ((v.values[ok] - v.values[ok].mean()) ** 2).sum()
    # Fourier 3 harmonics
    t = woy / 52.18 * 2 * np.pi
    X = np.column_stack([np.ones(n)] + [f(h * t) for h in (1, 2, 3) for f in (np.sin, np.cos)])
    mf = sm.OLS(v.values, X).fit(); fr2 = mf.rsquared
    fstat = ((sst - mf.ssr) / 6) / (mf.ssr / (n - 7)); fp = 1 - stats.f.cdf(fstat, 6, n - 7)
    # HAC-robust Wald on the 6 Fourier terms
    mh = sm.OLS(v.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4}); R = np.zeros((6, 7)); R[:, 1:] = np.eye(6)
    wp = float(mh.wald_test(R, use_f=False).pvalue)
    # ac(52) on time index
    ac52 = s.autocorr(52); ac1 = s.autocorr(1)
    return {"n": n, "r2_woy": r2, "r2_adj": adj, "r2_loyo": loyo, "r2_fourier3": fr2, "F_p": fp, "Wald_HAC_p": wp, "ac1": ac1, "ac52": ac52}


w = mt.prep().sort_values(["country", "date"]); w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]
w, HC = d12.add_holidays(w); w["log_vix_lvl"] = np.log(w["vix"]); w["F"] = w.groupby("date")["x_raw"].transform("mean")
rows = []
cityw = pd.read_csv(os.path.join(P, "city_daily.csv"), parse_dates=["date"])
cityw = cityw[cityw.country.isin(rb.MAIN)].set_index("date").groupby(["country", "city"])["log_c_dowadj"].resample("W-FRI").mean().reset_index()
cityw["x"] = cityw.groupby(["country", "city"])["log_c_dowadj"].transform(lambda s: s - s.rolling(4).mean().shift(1))
def mask_lock(s):
    s = s.copy(); s[(s.index >= LOCK[0]) & (s.index <= LOCK[1])] = np.nan; return s
for (c, ci), g in cityw.groupby(["country", "city"]):
    r = season_stats(mask_lock(g.set_index("date")["x"]))
    if r: rows.append({"level": "city", "name": f"{c}/{ci}", **r})
for c, g in w.groupby("country"):
    r = season_stats(mask_lock(g.set_index("date")["x_raw"]))
    if r: rows.append({"level": "country", "name": c, **r})
r = season_stats(mask_lock(w.groupby("date")["F"].first())); rows.append({"level": "factor", "name": "EM factor", **r})
gpath = os.path.join(P, "google_mobility_daily.csv")
if os.path.exists(gpath):
    g = pd.read_csv(gpath, parse_dates=["date"]); gw = g.set_index("date").groupby("country")["gm_work"].resample("W-FRI").mean().reset_index()
    gw["x"] = gw.groupby("country")["gm_work"].transform(lambda s: s - s.rolling(4).mean().shift(1))
    for c, gg in gw.groupby("country"):
        r = season_stats(mask_lock(gg.set_index("date")["x"]))
        if r: rows.append({"level": "google_country", "name": c, **r})
    r = season_stats(mask_lock(gw.groupby("date")["x"].mean())); rows.append({"level": "google_factor", "name": "Google factor", **r})
S = pd.DataFrame(rows); S.to_csv(os.path.join(RT, "round2_seasonality.csv"), index=False)
md.append("## 1. Seasonality diagnostics on a true weekly time index (lockdown weeks NaN)\n\n| level | n series | mean n | R2 woy (in-sample) | adj R2 | LOYO R2 | Fourier-3 R2 | share F p<0.05 | share HAC-Wald p<0.05 | mean ac(52) | share ac(52)>0.2 |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for lev, g in S.groupby("level", sort=False):
    md.append(f"| {lev} | {len(g)} | {g.n.mean():.0f} | {g.r2_woy.mean():.2f} | {g.r2_adj.mean():.2f} | {g.r2_loyo.mean():.2f} | {g.r2_fourier3.mean():.2f} | {(g.F_p<0.05).mean():.2f} | {(g.Wald_HAC_p<0.05).mean():.2f} | {g.ac52.mean():.2f} | {(g.ac52>0.2).mean():.2f} |")
md.append("\nCountry detail: " + "; ".join(f"{r['name']}: adj {r['r2_adj']:.2f}, LOYO {r['r2_loyo']:.2f}, Fourier {r['r2_fourier3']:.2f} (p {r['F_p']:.3f}), ac52 {r['ac52']:.2f}" for _, r in S[S.level == "country"].iterrows()))
md.append(f"\nChance level of in-sample R2 with k cells on n obs: about (k-1)/(n-1) = {51/137:.2f} for n=138.")

# ------------------------------------------------------------------ 2. attenuation bound by Monte Carlo
base = rb.exlock(w).copy()
base["x52"] = base.groupby("country")["x_raw"].shift(52); base["x_sd"] = base["x_raw"] - base["x52"]
sd_scale = base["x_sd"].std(); base["x_sd"] = base["x_sd"] / sd_scale
d0 = base.dropna(subset=["x52", "ret_etf_f1"] + ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]).copy().reset_index(drop=True)
d0["sm"] = "S" + d0["S_vix25"].astype(int).astype(str) + "_" + d0["moy"].astype(str)
ctrl = ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]
for c in ctrl: d0[c + "_S"] = d0[c] * d0["S_vix25"]
EXTRA = ctrl + [c + "_S" for c in ctrl] + HC + ["log_vix_lvl"]

def inter(d, x, y="ret_etf_f1"):
    r = d12.fit(d, y, [("x", d[x]), ("xS", d[x] * d["S_vix25"]), ("S", d["S_vix25"])], ["cy", "sm"], EXTRA)
    return r["b_x"], r["b_xS"], r["t_xS"]

obs = {v: inter(d0, v) for v in ("x_raw", "x52", "x_sd")}
md.append("\n## 2. Attenuation bound (placebo-sample, n = %d)\n\nObserved: actual x (calm %.3f, inter %.3f, t %.2f); lag-52 placebo (inter %.3f, t %.2f); seasonal diff (inter %.3f, t %.2f). Observed ratios: placebo/actual = %.2f, seasonal-diff/actual = %.2f."
          % (len(d0), obs["x_raw"][0], obs["x_raw"][1], obs["x_raw"][2], obs["x52"][1], obs["x52"][2], obs["x_sd"][1], obs["x_sd"][2], obs["x52"][1] / obs["x_raw"][1], obs["x_sd"][1] / obs["x_raw"][1]))
# residual noise: fit actual model, take residual SD
Xfit = d12.fit(d0, "ret_etf_f1", [("x", d0["x_raw"]), ("xS", d0["x_raw"] * d0["S_vix25"]), ("S", d0["S_vix25"])], ["cy", "sm"], EXTRA)
b1, b2 = obs["x_raw"][0], obs["x_raw"][1]
resid_sd = np.sqrt(1 - 0.05)  # standardized returns, R2 small; conservative
d0["woy"] = d0.date.dt.isocalendar().week.astype(int)
d0["x_seas"] = d0.groupby(["country", "woy"])["x_raw"].transform("mean")  # in-sample seasonal component
d0["x_seas52"] = d0.groupby("country")["x_seas"].shift(52) if False else d0["x_seas"]  # seasonal component is the same each year by construction
sims = {"H_news (y responds to actual x)": "x_raw", "H_seasonal (y responds to seasonal component of x only)": "x_seas"}
B = 300
for lab, drv in sims.items():
    rat_pl, rat_sd, t_pl, t_sd = [], [], [], []
    for b in range(B):
        y = b1 * d0[drv] + b2 * d0[drv] * d0["S_vix25"] + rng.normal(0, resid_sd, len(d0))
        dd = d0.copy(); dd["ysim"] = y.values
        a = inter(dd, "x_raw", "ysim"); p = inter(dd, "x52", "ysim"); s_ = inter(dd, "x_sd", "ysim")
        rat_pl.append(p[1] / a[1]); rat_sd.append(s_[1] / a[1]); t_pl.append(p[2]); t_sd.append(s_[2])
    rat_pl, rat_sd = np.array(rat_pl), np.array(rat_sd)
    md.append(f"\n{lab}: expected placebo/actual = {np.median(rat_pl):.2f} [5-95%: {np.percentile(rat_pl,5):.2f}, {np.percentile(rat_pl,95):.2f}]; expected seasonal-diff/actual = {np.median(rat_sd):.2f} [{np.percentile(rat_sd,5):.2f}, {np.percentile(rat_sd,95):.2f}]; median t placebo {np.median(t_pl):.2f}, median t seasonal-diff {np.median(t_sd):.2f}; share of sims with seasonal-diff ratio <= observed {obs['x_sd'][1]/obs['x_raw'][1]:.2f}: {(rat_sd <= obs['x_sd'][1]/obs['x_raw'][1]).mean():.3f}")

# ------------------------------------------------------------------ 3. calendar-preserving placebos
md.append("\n## 3. Calendar-preserving and persistence-preserving placebos (full ex-lockdown sample)\n\n| placebo | n | calm | t | inter | t |\n|---|---:|---:|---:|---:|---:|")
dfull = base.dropna(subset=["ret_etf_f1"] + ctrl).copy().reset_index(drop=True)
dfull["sm"] = "S" + dfull["S_vix25"].astype(int).astype(str) + "_" + dfull["moy"].astype(str)
for c in ctrl: dfull[c + "_S"] = dfull[c] * dfull["S_vix25"]
dfull["woy"] = dfull.date.dt.isocalendar().week.astype(int)
dfull["x_seas"] = dfull.groupby(["country", "woy"])["x_raw"].transform("mean")
dfull["x_seas"] = dfull.groupby("country")["x_seas"].transform(lambda s: (s - s.mean()) / s.std())
countries = sorted(dfull.country.unique()); rot = {c: countries[(i + 5) % len(countries)] for i, c in enumerate(countries)}
prof = dfull.groupby(["country", "woy"])["x_raw"].mean()
dfull["x_other"] = [prof.get((rot[c], wk), np.nan) for c, wk in zip(dfull.country, dfull.woy)]
dfull["x_other"] = dfull.groupby("country")["x_other"].transform(lambda s: (s - s.mean()) / s.std())
dfull["x_resid"] = dfull["x_raw"] - dfull.groupby(["country", "woy"])["x_raw"].transform("mean")
dfull["x_resid"] = dfull.groupby("country")["x_resid"].transform(lambda s: (s - s.mean()) / s.std())
for lab, x in (("actual x", "x_raw"), ("own in-sample week-of-year profile (pure seasonal)", "x_seas"), ("another country's week-of-year profile (rotated)", "x_other"), ("x minus own in-sample profile (in-sample deseasonalized)", "x_resid")):
    r = d12.fit(dfull.dropna(subset=[x]), "ret_etf_f1", [("x", dfull[x]), ("xS", dfull[x] * dfull["S_vix25"]), ("S", dfull["S_vix25"])], ["cy", "sm"], EXTRA)
    md.append(f"| {lab} | {r['n']} | {r['b_x']:.3f} | {r['t_x']:.2f} | {r['b_xS']:.3f} | {r['t_xS']:.2f} |")
# circular block shift (country signal, cross-section intact)
Fw = dfull.pivot_table(index="date", columns="country", values="x_raw"); weeks = Fw.index; ts_pl = []
for k in range(300):
    sh = int(rng.integers(8, len(weeks) - 8)); Fs = pd.DataFrame(np.roll(Fw.values, sh, axis=0), index=weeks, columns=Fw.columns)
    look = Fs.stack().to_dict(); dp = dfull.copy(); dp["x_raw"] = [look.get((t, c), np.nan) for t, c in zip(dp.date, dp.country)]
    try:
        r = d12.fit(dp.dropna(subset=["x_raw"]), "ret_etf_f1", [("x", dp["x_raw"]), ("xS", dp["x_raw"] * dp["S_vix25"]), ("S", dp["S_vix25"])], ["cy", "sm"], EXTRA); ts_pl.append(r["t_xS"])
    except Exception: pass
ts_pl = np.array(ts_pl); act = d12.fit(dfull, "ret_etf_f1", [("x", dfull["x_raw"]), ("xS", dfull["x_raw"] * dfull["S_vix25"]), ("S", dfull["S_vix25"])], ["cy", "sm"], EXTRA)["t_xS"]
md.append(f"\nCircular block shift of the whole country panel (300 draws, calendar broken, persistence and cross-section kept): actual t {act:.2f}; placebo mean {ts_pl.mean():.2f}, SD {ts_pl.std():.2f}, share >= actual {(ts_pl >= act).mean():.3f}")

# ------------------------------------------------------------------ 4. reconcile the 2022 anchor
raw = rb.W[rb.W.country.isin(rb.MAIN)][["date", "country", "ret_etf_f1"]].rename(columns={"ret_etf_f1": "rr"})
wb = w.merge(raw, on=["date", "country"], how="left")
hol = wb.groupby("date")[HC].mean()  # share of countries in a holiday week
bk = wb.groupby("date").agg(F=("F", "first"), S=("S_vix25", "first"), r=("rr", "mean"), ret_em=("ret_em", "first"), d_vix=("d_vix", "first"), brent=("ret_brent", "first"),
                            dxy=("d_dxy", "first"), us10=("d_us10y", "first"), lvix=("log_vix_lvl", "first")).join(hol).dropna(subset=["F", "r"])
bk["F52"] = bk["F"].shift(52); bk["F_sd_raw"] = bk["F"] - bk["F52"]
ex = bk[(bk.index < LOCK[0]) | (bk.index > LOCK[1])]
sd_ex = ex["F_sd_raw"].std(); bk["F_sd"] = bk["F_sd_raw"] / sd_ex; ex = bk[(bk.index < LOCK[0]) | (bk.index > LOCK[1])]
md.append(f"\n## 4. The 2022 anchor, one standardization (SD of F - F_52 over the ex-lockdown sample = {sd_ex:.3f})\n\n| version | sample | n | F calm | t | F x S | t |\n|---|---|---:|---:|---:|---:|---:|")
def tsreg(d, x, with_hol):
    d = d.dropna(subset=[x]); cols = [d[x], d[x] * d.S, d.S, d.ret_em, d.d_vix, d.brent, d.dxy, d.us10, d.lvix] + ([d[h] for h in HC] if with_hol else [])
    X = sm.add_constant(np.column_stack(cols)); m = sm.OLS(100 * d.r.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4}); return len(d), m.params[1], m.tvalues[1], m.params[2], m.tvalues[2]
for lab, x in (("seasonal diff, standardized (carry this)", "F_sd"), ("seasonal diff, unstandardized (note's 2.68)", "F_sd_raw")):
    for hl in (False, True):
        for s_, d in (("2022", ex[ex.index.year == 2022]), ("ex-lockdown", ex), ("2021", ex[ex.index.year == 2021])):
            n, b1_, t1, b2_, t2 = tsreg(d, x, hl)
            md.append(f"| {lab}{' + holiday shares' if hl else ''} | {s_} | {n} | {b1_:.2f} | {t1:.2f} | {b2_:.2f} | {t2:.2f} |")
txt = "\n".join(md); open(os.path.join(RT, "round2_stats.md"), "w", encoding="utf-8").write(txt); print(txt)
