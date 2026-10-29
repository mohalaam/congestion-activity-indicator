"""
Step 05: econometric nowcasting benchmarks for monthly industrial production growth from
daily congestion, with a rolling (expanding-window) pseudo real-time evaluation.

Target: ip_mom(t) = log IP(t) - log IP(t-1)  (seasonally adjusted IP, WB GEM / IMF IFS)

Information set at the nowcast origin (end of month t): all daily congestion through the last
day of month t; IP known through t-1 (optimistic for the AR benchmark: official releases come
4-8 weeks after month end, so this understates our advantage).

Models (all estimated by OLS unless stated):
  AR      : ip_mom(t) ~ ip_mom(t-1)
  BRIDGE  : ip_mom(t) ~ ip_mom(t-1) + d_cong_m(t)                 [monthly mean congestion change]
  BRIDGE2 : ip_mom(t) ~ ip_mom(t-1) + d_cong_m(t) + d_cong_m(t-1)
  UMIDAS  : ip_mom(t) ~ ip_mom(t-1) + weekly means of daily congestion in month t (4 lags)
            + monthly mean of month t-1                             [unrestricted MIDAS]
  AMIDAS  : ip_mom(t) ~ ip_mom(t-1) + sum_k w_k(theta) x(day t-k), k=0..59, exponential
            Almon weights (2 params), nonlinear least squares     [restricted MIDAS]
  POOLED-BRIDGE / POOLED-UMIDAS : same as above but coefficients pooled across countries with
            country fixed effects (helps with 20-30 training months per country).
Also a mid-month variant (BRIDGE_H1) using only the first 15 days of month t, to show the
timeliness value.

Evaluation: first OOS nowcast 2021-01 (training from the first month with data, ~2020-02),
expanding window, last OOS month = last month with full daily data (2023-01).
Metrics: RMSE, RMSE relative to AR, Diebold-Mariano test vs AR (squared loss, HAC, h=1),
pooled and per country. Also an "ex-COVID" evaluation restricted to 2021-07 onward.

Outputs: results/nowcast_benchmarks_summary.csv, results/nowcast_benchmarks_bycountry.csv,
         data_proc/nowcast_surprises.csv (model nowcast, realized, surprise, per country-month)
Run: py -I pipeline/05_nowcast_benchmarks.py
"""
import os
import json
import warnings
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy import stats

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data_proc")
R = os.path.join(ROOT, "results")
os.makedirs(R, exist_ok=True)

daily = pd.read_csv(os.path.join(P, "daily_for_nowcast.csv"), parse_dates=["date"])
monthly = pd.read_csv(os.path.join(P, "monthly_panel.csv"), parse_dates=["date"])
FIRST_OOS = pd.Timestamp("2021-01-31")
EXCOVID = pd.Timestamp("2021-07-31")
NLAGS_DAILY = 60
EXCLUDE_LOCKDOWN = os.environ.get("EXCL_LOCK","0")=="1"   # drop 2020-03..2020-06 from training
LOCK_LO, LOCK_HI = pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-30")


# ---------------------------------------------------------------- feature construction
def build_country(c):
    d = daily[daily.country == c].set_index("date").sort_index()["log_c_dowadj"]
    d = d.interpolate(limit=5)
    m = monthly[monthly.country == c].set_index("date").sort_index()
    if "ip_mom" not in m or m["ip_mom"].notna().sum() < 20:
        return None
    rows = []
    for t in m.index:
        if pd.isna(m.loc[t, "ip_mom"]):
            continue
        ms = t - pd.offsets.MonthBegin(1)  # first day of month t
        win = d[(d.index >= ms) & (d.index <= t)]
        if len(win) < 20:
            continue
        prev = d[(d.index >= ms - pd.offsets.MonthBegin(1)) & (d.index < ms)]
        # weekly means within month t (4 blocks of ~7-8 days)
        blocks = np.array_split(win.values, 4)
        wk = [np.nanmean(b) for b in blocks]
        h1 = np.nanmean(win.values[:15])
        # daily lag vector for Almon MIDAS: last 60 days ending at t
        lagv = d[d.index <= t].tail(NLAGS_DAILY).values
        if len(lagv) < NLAGS_DAILY:
            lagv = np.concatenate([np.full(NLAGS_DAILY - len(lagv), np.nan), lagv])
        rows.append({
            "date": t, "country": c, "y": m.loc[t, "ip_mom"],
            "y_lag": m["ip_mom"].shift(1).loc[t],
            "cong_m": np.nanmean(win.values), "cong_prev": np.nanmean(prev.values) if len(prev) else np.nan,
            "cong_h1": h1, "wk1": wk[0], "wk2": wk[1], "wk3": wk[2], "wk4": wk[3],
            "lags": lagv,
        })
    f = pd.DataFrame(rows).set_index("date")
    f["d_cong_m"] = f["cong_m"] - f["cong_prev"]
    f["d_cong_m_lag"] = f["d_cong_m"].shift(1)
    f["d_cong_h1"] = f["cong_h1"] - f["cong_prev"]
    return f.dropna(subset=["y", "y_lag", "d_cong_m"])


