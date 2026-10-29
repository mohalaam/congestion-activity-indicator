"""
Step 11: economic significance, Figure 1, by-country and country-exclusion tables.

A. State-conditional timing rule on USD country ETFs (weekly, ex-lockdown):
   position_{i,t} = +1 if (stress and x>0) or (calm and x<0); -1 otherwise  [sign rule]
   position_{i,t} = x_{i,t} * (2 S_t - 1)                                   [linear rule, scaled]
   Portfolio = equal-weighted average over countries of position x next-week ETF return.
   Benchmarks: equal-weight long-only EM basket; unconditional rule (long x>0); calm-only and
   stress-only legs. Metrics: mean, SD, annualized Sharpe, max drawdown, hit rate, turnover,
   break-even one-way cost, Newey-West t of the mean. Costs applied at 10 and 25 bp one-way.
   Figure 4: cumulative log returns.
B. Figure 1: weekly deseasonalized congestion innovation per country with stress weeks shaded.
C. By-country estimates of equation (2) (OLS, HAC 4 lags, calendar-month FE) on USD ETF 1-week.
D. Country-exclusion: headline spec dropping each country in turn.
Outputs: results/tables/table_strategy.csv, table_bycountry.csv, table_exclusion.csv,
         results/figures/fig1_congestion_series.png, fig4_strategy_cumret.png
Run: py -I pipeline/11_strategy_and_appendix.py
"""
import os
import sys
import importlib
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
rb = importlib.import_module("09_robustness")
mt = importlib.import_module("10_main_tables")
RT = os.path.join(ROOT, "results", "tables"); RF = os.path.join(ROOT, "results", "figures")


def perf(r, label, ann=52):
    r = r.dropna()
    m = sm.OLS(r.values, np.ones(len(r))).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    cum = r.cumsum(); dd = (cum - cum.cummax()).min()
    return {"portfolio": label, "weeks": int(len(r)), "mean_weekly_pct": 100 * r.mean(), "sd_weekly_pct": 100 * r.std(),
            "t_NW": m.tvalues[0], "sharpe_ann": r.mean() / r.std() * np.sqrt(ann), "max_drawdown_pct": 100 * dd,
            "hit_rate": float((r > 0).mean()), "cum_log_ret_pct": 100 * r.sum()}


