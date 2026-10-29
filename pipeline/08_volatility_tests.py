"""
Step 08: does congestion predict realized volatility, and do effects concentrate in high-VIX states?

A. Weekly realized variance from daily prices: RV_t = sum of squared daily log returns in week t
   (local index, USD ETF, FX). Target: log RV_{t+1} and log RV over the next 4 weeks.
   HAR-style baseline: log RV_t, mean log RV over t-3..t, mean over t-12..t, log VIX_t.
   Add congestion signals (cong_innov4, |cong_innov4|, d_cong, cong_innov13) with country FE,
   SEs clustered by week. Signals standardized within country.
B. State dependence: interact the congestion signal with HighVIX_t (VIX above its sample
   median, and alternatively above 25) for both the return and the volatility regressions.
C. Quantile regressions of next-week return on cong_innov4 at tau = 0.1, 0.25, 0.5, 0.75, 0.9
   (pooled, country-demeaned), to see whether congestion matters in the tails.
D. Monthly: next-month log RV on intra-month congestion slope and the nowcast surprise.

Outputs: results/vol_weekly.csv, vol_state.csv, vol_quantile.csv, vol_monthly.csv
Run: py -I pipeline/08_volatility_tests.py
"""
import os
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data_proc")
R = os.path.join(ROOT, "results")

mk = pd.read_csv(os.path.join(P, "market_daily.csv"), parse_dates=["date"])
W = pd.read_csv(os.path.join(P, "weekly_panel.csv"), parse_dates=["date"])
M = pd.read_csv(os.path.join(P, "monthly_panel.csv"), parse_dates=["date"])
S = pd.read_csv(os.path.join(P, "nowcast_surprises.csv"), parse_dates=["date"])
MAIN = ["Turkey", "Poland", "Brazil", "South Africa", "India", "Saudi Arabia", "Mexico",
        "Indonesia", "Thailand", "Egypt", "Malaysia", "Philippines"]
