"""
Step 13: main table for the reframed paper.

EM activity factor F_t = cross-country mean of the raw standardized congestion innovations of
the 12 main countries in week t. Idiosyncratic component e_{i,t} = x_{i,t} - F_t.

Panel specification (headline, "L6" controls from step 12):
  r_{i,t+1} = a_{i,y} + a_{S,m} + b1 F_t + b2 F_t S_t + c1 e_{i,t} + c2 e_{i,t} S_t + d S_t
              + holiday dummies + controls + controls x S_t + log VIX + u
  country x year FE, state x calendar-month FE, SEs clustered by week; Driscoll-Kraay also.
States: S = 1[VIX > 25] (main) and S = 1[VIX in top tercile of sample] (pre-specified alternative).
Samples: ex-lockdown; within 2020 H2; within 2021; within 2022.
Time-series specification: equal-weight EM basket next-week return on F_t, F_t S_t, S_t,
controls (HAC 4 lags), ex-lockdown and by year.
Outputs: results/tables/table_main_v2.csv, .md
Run: py -I pipeline/13_factor_table.py
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
RT = os.path.join(ROOT, "results", "tables")
CTRL = {"ret_etf_f1": ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"],
        "ret_idx_f1": ["ret_idx", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]}


def main():
    w = mt.prep().sort_values(["country", "date"])
    w["year"] = w.date.dt.year.astype(str); w["cy"] = w["country"] + "_" + w["year"]
    w, HC = d12.add_holidays(w)
    w["F"] = w.groupby("date")["x_raw"].transform("mean")
    w["e"] = w["x_raw"] - w["F"]
    w["log_vix_lvl"] = np.log(w["vix"])
    terc = rb.exlock(w)["vix"].quantile(2 / 3)
    w["S_terc"] = (w["vix"] > terc).astype(float)
    base = rb.exlock(w)
    rows, md = [], [f"# Main table v2: EM congestion activity factor and state-dependent pricing\n\nF = cross-country mean congestion innovation; e = country-specific residual. VIX top-tercile cutoff = {terc:.1f}.\n"]

    def panel(d, tgt, state, dk=None, label=""):
        d = d.copy(); d["sm"] = "S" + d[state].astype(int).astype(str) + "_" + d["moy"].astype(str)
        ctrl = CTRL[tgt]
        for c in ctrl:
            d[c + "_S"] = d[c] * d[state]
        xcols = [("F", d["F"]), ("F_x_S", d["F"] * d[state]), ("e", d["e"]), ("e_x_S", d["e"] * d[state]), ("S", d[state])]
        extra = ctrl + [c + "_S" for c in ctrl] + HC + ["log_vix_lvl"]
        fe = ["cy", "sm"] if d["year"].nunique() > 1 else ["country", "sm"]
        r = d12.fit(d, tgt, xcols, fe, extra, dk_lags=dk)
        return {"spec": label, **r}

    for tgt in ["ret_etf_f1", "ret_idx_f1"]:
        md.append(f"\n## Panel: {tgt}\n\n| sample | state | n | F calm | t | F x S | t | F stress | e calm | t | e x S | t |\n|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for lab, d in [("ex-lockdown", base), ("2020 H2", w[(w.date >= "2020-07-01") & (w.date <= "2020-12-31")]),
                       ("2021", w[w.year == "2021"]), ("2022", w[w.year == "2022"])]:
            for state in ["S_vix25", "S_terc"]:
                if d[state].nunique() < 2:
                    continue
                for dk in [None, 4]:
                    r = panel(d, tgt, state, dk=dk, label=f"{lab} {state} {'DK' if dk else 'cluster'}")
                    r.update({"target": tgt, "sample": lab, "state": state, "se": "DK4" if dk else "week-cluster"}); rows.append(r)
                    if dk is None:
                        md.append(f"| {lab} | {state} | {r['n']} | {r['b_F']:.3f} | {r['t_F']:.2f} | {r['b_F_x_S']:.3f} | {r['t_F_x_S']:.2f} | {r['b_F']+r['b_F_x_S']:.3f} | {r['b_e']:.3f} | {r['t_e']:.2f} | {r['b_e_x_S']:.3f} | {r['t_e_x_S']:.2f} |")
                    else:
                        md.append(f"| {lab} | {state} (DK t) | {r['n']} |  | {r['t_F']:.2f} |  | {r['t_F_x_S']:.2f} |  |  | {r['t_e']:.2f} |  | {r['t_e_x_S']:.2f} |")

    # time-series: EM basket on F
    raw = rb.W[rb.W.country.isin(rb.MAIN)][["date", "country", "ret_etf_f1", "ret_etf"]]
    bask = raw.groupby("date")[["ret_etf_f1", "ret_etf"]].mean()
    ts = w.groupby("date").agg(F=("F", "first"), S_vix25=("S_vix25", "first"), S_terc=("S_terc", "first"),
                               ret_em=("ret_em", "first"), d_vix=("d_vix", "first"), ret_brent=("ret_brent", "first"),
                               d_dxy=("d_dxy", "first"), d_us10y=("d_us10y", "first"), log_vix_lvl=("log_vix_lvl", "first"))
    ts = ts.join(bask).dropna()
    ts["year"] = ts.index.year
    md.append("\n## Time series: equal-weight EM basket next-week return (%) on F (HAC 4)\n\n| sample | state | n | F calm | t | F x S | t | F stress | R2 |\n|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for lab, d in [("ex-lockdown", ts[(ts.index < "2020-03-01") | (ts.index > "2020-06-30")]), ("2020 H2", ts[(ts.index >= "2020-07-01") & (ts.index <= "2020-12-31")]),
                   ("2021", ts[ts.year == 2021]), ("2022", ts[ts.year == 2022])]:
        for state in ["S_vix25", "S_terc"]:
            if d[state].nunique() < 2:
                continue
            X = pd.DataFrame({"F": d["F"], "FxS": d["F"] * d[state], "S": d[state], "ret_etf": d["ret_etf"], "ret_em": d["ret_em"],
                              "d_vix": d["d_vix"], "ret_brent": d["ret_brent"], "d_dxy": d["d_dxy"], "d_us10y": d["d_us10y"], "lvix": d["log_vix_lvl"]})
            X = sm.add_constant(X)
            m = sm.OLS(100 * d["ret_etf_f1"].values, X.values).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
            rows.append({"spec": f"TS {lab} {state}", "target": "basket_pct", "sample": lab, "state": state, "n": int(len(d)),
                         "b_F": m.params[1], "t_F": m.tvalues[1], "b_F_x_S": m.params[2], "t_F_x_S": m.tvalues[2], "r2": m.rsquared})
            md.append(f"| {lab} | {state} | {len(d)} | {m.params[1]:.3f} | {m.tvalues[1]:.2f} | {m.params[2]:.3f} | {m.tvalues[2]:.2f} | {m.params[1]+m.params[2]:.3f} | {m.rsquared:.3f} |")
    # descriptive: SD of F, share of variance common
    md.append(f"\nSD of F (ex-lockdown): {base.groupby('date')['F'].first().std():.3f}; mean within-week cross-country SD of x: {base.groupby('date')['x_raw'].std().mean():.3f}; share of x variance that is common: {base['F'].var()/base['x_raw'].var():.3f}")
    pd.DataFrame(rows).to_csv(os.path.join(RT, "table_main_v2.csv"), index=False)
    txt = "\n".join(md); open(os.path.join(RT, "table_main_v2.md"), "w", encoding="utf-8").write(txt); print(txt)


if __name__ == "__main__":
    main()
