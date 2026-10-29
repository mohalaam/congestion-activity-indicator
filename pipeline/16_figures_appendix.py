"""
Step 16: Figures 2-4, Appendix Tables A1-A5, monthly-average Diebold-Mariano, weighting and
inclusion robustness for MANUSCRIPT_v3.
Outputs: results/figures/fig2_seasonal_profile.png, fig3_three_versions.png, fig4_collector_coverage.png
         results/tables/appendix_A1_cities.csv, A2_holidays.csv, A3_nowcast_bycountry.csv,
         A4_2022_timeseries.md, A5_weights_inclusion.md, dm_monthly.md
Run: py -I pipeline/16_figures_appendix.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
mt = importlib.import_module("10_main_tables")
d12 = importlib.import_module("12_decisive_reestimation")
p01 = importlib.import_module("01_build_congestion_panel")
P = os.path.join(ROOT, "data_proc"); RT = os.path.join(ROOT, "results", "tables"); RF = os.path.join(ROOT, "results", "figures")
LOCK = rb.LOCK
CTRL = ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]
out = []


def exlock(d):
    return d[(d.date < LOCK[0]) | (d.date > LOCK[1])]


def state_example(d, x, tgt="ret_etf_f1"):
    d = d.dropna(subset=[x, tgt]).copy().reset_index(drop=True)
    d["sm"] = "S" + d["S_vix25"].astype(int).astype(str) + "_" + d["moy"].astype(str)
    own = tgt.replace("_f1", "")
    ctrl = [own] + [c for c in CTRL if c != "ret_etf"] if own != "ret_etf" else CTRL
    for c in ctrl:
        d[c + "_S"] = d[c] * d["S_vix25"]
    r = d12.fit(d, tgt, [("x", d[x]), ("xS", d[x] * d["S_vix25"]), ("S", d["S_vix25"])], ["cy", "sm"], ctrl + [c + "_S" for c in ctrl] + HC + ["log_vix_lvl"])
    return r


def vol_example(d, x):
    d = d.dropna(subset=[x, "lrv_etf_f1"]).copy().reset_index(drop=True); d["mo"] = d["moy"].astype(str)
    return d12.fit(d, "lrv_etf_f1", [("x", d[x])], ["cy", "mo"], ["lrv_etf", "lrv_etf_m4", "lrv_etf_m13", "log_vix", "ret_em", "d_vix"])


def prep_panel(w):
    w = w.sort_values(["country", "date"]).copy()
    w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]; w["log_vix_lvl"] = np.log(w["vix"])
    w["x52"] = w.groupby("country")["x_raw"].shift(52); w["x_sd"] = w["x_raw"] - w["x52"]
    w["x_sd"] = w.groupby("country")["x_sd"].transform(lambda s: s / s.std())
    return w


w = mt.prep(); w, HC = d12.add_holidays(w); w = prep_panel(w)
w["F"] = w.groupby("date")["x_raw"].transform("mean")
base = exlock(w)

# ------------------------------------------------------------ Figure 2: seasonal profile
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
b = base.copy(); b["woy"] = b.date.dt.isocalendar().week.astype(int)
prof = b.groupby(["country", "woy"])["x_raw"].mean().unstack(0)
axes[0].plot(prof.index, prof.mean(axis=1), color="#1f4e79", lw=2, label="mean of 12 countries")
axes[0].fill_between(prof.index, prof.quantile(0.25, axis=1), prof.quantile(0.75, axis=1), color="#1f4e79", alpha=0.15, label="interquartile range")
gpath = os.path.join(P, "google_mobility_daily.csv")
if os.path.exists(gpath):
    g = pd.read_csv(gpath, parse_dates=["date"]); gw = g.set_index("date").groupby("country")["gm_work"].resample("W-FRI").mean().reset_index()
    gw["innov"] = gw.groupby("country")["gm_work"].transform(lambda s: s - s.rolling(4).mean().shift(1)); gw["innov"] = gw.groupby("country")["innov"].transform(lambda s: s / s.std())
    gw = exlock(gw); gw["woy"] = gw.date.dt.isocalendar().week.astype(int)
    gp = gw.groupby("woy")["innov"].mean(); axes[0].plot(gp.index, gp.values, color="#c0504d", lw=1.4, ls="--", label="Google workplaces (12 countries)")
axes[0].axhline(0, color="k", lw=0.8); axes[0].set_xlabel("ISO week of year"); axes[0].set_ylabel("Mean weekly innovation (SD units)"); axes[0].legend(fontsize=8, frameon=False)
axes[0].set_title("A. Week-of-year profile of congestion innovations, 2020-2023 ex-lockdown", fontsize=9)
for c, col in (("Brazil", "#1f4e79"), ("Poland", "#c0504d"), ("Turkey", "#7f7f7f"), ("India", "#2e8b57")):
    axes[1].plot(prof.index, prof[c], lw=1.3, label=c, color=col)
axes[1].axhline(0, color="k", lw=0.8); axes[1].set_xlabel("ISO week of year"); axes[1].legend(fontsize=8, frameon=False)
axes[1].set_title("B. Selected countries (fixed vs moving holidays)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(RF, "fig2_seasonal_profile.png"), dpi=300); plt.close(fig)

# ------------------------------------------------------------ Figure 3: three versions
res = {}
for lab, x in (("Actual signal", "x_raw"), ("Lagged 52 weeks (placebo)", "x52"), ("Real-time seasonal difference", "x_sd")):
    res[lab] = state_example(base, x)
act_ps = state_example(base.dropna(subset=["x52"]), "x_raw"); res["Actual, placebo sample"] = act_ps
fig, ax = plt.subplots(figsize=(8, 3.6)); labs = list(res); xx = np.arange(len(labs)); wd = 0.36
calm = [res[l]["b_x"] for l in labs]; stress = [res[l]["b_x"] + res[l]["b_xS"] for l in labs]
ce = [1.96 * abs(res[l]["b_x"] / res[l]["t_x"]) for l in labs]; se_ = [1.96 * abs(res[l]["b_xS"] / res[l]["t_xS"]) for l in labs]
ax.bar(xx - wd / 2, calm, wd, yerr=ce, color="#7f7f7f", capsize=3, label="Calm (VIX <= 25)")
ax.bar(xx + wd / 2, stress, wd, yerr=se_, color="#c0504d", capsize=3, label="Stress (VIX > 25)")
ax.axhline(0, color="k", lw=0.8); ax.set_xticks(xx); ax.set_xticklabels(labs, fontsize=8); ax.set_ylabel("Next-week USD return per SD (SD units)")
ax.legend(fontsize=8, frameon=False); ax.set_title("Figure 3. State-dependent response under the three signal versions (eq. 1, 95% CI)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(RF, "fig3_three_versions.png"), dpi=300); plt.close(fig)
out.append("Figure 3 values: " + "; ".join(f"{l}: calm {res[l]['b_x']:.3f} (t {res[l]['t_x']:.2f}), inter {res[l]['b_xS']:.3f} (t {res[l]['t_xS']:.2f}), n {res[l]['n']}" for l in labs))

# ------------------------------------------------------------ Figure 4: collector coverage
cpath = os.path.join(ROOT, "collector", "data", "tomtom_live_hourly.csv")
if os.path.exists(cpath):
    cl = pd.read_csv(cpath, parse_dates=["date"])
    cov = cl.groupby("date")["city_id"].nunique(); hrs = cl.groupby("date").size() / cl.groupby("date")["city_id"].nunique()
    fig, ax = plt.subplots(figsize=(8, 3.2)); ax.bar(cov.index, cov.values, color="#1f4e79", width=0.8, label="cities with data")
    ax2 = ax.twinx(); ax2.plot(hrs.index, hrs.values, color="#c0504d", marker="o", lw=1.2, label="hours per city")
    ax.set_ylabel("Cities"); ax2.set_ylabel("Hours per city"); ax.set_title(f"Figure 4. Live-feed collector coverage since 2026-10-21 (490 target cities); rows so far: {len(cl):,}", fontsize=9)
    ax.legend(loc="upper left", fontsize=8, frameon=False); ax2.legend(loc="upper right", fontsize=8, frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(RF, "fig4_collector_coverage.png"), dpi=300); plt.close(fig)
    out.append(f"Collector: {cl.city_id.nunique()} cities, {cl.date.min().date()} to {cl.date.max().date()}, {len(cl):,} hourly rows")

# ------------------------------------------------------------ A1 cities
cd = pd.read_csv(os.path.join(P, "city_daily.csv"), parse_dates=["date"])
rows = []
for c, cities in p01.MAIN.items():
    for ci, wgt in cities.items():
        g = cd[(cd.country == c) & (cd.city == ci)]
        rows.append({"country": c, "city": ci, "population_weight_m": wgt, "first_day": g.date.min().date() if len(g) else None,
                     "last_day": g.date.max().date() if len(g) else None, "missing_share": round(g["missing"].mean(), 4) if len(g) else None,
                     "mean_congestion_pct": round(g["congestion"].mean(), 1) if len(g) else None})
pd.DataFrame(rows).to_csv(os.path.join(RT, "appendix_A1_cities.csv"), index=False)

# ------------------------------------------------------------ A2 holidays
rows = []
for h, dates in d12.HOLIDAYS.items():
    grp = {"ramadan_start": "Muslim-majority: " + ", ".join(d12.MUSLIM), "eid_fitr": "Muslim-majority", "eid_adha": "Muslim-majority", "diwali": "India",
           "lny": ", ".join(d12.LNY), "easter": ", ".join(d12.CHRISTIAN), "xmas": "all"}[h]
    for y, dt_ in dates.items():
        rows.append({"holiday": h, "year": y, "date": dt_, "countries": grp, "window": "holiday week + following week (Ramadan: whole month)"})
pd.DataFrame(rows).to_csv(os.path.join(RT, "appendix_A2_holidays.csv"), index=False)

# ------------------------------------------------------------ A3 nowcast by country + monthly-average DM
a = pd.read_csv(os.path.join(ROOT, "results", "nowcast_benchmarks_bycountry.csv")); b_ = pd.read_csv(os.path.join(ROOT, "results", "nowcast_benchmarks_bycountry_exlock.csv"))
A3 = a[a.model == "POOL_BRIDGE"][["country", "n", "rel_rmse_vs_AR"]].rename(columns={"rel_rmse_vs_AR": "rel_rmse_all_training"}).merge(
    b_[b_.model == "POOL_BRIDGE"][["country", "rel_rmse_vs_AR"]].rename(columns={"rel_rmse_vs_AR": "rel_rmse_exlock_training"}), on="country", how="outer")
A3.to_csv(os.path.join(RT, "appendix_A3_nowcast_bycountry.csv"), index=False)
pr = pd.read_csv(os.path.join(ROOT, "results", "nowcast_predictions_exlock.csv"), parse_dates=["date"])
dm_lines = ["# Diebold-Mariano on monthly-average loss differentials (AR vs POOL_BRIDGE, lockdown excluded from training)\n", "| sample | months | mean dL | DM t | p (t, n-1) |\n|---|---:|---:|---:|---:|"]
for lab, sub in (("2021-01+", pr), ("2021-07+", pr[pr.date >= "2021-07-01"])):
    s = sub.dropna(subset=["AR", "POOL_BRIDGE"]).copy(); s["dL"] = (s.y - s.AR) ** 2 - (s.y - s.POOL_BRIDGE) ** 2
    m = s.groupby("date")["dL"].mean(); n = len(m)
    dmt = m.mean() / (m.std(ddof=1) / np.sqrt(n)); p = 2 * (1 - stats.t.cdf(abs(dmt), df=n - 1))
    # HAC version
    mh = sm.OLS(m.values, np.ones(n)).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
    dm_lines.append(f"| {lab} | {n} | {m.mean():.5f} | {dmt:.2f} (HAC {mh.tvalues[0]:.2f}) | {p:.3f} |")
open(os.path.join(RT, "dm_monthly.md"), "w", encoding="utf-8").write("\n".join(dm_lines)); out.append("\n".join(dm_lines))

# ------------------------------------------------------------ A4 2022 time series under three versions
raw = rb.W[rb.W.country.isin(rb.MAIN)][["date", "country", "ret_etf_f1"]].rename(columns={"ret_etf_f1": "rr"})
wb = w.merge(raw, on=["date", "country"], how="left")
bk = wb.groupby("date").agg(F=("F", "first"), S=("S_vix25", "first"), r=("rr", "mean"), ret_em=("ret_em", "first"), d_vix=("d_vix", "first"), brent=("ret_brent", "first"),
                            dxy=("d_dxy", "first"), us10=("d_us10y", "first"), lvix=("log_vix_lvl", "first")).dropna()
bk["F52"] = bk["F"].shift(52); bk["F_sd"] = (bk["F"] - bk["F52"]); bk["F_sd"] = bk["F_sd"] / bk["F_sd"].std()
ex = bk[(bk.index < LOCK[0]) | (bk.index > LOCK[1])]
A4 = ["# Appendix A4. Basket next-week USD return (%) on the factor, time series, HAC(4)\n", "| version | sample | n | F calm | t | F x S | t |\n|---|---|---:|---:|---:|---:|---:|"]
for lab, x in (("actual", "F"), ("lagged 52 wk", "F52"), ("real-time seasonal diff", "F_sd")):
    for s_, d in (("ex-lockdown", ex), ("2022", ex[ex.index.year == 2022]), ("2021", ex[ex.index.year == 2021])):
        d = d.dropna(subset=[x]); X = sm.add_constant(np.column_stack([d[x], d[x] * d.S, d.S, d.ret_em, d.d_vix, d.brent, d.dxy, d.us10, d.lvix]))
        m = sm.OLS(100 * d.r.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
        A4.append(f"| {lab} | {s_} | {len(d)} | {m.params[1]:.2f} | {m.tvalues[1]:.2f} | {m.params[2]:.2f} | {m.tvalues[2]:.2f} |")
open(os.path.join(RT, "appendix_A4_2022_timeseries.md"), "w", encoding="utf-8").write("\n".join(A4)); out.append("\n".join(A4))

# ------------------------------------------------------------ A5 weights and inclusion
A5 = ["# Appendix A5. Weighting and inclusion robustness (state example eq. 1 and volatility, USD ETF, ex-lockdown)\n",
      "| variant | state: actual x, inter | t | state: seasonal-diff inter | t | vol: actual | t | vol: seasonal-diff | t |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|"]


def rebuild_country_signal(weights_fn, countries=None):
    """Recompute country weekly innovations from city_daily with a different weighting; returns weekly country frame merged with market data."""
    c = cd[cd.country.isin(countries or rb.MAIN)].copy()
    c["wgt"] = c.apply(weights_fn, axis=1)
    def wavg(g):
        m = g["log_c_dowadj"].notna(); return np.average(g.loc[m, "log_c_dowadj"], weights=g.loc[m, "wgt"]) if m.any() else np.nan
    daily = c.groupby(["country", "date"]).apply(wavg).rename("lc").reset_index()
    wk = daily.set_index("date").groupby("country")["lc"].resample("W-FRI").mean().reset_index()
    wk["x_raw"] = wk.groupby("country")["lc"].transform(lambda s: s - s.rolling(4).mean().shift(1))
    wk["x_raw"] = wk.groupby("country")["x_raw"].transform(lambda s: (s - s.mean()) / s.std())
    return wk[["date", "country", "x_raw"]]


def run_variant(name, wk, extra_market=None):
    base_cols = w.drop(columns=["x_raw", "x52", "x_sd", "F"]).copy()
    v = base_cols.merge(wk, on=["date", "country"], how="inner"); v = prep_panel(v); v = exlock(v)
    r1 = state_example(v, "x_raw"); r2 = state_example(v, "x_sd"); v1 = vol_example(v, "x_raw"); v2 = vol_example(v, "x_sd")
    A5.append(f"| {name} | {r1['b_xS']:.3f} | {r1['t_xS']:.2f} | {r2['b_xS']:.3f} | {r2['t_xS']:.2f} | {v1['b_x']:.3f} | {v1['t_x']:.2f} | {v2['b_x']:.3f} | {v2['t_x']:.2f} |")


wk_pop = w[["date", "country", "x_raw"]]
run_variant("population weights (baseline)", wk_pop)
run_variant("equal city weights", rebuild_country_signal(lambda r: 1.0))
largest = {c: max(d, key=d.get) for c, d in p01.MAIN.items()}
run_variant("largest city only", rebuild_country_signal(lambda r: 1.0 if r["city"] == largest.get(r["country"]) else 0.0))
# inclusion: Greece (in secondary panel), Taiwan and UAE (rebuild from the raw archive)
try:
    import yfinance as yf
    rawarch = pd.read_csv(os.path.join(ROOT, "data_raw", "tomtom_trafic_index.csv"), parse_dates=["date"])
    extra = {"Taiwan": {"Taipei": 7.0, "Taichung": 2.8, "Kaohsiung": 2.7, "Tainan": 1.9, "Taoyuan": 2.3}, "United Arab Emirates": {"Dubai": 3.4, "Abu Dhabi": 1.5}}
    frames = []
    for c, cities in extra.items():
        for ci, wgt in cities.items():
            g = rawarch[(rawarch.country == c) & (rawarch.city == ci)].set_index("date").sort_index()
            full = pd.date_range(g.index.min(), g.index.max(), freq="D"); g = g.reindex(full); g["congestion"] = g["congestion"].interpolate(limit=3)
            g["log_c"] = np.log(g["congestion"].clip(lower=1)); g["dow"] = g.index.dayofweek
            basel = g.groupby("dow")["log_c"].transform(lambda s: s.rolling(52, min_periods=8).mean().shift(1)); g["log_c_dowadj"] = g["log_c"] - basel
            g["country"], g["city"], g["wgt"] = c, ci, wgt; frames.append(g.rename_axis("date").reset_index()[["date", "country", "city", "log_c_dowadj", "wgt"]])
    ex_cd = pd.concat(frames)
    def wavg2(g):
        m = g["log_c_dowadj"].notna(); return np.average(g.loc[m, "log_c_dowadj"], weights=g.loc[m, "wgt"]) if m.any() else np.nan
    daily = ex_cd.groupby(["country", "date"]).apply(wavg2).rename("lc").reset_index()
    wk2 = daily.set_index("date").groupby("country")["lc"].resample("W-FRI").mean().reset_index()
    wk2["x_raw"] = wk2.groupby("country")["lc"].transform(lambda s: s - s.rolling(4).mean().shift(1)); wk2["x_raw"] = wk2.groupby("country")["x_raw"].transform(lambda s: (s - s.mean()) / s.std())
    # Greece from existing weekly panel (secondary); ETFs
    gr = rb.W[rb.W.country == "Greece"][["date", "country", "cong_innov4"]].rename(columns={"cong_innov4": "x_raw"}); gr["x_raw"] = (gr.x_raw - gr.x_raw.mean()) / gr.x_raw.std()
    etfs = {"Taiwan": "EWT", "United Arab Emirates": "UAE", "Greece": "GREK"}
    mk_rows = []
    for c, tk in etfs.items():
        h = yf.Ticker(tk).history(start="2019-01-01", auto_adjust=True)[["Close"]]; h.index = pd.to_datetime(h.index).tz_localize(None).normalize()
        wkr = np.log(h["Close"]).resample("W-FRI").last().diff(); rv = np.log((np.log(h["Close"]).diff() ** 2).resample("W-FRI").sum(min_count=3).replace(0, np.nan))
        f = pd.DataFrame({"ret_etf": wkr, "ret_etf_f1": wkr.shift(-1), "lrv_etf": rv, "lrv_etf_f1": rv.shift(-1), "lrv_etf_m4": rv.rolling(4).mean(), "lrv_etf_m13": rv.rolling(13).mean()}); f["country"] = c; mk_rows.append(f.reset_index().rename(columns={"index": "date", "Date": "date"}))
    mk_x = pd.concat(mk_rows)
    glob = w.groupby("date")[["vix", "S_vix25", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y", "log_vix", "moy"]].first().reset_index()
    sig = pd.concat([wk2, gr]); ext = sig.merge(mk_x, on=["date", "country"], how="inner").merge(glob, on="date", how="left")
    ext["year"] = ext.date.dt.year.astype(str); ext["cy"] = ext.country + "_" + ext.year; ext, _ = d12.add_holidays(ext)
    for h in HC:
        if h not in ext: ext[h] = 0.0
    ext["log_vix_lvl"] = np.log(ext.vix)
    extp = prep_panel(ext)
    keep = ["date", "country", "x_raw", "x52", "x_sd", "ret_etf", "ret_etf_f1", "lrv_etf", "lrv_etf_f1", "lrv_etf_m4", "lrv_etf_m13", "vix", "S_vix25", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y", "log_vix", "log_vix_lvl", "moy", "year", "cy"] + HC
    comb = pd.concat([base[keep], exlock(extp)[keep]], ignore_index=True)
    r1 = state_example(comb, "x_raw"); r2 = state_example(comb, "x_sd"); v1 = vol_example(comb, "x_raw"); v2 = vol_example(comb, "x_sd")
    A5.append(f"| + Taiwan, UAE, Greece (15 countries) | {r1['b_xS']:.3f} | {r1['t_xS']:.2f} | {r2['b_xS']:.3f} | {r2['t_xS']:.2f} | {v1['b_x']:.3f} | {v1['t_x']:.2f} | {v2['b_x']:.3f} | {v2['t_x']:.2f} |")
    # single-city countries vs multi-city
    multi = [c for c, d in p01.MAIN.items() if len(d) > 1]
    for nm, sub in (("multi-city countries only", base[base.country.isin(multi)]), ("single-city countries only", base[~base.country.isin(multi)])):
        r1 = state_example(sub, "x_raw"); r2 = state_example(sub, "x_sd"); v1 = vol_example(sub, "x_raw"); v2 = vol_example(sub, "x_sd")
        A5.append(f"| {nm} | {r1['b_xS']:.3f} | {r1['t_xS']:.2f} | {r2['b_xS']:.3f} | {r2['t_xS']:.2f} | {v1['b_x']:.3f} | {v1['t_x']:.2f} | {v2['b_x']:.3f} | {v2['t_x']:.2f} |")
except Exception as e:
    A5.append(f"| inclusion variants failed: {e} |")
open(os.path.join(RT, "appendix_A5_weights_inclusion.md"), "w", encoding="utf-8").write("\n".join(A5)); out.append("\n".join(A5))
print("\n\n".join(out))