# ---------------------------------------------------------------- estimators
def ols_fit_predict(Xtr, ytr, Xte):
    Xtr1 = np.column_stack([np.ones(len(Xtr)), Xtr])
    beta, *_ = np.linalg.lstsq(Xtr1, ytr, rcond=None)
    return np.concatenate([[1.0], np.atleast_1d(Xte)]) @ beta


def almon_weights(theta, K):
    k = np.arange(K, dtype=float)
    w = np.exp(theta[0] * k + theta[1] * k ** 2)
    return w / w.sum()


def amidas_fit_predict(ylag_tr, L_tr, ytr, ylag_te, L_te):
    """y = a + b*ylag + c * sum_k w_k(theta) L[:,k]  (L[:,0] = most recent day)."""
    K = L_tr.shape[1]
    L_tr = np.where(np.isnan(L_tr), np.nanmean(L_tr), L_tr)
    L_te = np.where(np.isnan(L_te), np.nanmean(L_tr), L_te)

    def resid(p):
        a, b, c, t1, t2 = p
        w = almon_weights([t1, t2], K)
        return ytr - (a + b * ylag_tr + c * (L_tr @ w))
    best = None
    for t1, t2 in [(-0.05, 0.0), (0.0, -0.001), (-0.1, 0.0), (0.05, -0.002)]:
        p0 = [ytr.mean(), 0.2, 0.0, t1, t2]
        try:
            sol = least_squares(resid, p0, bounds=([-np.inf, -np.inf, -np.inf, -1, -0.05], [np.inf, np.inf, np.inf, 1, 0.05]))
            if best is None or sol.cost < best.cost:
                best = sol
        except Exception:
            continue
    a, b, c, t1, t2 = best.x
    return a + b * ylag_te + c * (L_te @ almon_weights([t1, t2], K))


def dm_test(e1, e2, h=1):
    """Diebold-Mariano, squared loss, loss differential d = e1^2 - e2^2 (model 1 = benchmark).
    Positive stat => model 2 better. HAC variance with h-1 lags; small-sample Harvey correction."""
    d = e1 ** 2 - e2 ** 2
    d = d[~np.isnan(d)]
    n = len(d)
    if n < 8:
        return np.nan, np.nan
    mean = d.mean()
    gamma0 = ((d - mean) ** 2).mean()
    var = gamma0
    for k in range(1, h):
        gk = ((d[k:] - mean) * (d[:-k] - mean)).mean()
        var += 2 * gk
    if var <= 0:
        return np.nan, np.nan
    dm = mean / np.sqrt(var / n)
    dm *= np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    p = 2 * (1 - stats.t.cdf(abs(dm), df=n - 1))
    return dm, p


# ---------------------------------------------------------------- rolling evaluation
MODELS = ["AR", "BRIDGE", "BRIDGE_H1", "BRIDGE2", "UMIDAS", "AMIDAS", "POOL_BRIDGE", "POOL_UMIDAS"]


def spec(f, model):
    if model == "AR":
        return ["y_lag"]
    if model == "BRIDGE":
        return ["y_lag", "d_cong_m"]
    if model == "BRIDGE_H1":
        return ["y_lag", "d_cong_h1"]
    if model == "BRIDGE2":
        return ["y_lag", "d_cong_m", "d_cong_m_lag"]
    if model == "UMIDAS":
        return ["y_lag", "wk1", "wk2", "wk3", "wk4", "cong_prev"]
    raise ValueError