LOCK = (pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-30"))


def wide(series):
    w = mk[mk.series == series].pivot_table(index="date", columns="country", values="value").sort_index()
    return w.loc[:, w.count() > 200]


def weekly_rv(w):
    r = np.log(w).diff()
    rv = (r ** 2).resample("W-FRI").sum(min_count=3)
    return np.log(rv.replace(0, np.nan))


def monthly_rv(w):
    r = np.log(w).diff()
    rv = (r ** 2).resample("ME").sum(min_count=10)
    return np.log(rv.replace(0, np.nan))


def z_within(df, cols):
    out = df.copy()
    for c in cols:
        if c in out:
            out[c] = out.groupby("country")[c].transform(lambda s: (s - s.mean()) / s.std())
    return out


def fe_ols(d, y, xs, cluster="date"):
    d = d.dropna(subset=[y] + xs)
    if len(d) < 60 or d.country.nunique() < 3:
        return None
    X = pd.concat([d[xs], pd.get_dummies(d["country"]).astype(float)], axis=1)
    m = sm.OLS(d[y].values, X.values).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    return m, list(X.columns), int(len(d))


def samples(df):
    yield "full", df
    yield "ex_lockdown", df[(df.date < LOCK[0]) | (df.date > LOCK[1])]
    yield "post_2021-07", df[df.date >= "2021-07-01"]


def main():
    glob = mk[mk.country == "GLOBAL"].pivot_table(index="date", columns="series", values="value").sort_index()
    vix_w = np.log(glob["vix"]).resample("W-FRI").last().rename("log_vix")
    vix_lvl = glob["vix"].resample("W-FRI").last().rename("vix")

    # ---------------- build weekly RV panel
    rows = []
    for name, series in (("idx", "index"), ("etf", "etf_usd"), ("fx", "fx")):
        lrv = weekly_rv(wide(series))
        for c in lrv.columns:
            if c not in MAIN:
                continue
            s = lrv[c].to_frame(f"lrv_{name}")
            s["country"] = c
            rows.append(s.reset_index())
    rv = None
    for name in ("idx", "etf", "fx"):
        part = pd.concat([r for r in rows if f"lrv_{name}" in r.columns]) if any(f"lrv_{name}" in r.columns for r in rows) else None
        if part is None:
            continue
        rv = part if rv is None else rv.merge(part, on=["date", "country"], how="outer")
    w = W[W.country.isin(MAIN)].merge(rv, on=["date", "country"], how="left")
    w = w.merge(vix_w, left_on="date", right_index=True, how="left").merge(vix_lvl, left_on="date", right_index=True, how="left")
    w = w.sort_values(["country", "date"])
    for name in ("idx", "etf", "fx"):
        col = f"lrv_{name}"
        if col not in w:
            continue
        g = w.groupby("country")[col]
        w[f"{col}_f1"] = g.shift(-1)
        w[f"{col}_f4"] = g.transform(lambda s: np.log(np.exp(s).rolling(4).sum().shift(-4)))
        w[f"{col}_m4"] = g.transform(lambda s: s.rolling(4).mean())
        w[f"{col}_m13"] = g.transform(lambda s: s.rolling(13).mean())
    w["abs_innov4"] = w["cong_innov4"].abs()
    w["high_vix_med"] = (w["vix"] > w["vix"].median()).astype(float)
    w["high_vix_25"] = (w["vix"] > 25).astype(float)
    sig = ["cong_innov4", "abs_innov4", "d_cong", "cong_innov13"]
    w = z_within(w, sig)

    # ---------------- A. weekly volatility regressions
    out = []
    for lab, d in samples(w):
        for name in ("idx", "etf", "fx"):
            col = f"lrv_{name}"
            if col not in d:
                continue
            for h in ("f1", "f4"):
                base = [col, f"{col}_m4", f"{col}_m13", "log_vix", "ret_em", "d_vix"]
                for s in sig:
                    res = fe_ols(d, f"{col}_{h}", [s] + base)
                    if res is None:
                        continue
                    m, cols, n = res
                    out.append({"sample": lab, "target": f"{col}_{h}", "signal": s, "n": n,
                                "beta": m.params[0], "t": m.tvalues[0], "p": m.pvalues[0], "r2": m.rsquared})
    vol = pd.DataFrame(out)
    vol.to_csv(os.path.join(R, "vol_weekly.csv"), index=False)

    # ---------------- B. state dependence (returns and volatility)
    st = []
    wr = z_within(w, ["ret_idx_f1", "ret_etf_f1", "ret_fx_f1", "ret_idx_f4", "ret_etf_f4", "ret_fx_f4"])
    for lab, d in samples(wr):
        for state in ("high_vix_med", "high_vix_25"):
            d = d.copy()
            d["sig_x_state"] = d["cong_innov4"] * d[state]
            for tgt, base in [("ret_idx_f1", ["ret_idx", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]),
                              ("ret_etf_f1", ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]),
                              ("ret_etf_f4", ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]),
                              ("ret_fx_f4", ["ret_fx", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]),
                              ("lrv_etf_f1", ["lrv_etf", "lrv_etf_m4", "lrv_etf_m13", "log_vix", "ret_em", "d_vix"]),
                              ("lrv_idx_f1", ["lrv_idx", "lrv_idx_m4", "lrv_idx_m13", "log_vix", "ret_em", "d_vix"]),
                              ("lrv_fx_f1", ["lrv_fx", "lrv_fx_m4", "lrv_fx_m13", "log_vix", "ret_em", "d_vix"])]:
                if tgt not in d:
                    continue
                res = fe_ols(d, tgt, ["cong_innov4", "sig_x_state", state] + base)
                if res is None:
                    continue
                m, cols, n = res
                st.append({"sample": lab, "state": state, "target": tgt, "n": n,
                           "beta_low_state": m.params[0], "t_low": m.tvalues[0],
                           "beta_interaction": m.params[1], "t_inter": m.tvalues[1],
                           "beta_high_state": m.params[0] + m.params[1],
                           "share_high": float(d.dropna(subset=[tgt])[state].mean())})
    state_df = pd.DataFrame(st)
    state_df.to_csv(os.path.join(R, "vol_state.csv"), index=False)

    # ---------------- C. quantile regressions of next-week return
    q_rows = []
    for lab, d in samples(wr):
        for tgt in ("ret_idx_f1", "ret_etf_f1"):
            dd = d.dropna(subset=[tgt, "cong_innov4", "ret_em", "d_vix"]).copy()
            # country-demean to mimic fixed effects
            for c in [tgt, "cong_innov4", "ret_em", "d_vix"]:
                dd[c] = dd[c] - dd.groupby("country")[c].transform("mean")
            X = sm.add_constant(dd[["cong_innov4", "ret_em", "d_vix"]].values)
            for tau in (0.1, 0.25, 0.5, 0.75, 0.9):
                try:
                    qm = QuantReg(dd[tgt].values, X).fit(q=tau, max_iter=5000)
                    q_rows.append({"sample": lab, "target": tgt, "tau": tau, "n": int(len(dd)),
                                   "beta": qm.params[1], "t": qm.tvalues[1], "p": qm.pvalues[1]})
                except Exception:
                    pass
    qdf = pd.DataFrame(q_rows)
    qdf.to_csv(os.path.join(R, "vol_quantile.csv"), index=False)

    # ---------------- D. monthly RV
    mrows = []
    for name, series in (("idx", "index"), ("etf", "etf_usd"), ("fx", "fx")):
        lrv = monthly_rv(wide(series))
        for c in lrv.columns:
            if c in MAIN:
                s = lrv[c].to_frame(f"mlrv_{name}"); s["country"] = c
                mrows.append(s.reset_index())
    mrv = None
    for name in ("idx", "etf", "fx"):
        parts = [r for r in mrows if f"mlrv_{name}" in r.columns]
        if not parts:
            continue
        part = pd.concat(parts)
        mrv = part if mrv is None else mrv.merge(part, on=["date", "country"], how="outer")
    m = M[M.country.isin(MAIN)].merge(mrv, on=["date", "country"], how="left")
    S2 = S[["date", "country", "surprise_vs_AR"]].copy(); S2["date"] = S2["date"] + pd.offsets.MonthEnd(0)
    m = m.merge(S2, on=["date", "country"], how="left").sort_values(["country", "date"])
    vix_m = np.log(glob["vix"]).resample("ME").last().rename("log_vix_m")
    m = m.merge(vix_m, left_on="date", right_index=True, how="left")
    m = z_within(m, ["cong_slope", "cong_m_innov", "d_cong_m", "surprise_vs_AR"])
    mo = []
    for name in ("idx", "etf", "fx"):
        col = f"mlrv_{name}"
        if col not in m:
            continue
        m[f"{col}_f1"] = m.groupby("country")[col].shift(-1)
        for lab, d in samples(m):
            for s in ("cong_slope", "cong_m_innov", "d_cong_m", "surprise_vs_AR"):
                dd = d.dropna(subset=[f"{col}_f1", s, col, "log_vix_m"])
                if len(dd) < 40:
                    continue
                X = pd.concat([dd[[s, col, "log_vix_m"]], pd.get_dummies(dd["country"]).astype(float)], axis=1)
                mod = sm.OLS(dd[f"{col}_f1"].values, X.values).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
                mo.append({"sample": lab, "target": f"{col}_f1", "signal": s, "n": int(len(dd)),
                           "beta": mod.params[0], "t_NW": mod.tvalues[0], "p": mod.pvalues[0]})
    modf = pd.DataFrame(mo)
    modf.to_csv(os.path.join(R, "vol_monthly.csv"), index=False)

    pd.set_option("display.width", 220)
    print("=== A. Next-week / next-4-week log realized variance on congestion signals (HAR + VIX baseline, FE, week-clustered) ===")
    print(vol.pivot_table(index=["target", "signal"], columns="sample", values=["beta", "t"]).round(3).to_string())
    print("\n=== B. State dependence: beta in low-VIX state, interaction with high-VIX, implied high-state beta ===")
    print(state_df.round(3).to_string(index=False))
    print("\n=== C. Quantile regressions of next-week return on cong_innov4 ===")
    print(qdf.pivot_table(index=["target", "tau"], columns="sample", values=["beta", "t"]).round(3).to_string())
    print("\n=== D. Monthly: next-month log RV on congestion signals ===")
    print(modf.pivot_table(index=["target", "signal"], columns="sample", values=["beta", "t_NW"]).round(3).to_string())


if __name__ == "__main__":
    main()
