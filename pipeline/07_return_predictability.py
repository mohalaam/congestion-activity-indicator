"""
Step 07: return predictability from congestion innovations and nowcast surprises.

A. Weekly panel (country x week): next-week and next-4-week returns on congestion innovations
   r_{i,t+1} = a_i + b * cong_innov_{i,t} + g' controls_t + e
   - returns: local index (ret_idx), USD country ETF (ret_etf), FX (ret_fx, + = appreciation)
   - signals: d_cong (weekly change), cong_innov4 (vs 4-week mean), cong_innov13 (vs 13-week mean)
   - controls (same week t): ret_em, d_vix, ret_brent, d_dxy, d_us10y, own lagged return
   - country fixed effects; SEs clustered by week (cross-sectional dependence); signals and
     returns standardized within country so b is in SD units.
   - samples: full (2020-01..2023-02), ex-lockdown (drop 2020-03..2020-06), post-2021-07.
B. Country sort: each week rank countries by cong_innov4, long top third / short bottom third,
   hold next week (USD ETF returns). Mean, t, annualized Sharpe; also by subsample.
C. Monthly panel: next-month returns on monthly congestion innovation and on the pooled-bridge
   nowcast surprise (data_proc/nowcast_surprises.csv), Newey-West (3 lags) with country FE.
D. Sector returns (Turkey, India, Poland sectors available): next-week sector return on
   cong_innov4 with the same design.

Outputs: results/returns_weekly.csv, returns_monthly.csv, returns_sort.csv, returns_sectors.csv
Run: py -I pipeline/07_return_predictability.py
"""
import os
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data_proc")
R = os.path.join(ROOT, "results")
os.makedirs(R, exist_ok=True)

W = pd.read_csv(os.path.join(P, "weekly_panel.csv"), parse_dates=["date"])
M = pd.read_csv(os.path.join(P, "monthly_panel.csv"), parse_dates=["date"])
S = pd.read_csv(os.path.join(P, "nowcast_surprises.csv"), parse_dates=["date"])
MAIN = ["Turkey", "Poland", "Brazil", "South Africa", "India", "Saudi Arabia", "Mexico",
        "Indonesia", "Thailand", "Egypt", "Malaysia", "Philippines"]
