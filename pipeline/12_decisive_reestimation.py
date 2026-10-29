"""
Step 12: decisive re-estimation requested by the review panel.

Specification ladder for  r_{i,t+1} = FE + b1 x_{i,t} + b2 x_{i,t} S_t + b3 S_t + controls + e
with the RAW congestion innovation (no full-sample deseasonalization), S = 1[VIX>25]:
  L1  country x calendar-month FE                                   (headline reference)
  L2  + state x calendar-month FE
  L3  + year FE
  L4  country x year FE instead of year FE
  L5  + moving-holiday dummies (Ramadan weeks, Eid al-Fitr, Eid al-Adha, Diwali, Lunar New
       Year, Easter, Christmas/New Year; week of the holiday and the following week)
  L6  + state-interacted controls (own return, MSCI EM, dVIX, Brent, DXY, US10y, each x S) and
       the log VIX level
  L7  everything: L4 + L5 + L6 + state x month FE
  L8  L7 with x decomposed into the cross-country weekly mean (common) and the country-specific
       residual (idiosyncratic), each interacted with S
  L9  L7 restricted to calendar year 2021 only, and to 2020-07..2020-12 only
Targets: USD ETF next week (headline) and local index next week. Samples: ex-lockdown and
post-2021-07. Week-clustered SEs; Driscoll-Kraay (4 lags) also reported for L7.
Outputs: results/tables/table_decisive.csv and .md
Run: py -I pipeline/12_decisive_reestimation.py
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
RT = os.path.join(ROOT, "results", "tables")
CTRL = {"ret_etf_f1": ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"],
        "ret_idx_f1": ["ret_idx", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]}

MUSLIM = ["Turkey", "Saudi Arabia", "Egypt", "Malaysia", "Indonesia"]
LNY = ["Malaysia", "Indonesia", "Thailand", "Philippines"]
CHRISTIAN = ["Poland", "Brazil", "Mexico", "Philippines", "South Africa"]
HOLIDAYS = {  # date of the holiday (start for Ramadan); dummies cover the holiday week and the next week
    "ramadan_start": {2020: "2020-04-24", 2021: "2021-04-13", 2022: "2022-04-02"},
    "eid_fitr": {2020: "2020-05-24", 2021: "2021-05-13", 2022: "2022-05-02"},
    "eid_adha": {2020: "2020-07-31", 2021: "2021-07-20", 2022: "2022-07-09"},
    "diwali": {2020: "2020-11-14", 2021: "2021-11-04", 2022: "2022-10-24"},
    "lny": {2020: "2020-01-25", 2021: "2021-02-12", 2022: "2022-02-01", 2023: "2023-01-22"},
    "easter": {2020: "2020-04-12", 2021: "2021-04-04", 2022: "2022-04-17"},
    "xmas": {2020: "2020-12-25", 2021: "2021-12-25", 2022: "2022-12-25", 2019: "2019-12-25"},
}


def add_holidays(w):
    w = w.copy()
    wk_end = w["date"]
    def flag(dates, countries, name, weeks_after=1, span_days=0):
        col = np.zeros(len(w))
        for y, dstr in dates.items():
            d0 = pd.Timestamp(dstr); d1 = d0 + pd.Timedelta(days=span_days)
            lo = d0 - pd.Timedelta(days=6)                      # week containing d0 (Friday-ending)
            hi = d1 + pd.Timedelta(days=7 * weeks_after)
            m = (wk_end >= lo) & (wk_end <= hi) & w["country"].isin(countries)
            col[m.values] = 1
        w[name] = col
    flag(HOLIDAYS["ramadan_start"], MUSLIM, "h_ramadan", weeks_after=0, span_days=29)  # whole month
    flag(HOLIDAYS["eid_fitr"], MUSLIM, "h_eid_fitr")
    flag(HOLIDAYS["eid_adha"], MUSLIM, "h_eid_adha")
    flag(HOLIDAYS["diwali"], ["India"], "h_diwali")
    flag(HOLIDAYS["lny"], LNY, "h_lny")
    flag(HOLIDAYS["easter"], CHRISTIAN, "h_easter")
    flag(HOLIDAYS["xmas"], list(w.country.unique()), "h_xmas", weeks_after=1, span_days=7)
    return w, ["h_ramadan", "h_eid_fitr", "h_eid_adha", "h_diwali", "h_lny", "h_easter", "h_xmas"]


def fit(d, tgt, xcols, fe_cols, extra, cluster="week", dk_lags=None):
    """xcols: list of (name, series) regressors of interest reported; fe_cols: columns whose dummies are FE."""
    d = d.dropna(subset=[tgt] + [c for c in extra]).copy()
    X = pd.DataFrame({n: s.loc[d.index] for n, s in xcols}, index=d.index)
    X = pd.concat([X, d[extra]], axis=1)
    for f in fe_cols:
        X = pd.concat([X, pd.get_dummies(d[f], prefix=f).astype(float)], axis=1)
    keep = X.notna().all(axis=1)
    X, d = X[keep], d[keep]
    X = X.loc[:, (X != 0).any(axis=0)]
    y = d[tgt].values
    if dk_lags:
        # Driscoll-Kraay: Newey-West on the cross-sectionally summed moment conditions
        Xv = X.values; m = sm.OLS(y, Xv).fit(); u = m.resid
        dates = pd.factorize(d["date"].values, sort=True)[0]
        T = dates.max() + 1; k = Xv.shape[1]
        H = np.zeros((T, k))
        np.add.at(H, dates, Xv * u[:, None])
        Sm = H.T @ H
        for l in range(1, dk_lags + 1):
            wgt = 1 - l / (dk_lags + 1); G = H[l:].T @ H[:-l]; Sm += wgt * (G + G.T)
        XtXi = np.linalg.pinv(Xv.T @ Xv); V = XtXi @ Sm @ XtXi
        params, se = m.params, np.sqrt(np.diag(V))
        tv = params / se
    else:
        m = sm.OLS(y, X.values).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["date"])[0]})
        params, tv = m.params, m.tvalues
    out = {"n": int(len(d))}
    for i, (n, _) in enumerate(xcols):
        out[f"b_{n}"] = params[i]; out[f"t_{n}"] = tv[i]
    return out


def main():
    w = mt.prep().sort_values(["country", "date"])
    w["year"] = w.date.dt.year.astype(str)
    w["cy"] = w["country"] + "_" + w["year"]
    w["sm"] = "S" + w["S_vix25"].astype(int).astype(str) + "_" + w["moy"].astype(str)
    w, HC = add_holidays(w)
    # common / idiosyncratic decomposition of the raw signal
    w["x_common"] = w.groupby("date")["x_raw"].transform("mean")
    w["x_idio"] = w["x_raw"] - w["x_common"]
    S = {"ex_lockdown": rb.exlock(w), "post_2021-07": w[w.date >= "2021-07-01"]}
    rows, md = [], ["# Decisive re-estimation (raw signal, S = VIX>25, week-clustered t)\n"]

    def run(label, d, tgt, fe, extra, xs=("x_raw",), dk=None):
        xcols = []
        for xn in xs:
            xcols.append((xn, d[xn])); xcols.append((xn + "_x_S", d[xn] * d["S_vix25"]))
        xcols.append(("S", d["S_vix25"]))
        r = fit(d, tgt, xcols, fe, extra, dk_lags=dk)
        return {"spec": label, **r}

    for tgt in ["ret_etf_f1", "ret_idx_f1"]:
        base = CTRL[tgt]
        for lab, d in S.items():
            d = d.copy()
            d["log_vix_lvl"] = np.log(d["vix"])
            sctrl = []
            for c in base:
                d[c + "_S"] = d[c] * d["S_vix25"]; sctrl.append(c + "_S")
            ladder = [
                ("L1 country x month FE", ["cm"], base),
                ("L2 + state x month FE", ["cm", "sm"], base),
                ("L3 + year FE", ["cm", "sm", "year"], base),
                ("L4 country x year FE", ["cm", "sm", "cy"], base),
                ("L5 + holiday dummies", ["cm", "sm", "cy"], base + HC),
                ("L6 + S x controls, log VIX", ["cm", "sm", "cy"], base + HC + sctrl + ["log_vix_lvl"]),
            ]
            res = []
            for label, fe, extra in ladder:
                r = run(label, d, tgt, fe, extra); r.update({"target": tgt, "sample": lab}); res.append(r); rows.append(r)
            # L7 = L6 (everything) with Driscoll-Kraay
            r = run("L7 everything, Driscoll-Kraay(4)", d, tgt, ["cm", "sm", "cy"], base + HC + sctrl + ["log_vix_lvl"], dk=4)
            r.update({"target": tgt, "sample": lab}); res.append(r); rows.append(r)
            # L8 decomposition
            r = run("L8 common vs idiosyncratic (L6 FE)", d, tgt, ["cm", "sm", "cy"], base + HC + sctrl + ["log_vix_lvl"], xs=("x_common", "x_idio"))
            r.update({"target": tgt, "sample": lab}); res.append(r); rows.append(r)
            # L9 sub-periods (country x month FE only; too few obs for cy)
            for sub, dd in [("L9 within 2021 only", d[d.year == "2021"]), ("L9 within 2020H2 only", d[(d.date >= "2020-07-01") & (d.date <= "2020-12-31")]),
                            ("L9 within 2022 only", d[d.year == "2022"])]:
                if dd["S_vix25"].nunique() < 2 or len(dd) < 150:
                    continue
                try:
                    r = run(sub, dd, tgt, ["country"], base + HC); r.update({"target": tgt, "sample": lab}); res.append(r); rows.append(r)
                except Exception:
                    pass
            md.append(f"\n## {tgt}, {lab}\n\n| spec | n | b calm | t | b inter | t | b stress |\n|---|---:|---:|---:|---:|---:|---:|")
            for r in res:
                if "b_x_raw" in r:
                    md.append(f"| {r['spec']} | {r['n']} | {r['b_x_raw']:.3f} | {r['t_x_raw']:.2f} | {r['b_x_raw_x_S']:.3f} | {r['t_x_raw_x_S']:.2f} | {r['b_x_raw'] + r['b_x_raw_x_S']:.3f} |")
                else:
                    md.append(f"| {r['spec']} common | {r['n']} | {r['b_x_common']:.3f} | {r['t_x_common']:.2f} | {r['b_x_common_x_S']:.3f} | {r['t_x_common_x_S']:.2f} | {r['b_x_common'] + r['b_x_common_x_S']:.3f} |")
                    md.append(f"| {r['spec']} idiosyncratic | {r['n']} | {r['b_x_idio']:.3f} | {r['t_x_idio']:.2f} | {r['b_x_idio_x_S']:.3f} | {r['t_x_idio_x_S']:.2f} | {r['b_x_idio'] + r['b_x_idio_x_S']:.3f} |")
    pd.DataFrame(rows).to_csv(os.path.join(RT, "table_decisive.csv"), index=False)
    txt = "\n".join(md)
    open(os.path.join(RT, "table_decisive.md"), "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