def main():
    w = mt.prep()
    raw = rb.W[["date", "country", "ret_etf_f1"]].rename(columns={"ret_etf_f1": "ret_raw"})
    d = rb.exlock(w).merge(raw, on=["date", "country"], how="left")
    d["ret_etf_f1"] = d["ret_raw"]  # use RAW weekly log returns, not the standardized ones
    d = d.dropna(subset=["ret_etf_f1", "x_ds", "S_vix25"]).copy()
    d["state_sign"] = 2 * d["S_vix25"] - 1
    d["pos_sign"] = np.sign(d["x_ds"]) * d["state_sign"]
    d["pos_lin"] = (d["x_ds"] * d["state_sign"]).clip(-2, 2) / 2
    d["pos_uncond"] = np.sign(d["x_ds"])
    d["pos_calm"] = np.where(d["S_vix25"] == 0, -np.sign(d["x_ds"]), 0.0)
    d["pos_stress"] = np.where(d["S_vix25"] == 1, np.sign(d["x_ds"]), 0.0)
    g = d.groupby("date")
    series = {
        "State-conditional sign rule": g.apply(lambda x: (x.pos_sign * x.ret_etf_f1).mean()),
        "State-conditional linear rule": g.apply(lambda x: (x.pos_lin * x.ret_etf_f1).mean()),
        "Calm leg only (short on +innovation)": g.apply(lambda x: (x.pos_calm * x.ret_etf_f1).mean()),
        "Stress leg only (long on +innovation)": g.apply(lambda x: (x.pos_stress * x.ret_etf_f1).mean()),
        "Unconditional sign rule": g.apply(lambda x: (x.pos_uncond * x.ret_etf_f1).mean()),
        "Equal-weight EM basket (long only)": g["ret_etf_f1"].mean(),
    }
    rows = [perf(s, k) for k, s in series.items()]
    # turnover and costs for the sign rule
    pos = d.pivot_table(index="date", columns="country", values="pos_sign").fillna(0)
    turn = pos.diff().abs().sum(axis=1) / pos.shape[1]  # average absolute position change per country
    rows[0]["turnover_per_week"] = float(turn.mean())
    for bp in (10, 25):
        net = series["State-conditional sign rule"] - turn * bp / 1e4  # one-way cost per unit of position traded
        r = perf(net, f"Sign rule net of {bp} bp one-way")
        r["turnover_per_week"] = float(turn.mean()); rows.append(r)
    mean_gross = series["State-conditional sign rule"].mean()
    rows[0]["breakeven_oneway_bp"] = float(mean_gross / turn.mean() * 1e4)
    st = pd.DataFrame(rows); st.to_csv(os.path.join(RT, "table_strategy.csv"), index=False)

    # Figure 4
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for k, c in (("State-conditional sign rule", "#1f4e79"), ("Unconditional sign rule", "#7f7f7f"),
                 ("Equal-weight EM basket (long only)", "#c0504d")):
        ax.plot(series[k].index, 100 * series[k].cumsum(), label=k, color=c, lw=1.6)
    sw = d.groupby("date")["S_vix25"].first()
    for t in sw[sw == 1].index:
        ax.axvspan(t - pd.Timedelta(days=6), t, color="grey", alpha=0.12, lw=0)
    ax.axhline(0, color="k", lw=0.8); ax.set_ylabel("Cumulative log return (%)"); ax.legend(fontsize=8, frameon=False)
    ax.set_title("Figure 4. Cumulative returns of the state-conditional rule vs benchmarks (USD ETFs, ex-lockdown; shaded = VIX > 25)", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(RF, "fig4_strategy_cumret.png"), dpi=200); plt.close(fig)

    # ---------------- B. Figure 1
    ww = w[w.country.isin(rb.MAIN)]
    fig, axes = plt.subplots(4, 3, figsize=(10, 8), sharex=True)
    for ax, (c, gdf) in zip(axes.ravel(), ww.groupby("country")):
        ax.plot(gdf.date, gdf.cong_level, color="#1f4e79", lw=1.0)
        ax.set_title(c, fontsize=9); ax.tick_params(labelsize=7)
        s = gdf.set_index("date")["S_vix25"]
        for t in s[s == 1].index:
            ax.axvspan(t - pd.Timedelta(days=6), t, color="grey", alpha=0.15, lw=0)
        ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-30"), color="#c0504d", alpha=0.10, lw=0)
    fig.suptitle("Figure 1. Weekly congestion level (% extra travel time), 12 emerging markets, 2020-2023. Grey = VIX > 25; red = lockdown months excluded", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(RF, "fig1_congestion_series.png"), dpi=200); plt.close(fig)

    # ---------------- C. by-country
    rows = []
    base = rb.exlock(w)
    for c, gdf in base.groupby("country"):
        gdf = gdf.dropna(subset=["ret_etf_f1", "x_ds", "S_vix25"] + rb.CTRL["ret_etf_f1"]).copy()
        if len(gdf) < 60:
            continue
        gdf["sx"] = gdf["x_ds"] * gdf["S_vix25"]
        X = pd.concat([gdf[["x_ds", "sx", "S_vix25"] + rb.CTRL["ret_etf_f1"]], pd.get_dummies(gdf["moy"]).astype(float)], axis=1)
        m = sm.OLS(gdf["ret_etf_f1"].values, X.values).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
        rows.append({"country": c, "n": int(len(gdf)), "b_calm": m.params[0], "t_calm": m.tvalues[0],
                     "b_inter": m.params[1], "t_inter": m.tvalues[1], "b_stress": m.params[0] + m.params[1]})
    bc = pd.DataFrame(rows); bc.to_csv(os.path.join(RT, "table_bycountry.csv"), index=False)

    # ---------------- D. country exclusion
    rows = []
    for c in sorted(base.country.unique()):
        r = mt.reg(base[base.country != c], "ret_etf_f1", "x_ds", fe="cm")
        rows.append({"dropped": c, **{k: r[k] for k in ("n", "b_calm", "t_calm", "b_inter", "t_inter", "b_stress", "t_stress")}})
    ex = pd.DataFrame(rows); ex.to_csv(os.path.join(RT, "table_exclusion.csv"), index=False)

    pd.set_option("display.width", 220)
    print("=== Strategy (USD ETFs, ex-lockdown) ==="); print(st.round(3).to_string(index=False))
    print("\n=== By country (USD ETF next week, calendar-month FE, HAC) ==="); print(bc.round(3).to_string(index=False))
    print("\n=== Country exclusion (headline spec) ==="); print(ex.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