LOCK = (pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-30"))
CONTROLS = ["ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]


def zscore_within(df, cols):
    out = df.copy()
    for c in cols:
        if c in out:
            out[c] = out.groupby("country")[c].transform(lambda s: (s - s.mean()) / s.std())
    return out


def fe_reg(df, y, x, controls, cluster="date"):
    cols = [y, x] + controls
    d = df.dropna(subset=cols).copy()
    if len(d) < 60 or d.country.nunique() < 3:
        return None
    X = pd.concat([d[[x] + controls], pd.get_dummies(d["country"], drop_first=False).astype(float)], axis=1)
    m = sm.OLS(d[y].values, X.values).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    i = list(X.columns).index(x)
    return {"n": int(len(d)), "countries": int(d.country.nunique()), "beta": m.params[i],
            "t": m.tvalues[i], "p": m.pvalues[i], "r2_within": m.rsquared}


def samples(df):
    yield "full", df
    yield "ex_lockdown", df[(df.date < LOCK[0]) | (df.date > LOCK[1])]
    yield "post_2021-07", df[df.date >= "2021-07-01"]


def main():
    # ------------------------------------------------------------ A. weekly
    w = W[W.country.isin(MAIN)].copy()
    sig = ["d_cong", "cong_innov4", "cong_innov13"]
    rets = [c for c in ["ret_idx", "ret_etf", "ret_fx"] if c in w]
    w = zscore_within(w, sig + rets + [f"{r}_f1" for r in rets] + [f"{r}_f4" for r in rets])
    rows = []
    for lab, d in samples(w):
        for r in rets:
            for h in ("f1", "f4"):
                for s in sig:
                    ctrl = CONTROLS + [r]  # own same-week return as control
                    res = fe_reg(d, f"{r}_{h}", s, ctrl)
                    if res:
                        rows.append({"sample": lab, "ret": r, "horizon": h, "signal": s, **res})
    wk = pd.DataFrame(rows)
    wk.to_csv(os.path.join(R, "returns_weekly.csv"), index=False)

    # ------------------------------------------------------------ B. country sort
    srt = []
    d = W[W.country.isin(MAIN)].dropna(subset=["cong_innov4", "ret_etf_f1"]).copy()
    d["rank"] = d.groupby("date")["cong_innov4"].rank(pct=True)
    d["n_wk"] = d.groupby("date")["country"].transform("count")
    d = d[d.n_wk >= 6]
    d["pos"] = np.where(d["rank"] > 2 / 3, 1.0, np.where(d["rank"] <= 1 / 3, -1.0, 0.0))
    ls = d[d.pos != 0].groupby("date").apply(lambda g: (g.pos * g.ret_etf_f1).sum() / (g.pos == 1).sum())
    ls.name = "ls_ret"
    ls = ls.to_frame()
    ls["long"] = d[d.pos == 1].groupby("date")["ret_etf_f1"].mean()
    ls["short"] = d[d.pos == -1].groupby("date")["ret_etf_f1"].mean()
    ls["ew_all"] = d.groupby("date")["ret_etf_f1"].mean()
    ls = ls.reset_index()
    for lab, dd in samples(ls):
        for col in ["ls_ret", "long", "short", "ew_all"]:
            x = dd[col].dropna()
            if len(x) < 20:
                continue
            m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
            srt.append({"sample": lab, "portfolio": col, "n_weeks": int(len(x)),
                        "mean_weekly_pct": 100 * x.mean(), "t_NW": m.tvalues[0],
                        "sharpe_ann": x.mean() / x.std() * np.sqrt(52), "hit_rate": float((x > 0).mean())})
    srt = pd.DataFrame(srt)
    srt.to_csv(os.path.join(R, "returns_sort.csv"), index=False)
    ls.to_csv(os.path.join(R, "returns_sort_series.csv"), index=False)

    # ------------------------------------------------------------ C. monthly
    m = M[M.country.isin(MAIN)].copy()
    S2 = S[["date", "country", "surprise_vs_AR", "realized_minus_nowcast", "nowcast_cong"]].copy()
    S2["date"] = S2["date"] + pd.offsets.MonthEnd(0)
    m = m.merge(S2, on=["date", "country"], how="left")
    msig = ["d_cong_m", "cong_m_innov", "cong_slope", "surprise_vs_AR", "nowcast_cong"]
    mrets = [c for c in ["ret_idx_m", "ret_etf_m", "ret_fx_m"] if c in m]
    m = zscore_within(m, msig + mrets + [f"{r}_f1" for r in mrets] + [f"{r}_f3" for r in mrets if f"{r}_f3" in m])
    rows = []
    for lab, d in samples(m):
        for r in mrets:
            for h in ("f1", "f3"):
                if f"{r}_{h}" not in d:
                    continue
                for s in msig:
                    if s not in d:
                        continue
                    dd = d.dropna(subset=[f"{r}_{h}", s, r])
                    if len(dd) < 40 or dd.country.nunique() < 3:
                        continue
                    X = pd.concat([dd[[s, r]], pd.get_dummies(dd["country"]).astype(float)], axis=1)
                    mod = sm.OLS(dd[f"{r}_{h}"].values, X.values).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
                    rows.append({"sample": lab, "ret": r, "horizon": h, "signal": s, "n": int(len(dd)),
                                 "countries": int(dd.country.nunique()), "beta": mod.params[0],
                                 "t_NW": mod.tvalues[0], "p": mod.pvalues[0]})
    mo = pd.DataFrame(rows)
    mo.to_csv(os.path.join(R, "returns_monthly.csv"), index=False)

    # ------------------------------------------------------------ D. sectors (weekly)
    sec_cols = [c for c in W.columns if c.startswith("ret_sector_") and c.endswith("_f1")]
    rows = []
    for sc in sec_cols:
        base = sc[:-3]
        d = W.dropna(subset=[sc, "cong_innov4", base]).copy()
        if d.country.nunique() == 0:
            continue
        d = zscore_within(d, [sc, base, "cong_innov4"])
        for lab, dd in samples(d):
            dd = dd.dropna(subset=[sc, "cong_innov4", base] + CONTROLS)
            if len(dd) < 40:
                continue
            X = sm.add_constant(dd[["cong_innov4", base] + CONTROLS].values)
            mod = sm.OLS(dd[sc].values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
            rows.append({"sample": lab, "sector": base.replace("ret_sector_", ""),
                         "countries": ",".join(sorted(dd.country.unique())), "n": int(len(dd)),
                         "beta": mod.params[1], "t_NW": mod.tvalues[1], "p": mod.pvalues[1]})
    se = pd.DataFrame(rows)
    se.to_csv(os.path.join(R, "returns_sectors.csv"), index=False)

    pd.set_option("display.width", 220)
    print("=== A. Weekly panel: next-period return (SD units) on congestion signal (SD units), FE, week-clustered SE ===")
    print(wk.pivot_table(index=["ret", "horizon", "signal"], columns="sample", values=["beta", "t"]).round(3).to_string())
    print("\n=== B. Weekly country sort on cong_innov4 (USD ETF returns, next week) ===")
    print(srt.round(3).to_string(index=False))
    print("\n=== C. Monthly panel ===")
    print(mo.pivot_table(index=["ret", "horizon", "signal"], columns="sample", values=["beta", "t_NW"]).round(3).to_string())
    print("\n=== D. Sectors (weekly, next-week sector return on cong_innov4) ===")
    print(se.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
