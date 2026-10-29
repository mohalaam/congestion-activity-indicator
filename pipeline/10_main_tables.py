"""
Step 10: headline tables and figures for the paper.

Main specification (per country i, week t, h = 1 week):
  r_{i,t+1} = a_{i,m(t)} + b1 * x_{i,t} + b2 * x_{i,t} x S_t + b3 * S_t + g' controls_{i,t} + e
  x = congestion innovation (4-week), deseasonalized by removing the country x month-of-year
      mean, standardized within country; S = 1[VIX_t > 25]; a_{i,m} = country x calendar-month
      fixed effects; controls = own same-week return, MSCI EM return, dVIX, Brent, DXY, US10y.
  SEs clustered by week. Samples: ex-lockdown (2020-07..2023-02) and post-2021-07.

Outputs (results/tables and results/figures):
  table1_headline.csv / .md        4 specs x 2 targets x 2 samples
  fig1_vix_threshold_sweep.png     interaction coefficient vs VIX cutoff (18..32) with 95% CI
  fig2_state_betas.png             calm vs stress conditional betas, both targets, both samples
  table2_volatility_quantile.csv   next-week log RV and quantile regressions, deseasonalized + calendar FE
  table3_placebos.csv              shuffle placebo (500 draws) and 52-week-lag placebo under the main spec
  table4_descriptives.csv          sample descriptives per country
Run: py -I pipeline/10_main_tables.py
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
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
P = os.path.join(ROOT, "data_proc")
RT = os.path.join(ROOT, "results", "tables")
RF = os.path.join(ROOT, "results", "figures")
os.makedirs(RT, exist_ok=True); os.makedirs(RF, exist_ok=True)
rng = np.random.default_rng(7)
CTRL = rb.CTRL
MAIN = rb.MAIN


def prep():
    w = rb.build_panel().sort_values(["country", "date"]).copy()
    w["moy"] = w.date.dt.month
    w["cm"] = w["country"] + "_" + w["moy"].astype(str)
    w["x_raw"] = w["cong_innov4"]
    w["x_ds"] = w["cong_innov4"] - w.groupby(["country", "moy"])["cong_innov4"].transform("mean")
    w["x_ds"] = w.groupby("country")["x_ds"].transform(lambda s: (s - s.mean()) / s.std())
    w["x_lag52"] = w.groupby("country")["x_ds"].shift(52)
    # realized vol for index too
    mk = rb.mk
    idx = mk[mk.series == "index"].pivot_table(index="date", columns="country", values="value").sort_index()
    idx = idx.loc[:, idx.count() > 200]
    lrv_i = np.log((np.log(idx).diff() ** 2).resample("W-FRI").sum(min_count=3).replace(0, np.nan))
    lrv_i = lrv_i.stack().rename("lrv_idx").reset_index().rename(columns={"level_1": "country"})
    w = w.merge(lrv_i, on=["date", "country"], how="left").rename(columns={"lrv": "lrv_etf"}).sort_values(["country", "date"])
    glob = mk[mk.country == "GLOBAL"].pivot_table(index="date", columns="series", values="value").sort_index()
    w = w.merge(np.log(glob["vix"]).resample("W-FRI").last().rename("log_vix"), left_on="date", right_index=True, how="left")
    for v in ("lrv_etf", "lrv_idx"):
        g = w.groupby("country")[v]
        w[f"{v}_f1"] = g.shift(-1); w[f"{v}_m4"] = g.transform(lambda s: s.rolling(4).mean()); w[f"{v}_m13"] = g.transform(lambda s: s.rolling(13).mean())
    return w


def reg(d, tgt, x, state="S_vix25", fe="cm", cluster=True, extra_ctrl=None):
    d = d.copy(); d["sx"] = d[x] * d[state]
    ctrl = CTRL.get(tgt, extra_ctrl or [])
    cols = [tgt, x, "sx", state] + ctrl
    d = d.dropna(subset=cols)
    D = pd.get_dummies(d[fe]).astype(float)
    X = pd.concat([d[[x, "sx", state] + ctrl], D], axis=1)
    if cluster:
        m = sm.OLS(d[tgt].values, X.values).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["date"])[0]})
    else:
        m = sm.OLS(d[tgt].values, X.values).fit()
    cov = m.cov_params()
    se_stress = np.sqrt(cov[0, 0] + cov[1, 1] + 2 * cov[0, 1])
    return {"n": int(len(d)), "weeks": int(d.date.nunique()), "b_calm": m.params[0], "se_calm": m.bse[0], "t_calm": m.tvalues[0],
            "b_inter": m.params[1], "se_inter": m.bse[1], "t_inter": m.tvalues[1], "p_inter": m.pvalues[1],
            "b_stress": m.params[0] + m.params[1], "se_stress": se_stress, "t_stress": (m.params[0] + m.params[1]) / se_stress,
            "share_stress": float(d[state].mean()), "r2": m.rsquared}


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def main():
    w = prep()
    S = {"ex_lockdown": rb.exlock(w), "post_2021-07": w[w.date >= "2021-07-01"]}
    TGT = {"ret_etf_f1": "USD ETF, next week", "ret_idx_f1": "Local index, next week"}

    # ------------------------------------------------ Table 1
    specs = [("x_raw", "country", "(1) raw, country FE"), ("x_raw", "cm", "(2) raw, country x month FE"),
             ("x_ds", "country", "(3) deseasonalized, country FE"), ("x_ds", "cm", "(4) deseasonalized, country x month FE")]
    rows, md = [], ["# Table 1. State-dependent return response to congestion innovations\n",
                    "Dependent: next-week return (SD units). x = congestion innovation (SD units). S = 1[VIX>25]. SEs clustered by week. *, **, *** = 10, 5, 1%.\n"]
    for lab, d in S.items():
        for tgt, tname in TGT.items():
            md.append(f"\n## {tname}, sample {lab}\n\n| | " + " | ".join(s[2] for s in specs) + " |\n|---|" + "---|" * len(specs))
            res = [reg(d, tgt, x, fe=fe) for x, fe, _ in specs]
            for x, fe, name in specs:
                r = reg(d, tgt, x, fe=fe)
                rows.append({"sample": lab, "target": tgt, "spec": name, **r})
            def line(key, label, sek, tk, pk=None):
                cells = []
                for r in res:
                    p = 2 * (1 - __import__("scipy").stats.norm.cdf(abs(r[tk])))
                    cells.append(f"{r[key]:.3f}{stars(p)} ({r[sek]:.3f})")
                return f"| {label} | " + " | ".join(cells) + " |"
            md.append(line("b_calm", "x (calm state)", "se_calm", "t_calm"))
            md.append(line("b_inter", "x times S (interaction)", "se_inter", "t_inter"))
            md.append(line("b_stress", "x in stress state (sum)", "se_stress", "t_stress"))
            md.append("| Obs. / weeks / share stress | " + " | ".join(f"{r['n']} / {r['weeks']} / {r['share_stress']:.2f}" for r in res) + " |")
    t1 = pd.DataFrame(rows); t1.to_csv(os.path.join(RT, "table1_headline.csv"), index=False)
    open(os.path.join(RT, "table1_headline.md"), "w", encoding="utf-8").write("\n".join(md))

    # ------------------------------------------------ Figure 1: VIX threshold sweep
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for ax, (lab, d) in zip(axes, S.items()):
        for tgt, col, mk_ in (("ret_etf_f1", "#1f4e79", "o"), ("ret_idx_f1", "#c0504d", "s")):
            cut, b, lo, hi = [], [], [], []
            for c in range(18, 33):
                dd = d.copy(); dd["S_cut"] = (dd["vix"] > c).astype(float)
                if dd["S_cut"].mean() < 0.05 or dd["S_cut"].mean() > 0.95:
                    continue
                r = reg(dd, tgt, "x_ds", state="S_cut", fe="cm")
                cut.append(c); b.append(r["b_inter"]); lo.append(r["b_inter"] - 1.96 * r["se_inter"]); hi.append(r["b_inter"] + 1.96 * r["se_inter"])
            ax.plot(cut, b, marker=mk_, color=col, lw=1.5, label=TGT[tgt])
            ax.fill_between(cut, lo, hi, color=col, alpha=0.12)
        ax.axhline(0, color="k", lw=0.8); ax.axvline(25, color="grey", ls="--", lw=0.8)
        ax.set_title(f"Sample: {lab.replace('_', ' ')}", fontsize=10); ax.set_xlabel("VIX cutoff defining the stress state")
    axes[0].set_ylabel("Interaction coefficient (SD units)"); axes[0].legend(fontsize=8, frameon=False)
    fig.suptitle("Figure 1. Interaction of congestion innovation with the stress state, by VIX cutoff (95% CI, week-clustered)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(RF, "fig1_vix_threshold_sweep.png"), dpi=200); plt.close(fig)

    # ------------------------------------------------ Figure 2: calm vs stress betas
    fig, ax = plt.subplots(figsize=(7, 3.6))
    labels, calm, stress, ce, se_ = [], [], [], [], []
    for lab, d in S.items():
        for tgt, tname in TGT.items():
            r = reg(d, tgt, "x_ds", fe="cm")
            labels.append(f"{tname}\n{lab.replace('_', ' ')}"); calm.append(r["b_calm"]); stress.append(r["b_stress"]); ce.append(1.96 * r["se_calm"]); se_.append(1.96 * r["se_stress"])
    xx = np.arange(len(labels)); wd = 0.36
    ax.bar(xx - wd / 2, calm, wd, yerr=ce, color="#7f7f7f", label="Calm (VIX <= 25)", capsize=3)
    ax.bar(xx + wd / 2, stress, wd, yerr=se_, color="#c0504d", label="Stress (VIX > 25)", capsize=3)
    ax.axhline(0, color="k", lw=0.8); ax.set_xticks(xx); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Return response (SD per SD)"); ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title("Figure 2. Conditional response of next-week returns to congestion innovations (95% CI)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(RF, "fig2_state_betas.png"), dpi=200); plt.close(fig)

    # ------------------------------------------------ Table 2: volatility and quantiles, deseasonalized + calendar FE
    rows = []
    for lab, d in S.items():
        for v, vname in (("lrv_etf", "USD ETF"), ("lrv_idx", "Local index")):
            ctrl = [v, f"{v}_m4", f"{v}_m13", "log_vix", "ret_em", "d_vix"]
            dd = d.dropna(subset=[f"{v}_f1", "x_ds"] + ctrl)
            X = pd.concat([dd[["x_ds"] + ctrl], pd.get_dummies(dd["cm"]).astype(float)], axis=1)
            m = sm.OLS(dd[f"{v}_f1"].values, X.values).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(dd["date"])[0]})
            rows.append({"sample": lab, "block": "volatility", "target": f"{vname} next-week log RV", "stat": "x_ds", "n": int(len(dd)), "beta": m.params[0], "se": m.bse[0], "t": m.tvalues[0], "p": m.pvalues[0]})
            # with state interaction
            r = reg(dd, f"{v}_f1", "x_ds", fe="cm", extra_ctrl=ctrl)
            rows.append({"sample": lab, "block": "volatility", "target": f"{vname} next-week log RV", "stat": "x_ds calm", "n": r["n"], "beta": r["b_calm"], "se": r["se_calm"], "t": r["t_calm"], "p": np.nan})
            rows.append({"sample": lab, "block": "volatility", "target": f"{vname} next-week log RV", "stat": "x_ds x S", "n": r["n"], "beta": r["b_inter"], "se": r["se_inter"], "t": r["t_inter"], "p": r["p_inter"]})
        for tgt, tname in TGT.items():
            dd = d.dropna(subset=[tgt, "x_ds", "ret_em", "d_vix"]).copy()
            for c in [tgt, "x_ds", "ret_em", "d_vix"]:
                dd[c] = dd[c] - dd.groupby("cm")[c].transform("mean")  # calendar FE by demeaning
            X = sm.add_constant(dd[["x_ds", "ret_em", "d_vix"]].values)
            for tau in (0.1, 0.25, 0.5, 0.75, 0.9):
                qm = QuantReg(dd[tgt].values, X).fit(q=tau, max_iter=5000)
                rows.append({"sample": lab, "block": "quantile", "target": tname, "stat": f"tau={tau}", "n": int(len(dd)), "beta": qm.params[1], "se": qm.bse[1], "t": qm.tvalues[1], "p": qm.pvalues[1]})
    t2 = pd.DataFrame(rows); t2.to_csv(os.path.join(RT, "table2_volatility_quantile.csv"), index=False)

    # ------------------------------------------------ Table 3: placebos under the main spec
    rows = []
    for lab, d in S.items():
        for tgt, tname in TGT.items():
            actual = reg(d, tgt, "x_ds", fe="cm")
            ts = []
            d0 = d.dropna(subset=[tgt, "x_ds", "S_vix25"] + CTRL[tgt]).copy()
            for k in range(500):
                dp = d0.copy()
                dp["x_ds"] = dp.groupby("country")["x_ds"].transform(lambda s: s.sample(frac=1, random_state=int(rng.integers(1e9))).values)
                try:
                    ts.append(reg(dp, tgt, "x_ds", fe="cm", cluster=False)["t_inter"])
                except Exception:
                    continue
            ts = np.array(ts); act_nc = reg(d0, tgt, "x_ds", fe="cm", cluster=False)["t_inter"]
            rows.append({"sample": lab, "target": tname, "placebo": "within-country shuffle (500)", "actual_t": act_nc,
                         "placebo_mean_t": ts.mean(), "placebo_sd_t": ts.std(), "p_value_placebo": float((ts >= act_nc).mean())})
            r = reg(d, tgt, "x_lag52", fe="cm")
            rows.append({"sample": lab, "target": tname, "placebo": "signal lagged 52 weeks", "actual_t": actual["t_inter"],
                         "placebo_b_inter": r["b_inter"], "placebo_t_inter": r["t_inter"], "n": r["n"]})
    t3 = pd.DataFrame(rows); t3.to_csv(os.path.join(RT, "table3_placebos.csv"), index=False)

    # ------------------------------------------------ Table 4: descriptives
    d = rb.exlock(w)
    t4 = d.groupby("country").agg(weeks=("date", "nunique"), mean_congestion=("cong_level", "mean"),
                                  sd_innov=("cong_innov4", "std"), mean_ret_etf_pct=("ret_etf", lambda s: 100 * s.mean()),
                                  sd_ret_etf_pct=("ret_etf", lambda s: 100 * s.std()),
                                  share_stress=("S_vix25", "mean")).round(3)
    t4.to_csv(os.path.join(RT, "table4_descriptives.csv"))

    pd.set_option("display.width", 220)
    print("\n".join(md))
    print("\n=== Table 2 (deseasonalized signal, country x month FE) ===")
    print(t2.round(3).to_string(index=False))
    print("\n=== Table 3 placebos ===")
    print(t3.round(3).to_string(index=False))
    print("\nFigures saved:", os.listdir(RF))


if __name__ == "__main__":
    main()
