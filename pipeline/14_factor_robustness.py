"""
Step 14: Sections 3.4-3.7 on the factor specification (equation 3 of MANUSCRIPT_v2).

A. Volatility: next-week log realized variance (USD ETF, local index) on F, e, HAR controls,
   log VIX, country x year + month FE; with and without state interaction.
B. Quantiles: (i) time series, basket next-week return on F, F x S, S, controls at tau 0.1-0.9;
   (ii) panel, USD ETF return on F and e (country-year demeaned) at tau 0.1-0.9 with week-block
   bootstrap SEs (200 draws).
C. Robustness of the headline F x S (eq. 3, USD ETF, ex-lockdown): alternative states
   (VIX>20/25/30, top tercile, continuous log VIX, EM drawdown>10%); moving-block bootstrap
   (8-week blocks, 1000 draws); episode jackknife; country exclusion; placebos (circular block
   permutation of the F series keeping the cross-section, 500 draws; F lagged 52 weeks on the
   like-for-like sample); Google workplaces common component in the overlap window.
D. Strategy: one position per week on the equal-weight USD basket: long if (stress and F>0)
   or (calm and F<0), short otherwise; gross and net of 10/25 bp per switch; by year; plus the
   calm-only rule (short basket on F>0 in calm weeks, flat otherwise).
Outputs: results/tables/table_factor_robustness.md (+ CSVs), results/figures/fig4_factor_strategy.png
Run: py -I pipeline/14_factor_robustness.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
rng = np.random.default_rng(1403)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
mt = importlib.import_module("10_main_tables")
d12 = importlib.import_module("12_decisive_reestimation")
RT = os.path.join(ROOT, "results", "tables"); RF = os.path.join(ROOT, "results", "figures")
CTRL = ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]
md = ["# Factor-specification results for Sections 3.4-3.7\n"]


def build():
    w = mt.prep().sort_values(["country", "date"])
    w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]
    w, HC = d12.add_holidays(w)
    w["F"] = w.groupby("date")["x_raw"].transform("mean"); w["e"] = w["x_raw"] - w["F"]
    w["log_vix_lvl"] = np.log(w["vix"])
    w["S_terc"] = (w["vix"] > rb.exlock(w)["vix"].quantile(2 / 3)).astype(float)
    for c in CTRL:
        w[c + "_S"] = w[c] * w["S_vix25"]
    raw = rb.W[rb.W.country.isin(rb.MAIN)][["date", "country", "ret_etf_f1"]].rename(columns={"ret_etf_f1": "ret_raw_f1"})
    w = w.merge(raw, on=["date", "country"], how="left")
    return w, HC


def headline(d, state="S_vix25", tgt="ret_etf_f1", fe=("cy", "sm"), dk=None, xF="F", xe="e"):
    d = d.copy().reset_index(drop=True); d["sm"] = "S" + d[state].astype(int).astype(str) + "_" + d["moy"].astype(str)
    for c in CTRL:
        d[c + "_S"] = d[c] * d[state]
    xcols = [("F", d[xF]), ("FxS", d[xF] * d[state]), ("e", d[xe]), ("exS", d[xe] * d[state]), ("S", d[state])]
    extra = CTRL + [c + "_S" for c in CTRL] + HC + ["log_vix_lvl"]
    return d12.fit(d, tgt, xcols, list(fe), extra, dk_lags=dk)


w, HC = build()
base = rb.exlock(w)

# ------------------------------------------------------------------ A. volatility
md.append("## A. Next-week log realized variance on F and e (country x year + month FE, HAR + log VIX controls)\n\n| target | sample | n | F | t | e | t | F x S | t |\n|---|---|---:|---:|---:|---:|---:|---:|---:|")
for v, vname in (("lrv_etf", "USD ETF"), ("lrv_idx", "Local index")):
    for lab, d in [("ex-lockdown", base), ("2021-2022", base[base.year.isin(["2021", "2022"])])]:
        ctrl = [v, f"{v}_m4", f"{v}_m13", "log_vix_lvl", "ret_em", "d_vix"]
        d = d.copy(); d["mo"] = d["moy"].astype(str)
        r1 = d12.fit(d, f"{v}_f1", [("F", d["F"]), ("e", d["e"])], ["cy", "mo"], ctrl)
        r2 = d12.fit(d, f"{v}_f1", [("F", d["F"]), ("FxS", d["F"] * d["S_vix25"]), ("e", d["e"]), ("S", d["S_vix25"])], ["cy", "mo"], ctrl)
        md.append(f"| {vname} | {lab} | {r1['n']} | {r1['b_F']:.3f} | {r1['t_F']:.2f} | {r1['b_e']:.3f} | {r1['t_e']:.2f} | {r2['b_FxS']:.3f} | {r2['t_FxS']:.2f} |")

# ------------------------------------------------------------------ B. quantiles
md.append("\n## B. Quantile regressions\n\n(i) Time series: basket next-week return (%) on F, F x S, S, controls (n = 138, ex-lockdown)\n\n| tau | F calm | t | F x S | t |\n|---|---:|---:|---:|---:|")
bask = w.groupby("date").agg(F=("F", "first"), S=("S_vix25", "first"), r=("ret_raw_f1", "mean"), ret_em=("ret_em", "first"), d_vix=("d_vix", "first"),
                             ret_brent=("ret_brent", "first"), d_dxy=("d_dxy", "first"), d_us10y=("d_us10y", "first"), lvix=("log_vix_lvl", "first")).dropna()
bask = bask[(bask.index < "2020-03-01") | (bask.index > "2020-06-30")]
Xb = sm.add_constant(pd.DataFrame({"F": bask.F, "FxS": bask.F * bask.S, "S": bask.S, "ret_em": bask.ret_em, "d_vix": bask.d_vix, "brent": bask.ret_brent, "dxy": bask.d_dxy, "us10": bask.d_us10y, "lvix": bask.lvix}).values)
for tau in (0.1, 0.25, 0.5, 0.75, 0.9):
    qm = QuantReg(100 * bask.r.values, Xb).fit(q=tau, max_iter=5000)
    md.append(f"| {tau} | {qm.params[1]:.3f} | {qm.tvalues[1]:.2f} | {qm.params[2]:.3f} | {qm.tvalues[2]:.2f} |")
md.append("\n(ii) Panel: USD ETF next-week return on F and e, country-year demeaned, week-block bootstrap SE (200 draws)\n\n| tau | F | boot t | e | boot t |\n|---|---:|---:|---:|---:|")
dq = base.dropna(subset=["ret_etf_f1", "F", "e", "ret_em", "d_vix"]).copy()
for c in ["ret_etf_f1", "F", "e", "ret_em", "d_vix"]:
    dq[c] = dq[c] - dq.groupby("cy")[c].transform("mean")
Xq = sm.add_constant(dq[["F", "e", "ret_em", "d_vix"]].values)
weeks = np.array(sorted(dq.date.unique())); byw = {t: g for t, g in dq.groupby("date")}
for tau in (0.1, 0.25, 0.5, 0.75, 0.9):
    qm = QuantReg(dq["ret_etf_f1"].values, Xq).fit(q=tau, max_iter=5000)
    bF, be = [], []
    for b in range(200):
        starts = rng.integers(0, len(weeks) - 8 + 1, size=int(np.ceil(len(weeks) / 8)))
        sel = np.concatenate([weeks[s:s + 8] for s in starts])[:len(weeks)]
        db = pd.concat([byw[t] for t in sel])
        try:
            q2 = QuantReg(db["ret_etf_f1"].values, sm.add_constant(db[["F", "e", "ret_em", "d_vix"]].values)).fit(q=tau, max_iter=3000)
            bF.append(q2.params[1]); be.append(q2.params[2])
        except Exception:
            pass
    md.append(f"| {tau} | {qm.params[1]:.3f} | {qm.params[1]/np.std(bF):.2f} | {qm.params[2]:.3f} | {qm.params[2]/np.std(be):.2f} |")

# ------------------------------------------------------------------ C. robustness
md.append("\n## C. Robustness of the headline F x S (USD ETF, ex-lockdown, eq. 3)\n\n### C1 alternative states\n\n| state | n | F calm | t | F x S | t | share stress |\n|---|---:|---:|---:|---:|---:|---:|")
glob = rb.mk[rb.mk.country == "GLOBAL"].pivot_table(index="date", columns="series", values="value").sort_index()
eem = glob["msci_em_etf"].resample("W-FRI").last(); dd = (eem / eem.rolling(26).max() - 1).rename("em_dd")
base = base.merge(dd, left_on="date", right_index=True, how="left")
base["S_vix20"] = (base.vix > 20).astype(float); base["S_vix30"] = (base.vix > 30).astype(float)
base["S_emdd"] = (base.em_dd < -0.10).astype(float); base["S_lvix"] = np.log(base.vix) - np.log(base.vix).mean()
for st in ["S_vix20", "S_vix25", "S_terc", "S_vix30", "S_emdd", "S_lvix"]:
    try:
        fe = ("cy", "sm") if st != "S_lvix" else ("cy", "moy_s")
        d = base.copy(); d["moy_s"] = d["moy"].astype(str)
        r = headline(d, state=st, fe=fe)
        md.append(f"| {st} | {r['n']} | {r['b_F']:.3f} | {r['t_F']:.2f} | {r['b_FxS']:.3f} | {r['t_FxS']:.2f} | {d[st].mean():.2f} |")
    except Exception as ex:
        md.append(f"| {st} | failed: {ex} |")

# C2 block bootstrap (cluster=False fits inside d12.fit use clustered; use point/boot SE)
d0 = base.dropna(subset=["ret_etf_f1", "F", "e", "S_vix25"] + CTRL).copy()
point = headline(d0)
weeks = np.array(sorted(d0.date.unique())); byw = {t: g for t, g in d0.groupby("date")}
boots = []
for b in range(1000):
    starts = rng.integers(0, len(weeks) - 8 + 1, size=int(np.ceil(len(weeks) / 8)))
    sel = np.concatenate([weeks[s:s + 8] for s in starts])[:len(weeks)]
    db = pd.concat([byw[t] for t in sel])
    try:
        boots.append(headline(db)["b_FxS"])
    except Exception:
        pass
boots = np.array(boots)
md.append(f"\n### C2 moving-block bootstrap (8-week blocks, {len(boots)} draws): F x S = {point['b_FxS']:.3f}, boot SE {boots.std():.3f}, boot t {point['b_FxS']/boots.std():.2f}, 95% CI [{np.percentile(boots,2.5):.3f}, {np.percentile(boots,97.5):.3f}], share > 0: {(boots>0).mean():.3f}")

# C3 episode jackknife
sv = d0.groupby("date")["S_vix25"].first().sort_index(); ep, cur, last = [], [], None
for t, v in sv.items():
    if v == 1:
        if cur and (t - last).days > 14:
            ep.append(cur); cur = []
        cur.append(t); last = t
if cur: ep.append(cur)
md.append("\n### C3 episode jackknife\n\n| dropped episode | F x S | t |\n|---|---:|---:|")
for e_ in ep:
    r = headline(d0[~d0.date.isin(e_)])
    md.append(f"| {e_[0].date()}..{e_[-1].date()} ({len(e_)} wks) | {r['b_FxS']:.3f} | {r['t_FxS']:.2f} |")

# C4 country exclusion (F recomputed without the country)
md.append("\n### C4 country exclusion (factor recomputed without the dropped country)\n\n| dropped | F x S | t |\n|---|---:|---:|")
for c in sorted(base.country.unique()):
    d = base[base.country != c].copy()
    d["F"] = d.groupby("date")["x_raw"].transform("mean"); d["e"] = d["x_raw"] - d["F"]
    r = headline(d); md.append(f"| {c} | {r['b_FxS']:.3f} | {r['t_FxS']:.2f} |")

# C5 placebos
Fser = d0.groupby("date")["F"].first().sort_index(); nW = len(Fser)
ts_pl = []
for k in range(500):
    shift = int(rng.integers(8, nW - 8)); Fp = pd.Series(np.roll(Fser.values, shift), index=Fser.index)
    dp = d0.copy(); dp["F"] = dp["date"].map(Fp)
    try:
        ts_pl.append(headline(dp)["t_FxS"])
    except Exception:
        pass
ts_pl = np.array(ts_pl)
d52 = base.copy(); d52["F52"] = d52["date"].map(Fser.shift(52)); d52 = d52.dropna(subset=["F52"])
r_act = headline(d52); r_pl = headline(d52, xF="F52")
md.append(f"\n### C5 placebos\n- Circular block shift of the F series (500 draws, cross-section intact, clustered t): actual t = {point['t_FxS']:.2f}; placebo mean {ts_pl.mean():.2f}, SD {ts_pl.std():.2f}, share >= actual {(ts_pl>=point['t_FxS']).mean():.3f}\n- F lagged 52 weeks, like-for-like sample (n = {r_pl['n']}): actual F x S = {r_act['b_FxS']:.3f} (t {r_act['t_FxS']:.2f}); placebo = {r_pl['b_FxS']:.3f} (t {r_pl['t_FxS']:.2f})")

# C6 Google common component
gpath = os.path.join(ROOT, "data_proc", "google_mobility_daily.csv")
if os.path.exists(gpath):
    g = pd.read_csv(gpath, parse_dates=["date"])
    gw = g.set_index("date").groupby("country")[["gm_work"]].resample("W-FRI").mean().reset_index()
    gw["gm_innov"] = gw.groupby("country")["gm_work"].transform(lambda s: s - s.rolling(4).mean().shift(1))
    gw["gm_innov"] = gw.groupby("country")["gm_innov"].transform(lambda s: (s - s.mean()) / s.std())
    wg = base.merge(gw[["date", "country", "gm_innov"]], on=["date", "country"], how="inner").dropna(subset=["gm_innov"])
    wg["Fg"] = wg.groupby("date")["gm_innov"].transform("mean"); wg["eg"] = wg["gm_innov"] - wg["Fg"]
    wg["F2"] = wg.groupby("date")["x_raw"].transform("mean"); wg["e2"] = wg["x_raw"] - wg["F2"]
    rg = headline(wg, xF="Fg", xe="eg"); rc = headline(wg, xF="F2", xe="e2")
    corrF = wg.groupby("date")[["Fg", "F2"]].first().corr().iloc[0, 1]
    md.append(f"\n### C6 Google workplaces mobility common component (overlap window, n = {rg['n']}): correlation of Google and congestion factors {corrF:.2f}; Google F x S = {rg['b_FxS']:.3f} (t {rg['t_FxS']:.2f}), calm {rg['b_F']:.3f} (t {rg['t_F']:.2f}); congestion in same window F x S = {rc['b_FxS']:.3f} (t {rc['t_FxS']:.2f})")

# ------------------------------------------------------------------ D. strategy
bk = w.groupby("date").agg(F=("F", "first"), S=("S_vix25", "first"), r=("ret_raw_f1", "mean")).dropna()
bk = bk[(bk.index < "2020-03-01") | (bk.index > "2020-06-30")]
bk["pos"] = np.where(((bk.S == 1) & (bk.F > 0)) | ((bk.S == 0) & (bk.F < 0)), 1.0, -1.0)
bk["pos_calm"] = np.where((bk.S == 0) & (bk.F > 0), -1.0, np.where((bk.S == 0) & (bk.F < 0), 1.0, 0.0))
bk["pos_stress"] = np.where((bk.S == 1), np.sign(bk.F), 0.0)
bk["pos_uncond"] = np.sign(bk.F)
bk["year"] = bk.index.year


def perf(r, label):
    r = r.dropna(); m = sm.OLS(r.values, np.ones(len(r))).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    cum = r.cumsum(); return {"portfolio": label, "weeks": len(r), "mean_pct": 100 * r.mean(), "sd_pct": 100 * r.std(), "t": m.tvalues[0],
                               "sharpe": r.mean() / r.std() * np.sqrt(52), "mdd_pct": 100 * (cum - cum.cummax()).min(), "hit": (r > 0).mean()}


turn = bk["pos"].diff().abs().fillna(0) / 2  # fraction of portfolio switched (0, or 1 when flipping)
rows = [perf(bk.pos * bk.r, "State rule, gross"), perf(bk.pos * bk.r - turn * 2 * 10 / 1e4, "State rule, net 10 bp one-way"),
        perf(bk.pos * bk.r - turn * 2 * 25 / 1e4, "State rule, net 25 bp one-way"), perf(bk.pos_calm * bk.r, "Calm leg only"),
        perf(bk.pos_stress * bk.r, "Stress leg only"), perf(bk.pos_uncond * bk.r, "Unconditional sign rule"), perf(bk.r, "Long-only basket")]
for y in (2020, 2021, 2022):
    rows.append(perf((bk.pos * bk.r)[bk.year == y], f"State rule, {y} only"))
st = pd.DataFrame(rows); st.to_csv(os.path.join(RT, "table_factor_strategy.csv"), index=False)
md.append("\n## D. Basket timing rule on F (one position per week, equal-weight USD basket, ex-lockdown)\n\n| portfolio | weeks | mean %/wk | SD % | t NW | Sharpe | max DD % | hit |\n|---|---:|---:|---:|---:|---:|---:|---:|")
for r in rows:
    md.append(f"| {r['portfolio']} | {r['weeks']} | {r['mean_pct']:.3f} | {r['sd_pct']:.2f} | {r['t']:.2f} | {r['sharpe']:.2f} | {r['mdd_pct']:.1f} | {r['hit']:.2f} |")
md.append(f"\nAverage weekly turnover (share of weeks with a position flip): {turn.mean()*2:.2f}; break-even one-way cost: {100*(bk.pos*bk.r).mean()/ (turn.mean()*2) * 100:.0f} bp")
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(bk.index, 100 * (bk.pos * bk.r).cumsum(), color="#1f4e79", lw=1.6, label="State rule on F")
ax.plot(bk.index, 100 * (bk.pos_uncond * bk.r).cumsum(), color="#7f7f7f", lw=1.4, label="Unconditional sign rule")
ax.plot(bk.index, 100 * bk.r.cumsum(), color="#c0504d", lw=1.4, label="Long-only basket")
for t in bk[bk.S == 1].index:
    ax.axvspan(t - pd.Timedelta(days=6), t, color="grey", alpha=0.12, lw=0)
ax.axhline(0, color="k", lw=0.8); ax.set_ylabel("Cumulative log return (%)"); ax.legend(fontsize=8, frameon=False)
ax.set_title("Figure 4. Basket timing rule on the EM activity factor (shaded = VIX > 25)", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(RF, "fig4_factor_strategy.png"), dpi=200); plt.close(fig)

txt = "\n".join(md); open(os.path.join(RT, "table_factor_robustness.md"), "w", encoding="utf-8").write(txt); print(txt)