def main():
    feats = {}
    for c in sorted(monthly.country.unique()):
        f = build_country(c)
        if f is not None and len(f) >= 24:
            feats[c] = f
    print("countries with IP and daily data:", list(feats))
    allf = pd.concat([f.assign(country=c) for c, f in feats.items()])
    oos_months = sorted(set(allf.index[allf.index >= FIRST_OOS]))
    preds = []
    for t in oos_months:
        # pooled training set: all countries, months < t
        pool_tr = allf[allf.index < t]
        if EXCLUDE_LOCKDOWN:
            pool_tr = pool_tr[(pool_tr.index < LOCK_LO) | (pool_tr.index > LOCK_HI)]
        pool_tr = pool_tr.dropna(subset=["y", "y_lag", "d_cong_m", "wk1", "wk2", "wk3", "wk4", "cong_prev"])
        for c, f in feats.items():
            if t not in f.index:
                continue
            tr = f[f.index < t]
            if EXCLUDE_LOCKDOWN:
                tr = tr[(tr.index < LOCK_LO) | (tr.index > LOCK_HI)]
            te = f.loc[t]
            if len(tr) < 10:
                continue
            row = {"date": t, "country": c, "y": te["y"]}
            for model in MODELS:
                try:
                    if model in ("AR", "BRIDGE", "BRIDGE_H1", "BRIDGE2", "UMIDAS"):
                        cols = spec(f, model)
                        trc = tr.dropna(subset=cols)
                        if len(trc) < len(cols) + 6 or te[cols].isna().any():
                            row[model] = np.nan; continue
                        row[model] = ols_fit_predict(trc[cols].values.astype(float), trc["y"].values.astype(float),
                                                     te[cols].values.astype(float))
                    elif model == "AMIDAS":
                        L_tr = np.vstack(tr["lags"].values)[:, ::-1]
                        L_te = np.asarray(te["lags"])[::-1]
                        row[model] = amidas_fit_predict(tr["y_lag"].values.astype(float), L_tr,
                                                        tr["y"].values.astype(float), float(te["y_lag"]), L_te)
                    elif model.startswith("POOL_"):
                        cols = spec(f, model.replace("POOL_", ""))
                        X = pool_tr[cols].values.astype(float)
                        D = pd.get_dummies(pool_tr["country"]).values.astype(float)
                        Xd = np.column_stack([X, D])
                        beta, *_ = np.linalg.lstsq(Xd, pool_tr["y"].values.astype(float), rcond=None)
                        dvec = (pd.get_dummies(pool_tr["country"]).columns == c).astype(float)
                        row[model] = np.concatenate([te[cols].values.astype(float), dvec]) @ beta
                except Exception:
                    row[model] = np.nan
            preds.append(row)
    pr = pd.DataFrame(preds).sort_values(["country", "date"])
    pr.to_csv(os.path.join(R, "nowcast_predictions" + ("_exlock" if EXCLUDE_LOCKDOWN else "") + ".csv"), index=False)

    # ---------------- metrics
    def summarize(sub, label):
        out = []
        for model in MODELS:
            e = sub["y"] - sub[model]
            e_ar = sub["y"] - sub["AR"]
            m = e.notna() & e_ar.notna()
            if m.sum() < 8:
                continue
            rmse = np.sqrt((e[m] ** 2).mean()); rmse_ar = np.sqrt((e_ar[m] ** 2).mean())
            dm, p = dm_test(e_ar[m].values, e[m].values)
            out.append({"sample": label, "model": model, "n": int(m.sum()), "rmse": rmse,
                        "rel_rmse_vs_AR": rmse / rmse_ar, "DM_stat": dm, "DM_p": p,
                        "mae": e[m].abs().mean(),
                        "dir_acc": float(((np.sign(sub.loc[m, "y"]) == np.sign(sub.loc[m, model]))).mean())})
        return pd.DataFrame(out)

    summ = pd.concat([summarize(pr, "full_OOS_2021-01+"),
                      summarize(pr[pr.date >= EXCOVID], "exCOVID_2021-07+")], ignore_index=True)
    tag = "_exlock" if EXCLUDE_LOCKDOWN else ""
    summ.to_csv(os.path.join(R, f"nowcast_benchmarks_summary{tag}.csv"), index=False)
    byc = pd.concat([summarize(g, c).assign(country=c) for c, g in pr.groupby("country")], ignore_index=True)
    byc.to_csv(os.path.join(R, f"nowcast_benchmarks_bycountry{tag}.csv"), index=False)

    # ---------------- surprises for the return tests (best congestion model by pooled RMSE)
    cong_models = [m for m in MODELS if m != "AR"]
    best = summ[(summ["sample"].str.startswith("full")) & (summ.model.isin(cong_models))].sort_values("rmse").iloc[0]["model"]
    sp = pr[["date", "country", "y", "AR", best]].rename(columns={best: "nowcast_cong"})
    sp["surprise_vs_AR"] = sp["nowcast_cong"] - sp["AR"]          # information added by congestion
    sp["realized_minus_nowcast"] = sp["y"] - sp["nowcast_cong"]   # ex-post nowcast error
    sp["best_model"] = best
    sp.to_csv(os.path.join(P, "nowcast_surprises.csv"), index=False)

    pd.set_option("display.width", 200)
    print("\n=== Pooled out-of-sample results (IP m/m growth) ===")
    print(summ.round(4).to_string(index=False))
    print("\n=== Relative RMSE vs AR by country (full OOS) ===")
    piv = byc.pivot_table(index="country", columns="model", values="rel_rmse_vs_AR")
    print(piv[[m for m in MODELS if m in piv.columns]].round(3).to_string())
    print("\nbest congestion model:", best, "| surprises saved to data_proc/nowcast_surprises.csv")
    json.dump({"countries": list(feats), "oos_months": [str(t.date()) for t in oos_months],
               "best_model": best}, open(os.path.join(R, "nowcast_benchmarks_meta.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
