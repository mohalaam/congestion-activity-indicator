"""
Step 09: robustness battery for the main result
  r_{i,t+h} = a_i + b1 * cong_innov4_{i,t} + b2 * cong_innov4_{i,t} x Stress_t + b3 * Stress_t + controls + e
Main spec: USD ETF next-week return, Stress = VIX > 25, ex-lockdown sample. Also local index
and 4-week horizon.

Checks:
 1. Alternative state variables: VIX > 20 / 25 / 30, continuous log VIX (demeaned), MSCI EM
    drawdown > 10% from 26-week high, own-country realized volatility above its median,
    own-country 4-week return below -5% (local stress).
 2. Block bootstrap over time: resample calendar weeks in moving blocks of 8 weeks (all
    countries of a week move together), 1,000 draws; report bootstrap SE, percentile CI and
    the share of draws with a positive interaction. Plus an episode jackknife: identify
    contiguous high-VIX runs and drop each one in turn.
 3. Google Community Mobility (workplaces, transit stations; country level, 2020-02..2022-10)
    as an alternative activity signal in the same regression.
 4. Placebos: (a) shuffle each country's congestion series across weeks (500 draws) and
    record the interaction t; (b) use congestion shifted by 52 weeks as a pseudo-signal.

Outputs: results/rob_states.csv, rob_bootstrap.csv, rob_jackknife.csv, rob_google.csv,
         rob_placebo.csv, rob_summary.txt
Run: py -I pipeline/09_robustness.py
"""
import os
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
rng = np.random.default_rng(20261028)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data_proc")
R = os.path.join(ROOT, "results")
RAW = os.path.join(ROOT, "data_raw")

mk = pd.read_csv(os.path.join(P, "market_daily.csv"), parse_dates=["date"])
W = pd.read_csv(os.path.join(P, "weekly_panel.csv"), parse_dates=["date"])
MAIN = ["Turkey", "Poland", "Brazil", "South Africa", "India", "Saudi Arabia", "Mexico",
        "Indonesia", "Thailand", "Egypt", "Malaysia", "Philippines"]
ISO2 = {"Turkey": "TR", "Poland": "PL", "Brazil": "BR", "South Africa": "ZA", "India": "IN",
        "Saudi Arabia": "SA", "Mexico": "MX", "Indonesia": "ID", "Thailand": "TH", "Egypt": "EG",
        "Malaysia": "MY", "Philippines": "PH"}
LOCK = (pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-30"))
CTRL = {"ret_etf_f1": ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"],
        "ret_idx_f1": ["ret_idx", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"],
        "ret_etf_f4": ["ret_etf", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"],
        "ret_fx_f4": ["ret_fx", "ret_em", "d_vix", "ret_brent", "d_dxy", "d_us10y"]}


def z_within(df, cols):
    out = df.copy()
    for c in cols:
        if c in out:
            out[c] = out.groupby("country")[c].transform(lambda s: (s - s.mean()) / s.std())
    return out


def build_panel():
    glob = mk[mk.country == "GLOBAL"].pivot_table(index="date", columns="series", values="value").sort_index()
    vix = glob["vix"].resample("W-FRI").last().rename("vix")
    eem = glob["msci_em_etf"].resample("W-FRI").last()
    dd = (eem / eem.rolling(26).max() - 1).rename("em_drawdown")
    w = W[W.country.isin(MAIN)].copy()
    w = w.merge(vix, left_on="date", right_index=True, how="left").merge(dd, left_on="date", right_index=True, how="left")
    # own realized vol (weekly, from daily ETF prices)
    etf = mk[mk.series == "etf_usd"].pivot_table(index="date", columns="country", values="value").sort_index()
    lrv = np.log((np.log(etf).diff() ** 2).resample("W-FRI").sum(min_count=3).replace(0, np.nan))
    lrv = lrv.stack().rename("lrv").reset_index().rename(columns={"level_1": "country"})
    w = w.merge(lrv, on=["date", "country"], how="left").sort_values(["country", "date"])
    w["own_ret4"] = w.groupby("country")["ret_etf"].transform(lambda s: s.rolling(4).sum())
    w["log_vix_dm"] = np.log(w["vix"]) - np.log(w["vix"]).mean()
    w["S_vix20"] = (w["vix"] > 20).astype(float)
    w["S_vix25"] = (w["vix"] > 25).astype(float)
    w["S_vix30"] = (w["vix"] > 30).astype(float)
    w["S_emdd10"] = (w["em_drawdown"] < -0.10).astype(float)
    w["S_ownvol"] = (w["lrv"] > w.groupby("country")["lrv"].transform("median")).astype(float)
    w["S_ownret"] = (w["own_ret4"] < -0.05).astype(float)
    w = z_within(w, ["cong_innov4", "ret_etf_f1", "ret_idx_f1", "ret_etf_f4", "ret_fx_f4"])
    return w


def interaction_reg(d, tgt, state, signal="cong_innov4", cluster=True):
    d = d.copy()
    d["sx"] = d[signal] * d[state]
    cols = [tgt, signal, "sx", state] + CTRL[tgt]
    d = d.dropna(subset=cols)
    if len(d) < 80 or d.country.nunique() < 3:
        return None
    X = pd.concat([d[[signal, "sx", state] + CTRL[tgt]], pd.get_dummies(d["country"]).astype(float)], axis=1)
    if cluster:
        m = sm.OLS(d[tgt].values, X.values).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["date"])[0]})
    else:
        m = sm.OLS(d[tgt].values, X.values).fit()
    return {"n": int(len(d)), "b_calm": m.params[0], "t_calm": m.tvalues[0],
            "b_inter": m.params[1], "t_inter": m.tvalues[1], "b_stress": m.params[0] + m.params[1],
            "share_stress": float(d[state].mean())}


def exlock(d):
    return d[(d.date < LOCK[0]) | (d.date > LOCK[1])]


def main():
    w = build_panel()
    base = exlock(w)
    lines = []

    # ---------------- 1. alternative states
    rows = []
    for state in ["S_vix20", "S_vix25", "S_vix30", "log_vix_dm", "S_emdd10", "S_ownvol", "S_ownret"]:
        for tgt in ["ret_etf_f1", "ret_idx_f1", "ret_etf_f4", "ret_fx_f4"]:
            for lab, d in [("ex_lockdown", base), ("post_2021-07", w[w.date >= "2021-07-01"])]:
                r = interaction_reg(d, tgt, state)
                if r:
                    rows.append({"sample": lab, "state": state, "target": tgt, **r})
    st = pd.DataFrame(rows)
    st.to_csv(os.path.join(R, "rob_states.csv"), index=False)

    # ---------------- 2. block bootstrap + episode jackknife (main spec)
    tgt, state = "ret_etf_f1", "S_vix25"
    d0 = base.dropna(subset=[tgt, "cong_innov4", state] + CTRL[tgt]).copy()
    weeks = np.array(sorted(d0.date.unique()))
    nW, B, L = len(weeks), 1000, 8
    point = interaction_reg(d0, tgt, state)
    boots = []
    byweek = {t: g for t, g in d0.groupby("date")}
    for b in range(B):
        starts = rng.integers(0, nW - L + 1, size=int(np.ceil(nW / L)))
        sel = np.concatenate([weeks[s:s + L] for s in starts])[:nW]
        db = pd.concat([byweek[t] for t in sel])
        r = interaction_reg(db, tgt, state, cluster=False)
        if r:
            boots.append(r["b_inter"])
    boots = np.array(boots)
    bs = {"spec": f"{tgt} x {state}, ex-lockdown", "point_b_inter": point["b_inter"], "cluster_t": point["t_inter"],
          "boot_se": boots.std(), "boot_t": point["b_inter"] / boots.std(),
          "ci_2.5": np.percentile(boots, 2.5), "ci_97.5": np.percentile(boots, 97.5),
          "share_positive": float((boots > 0).mean()), "B": int(len(boots)), "block_len": L}
    pd.DataFrame([bs]).to_csv(os.path.join(R, "rob_bootstrap.csv"), index=False)

    # episodes: contiguous runs of high-VIX weeks (allow 1-week gaps)
    sv = d0.groupby("date")[state].first().sort_index()
    ep, cur, last = [], [], None
    for t, v in sv.items():
        if v == 1:
            if cur and (t - last).days > 14:
                ep.append(cur); cur = []
            cur.append(t); last = t
    if cur:
        ep.append(cur)
    jk = []
    for i, e in enumerate(ep):
        dj = d0[~d0.date.isin(e)]
        r = interaction_reg(dj, tgt, state)
        if r:
            jk.append({"dropped_episode": f"{e[0].date()}..{e[-1].date()} ({len(e)} wks)", **r})
    jk = pd.DataFrame(jk)
    jk.to_csv(os.path.join(R, "rob_jackknife.csv"), index=False)

    # ---------------- 3. Google mobility
    gm_rows = []
    gpath = os.path.join(RAW, "Global_Mobility_Report.csv")
    if os.path.exists(gpath) and os.path.getsize(gpath) > 1e6:
        keep = []
        for ch in pd.read_csv(gpath, chunksize=500_000, usecols=["country_region_code", "sub_region_1", "date",
                              "workplaces_percent_change_from_baseline", "transit_stations_percent_change_from_baseline",
                              "retail_and_recreation_percent_change_from_baseline"], low_memory=False):
            ch = ch[ch.country_region_code.isin(ISO2.values()) & ch.sub_region_1.isna()]
            keep.append(ch)
        g = pd.concat(keep)
        g["date"] = pd.to_datetime(g["date"])
        inv = {v: k for k, v in ISO2.items()}
        g["country"] = g.country_region_code.map(inv)
        g = g.rename(columns={"workplaces_percent_change_from_baseline": "gm_work",
                              "transit_stations_percent_change_from_baseline": "gm_transit",
                              "retail_and_recreation_percent_change_from_baseline": "gm_retail"})
        g.to_csv(os.path.join(P, "google_mobility_daily.csv"), index=False)
        gw = g.set_index("date").groupby("country")[["gm_work", "gm_transit", "gm_retail"]].resample("W-FRI").mean().reset_index()
        for c in ["gm_work", "gm_transit", "gm_retail"]:
            gw[f"{c}_innov4"] = gw.groupby("country")[c].transform(lambda s: s - s.rolling(4).mean().shift(1))
        wg = w.merge(gw, on=["date", "country"], how="inner")
        wg = z_within(wg, [f"{c}_innov4" for c in ["gm_work", "gm_transit", "gm_retail"]])
        for sig in ["gm_work_innov4", "gm_transit_innov4", "gm_retail_innov4", "cong_innov4"]:
            for tg in ["ret_etf_f1", "ret_idx_f1", "ret_fx_f4"]:
                for lab, d in [("google_window_all", wg), ("google_window_exlock", exlock(wg))]:
                    r = interaction_reg(d, tg, "S_vix25", signal=sig)
                    if r:
                        gm_rows.append({"sample": lab, "signal": sig, "target": tg, **r})
        # correlation between the two activity measures
        corr = wg[["cong_innov4", "gm_work_innov4", "gm_transit_innov4"]].corr().round(3)
        lines.append("Google vs TomTom weekly innovation correlations:\n" + corr.to_string())
    gm = pd.DataFrame(gm_rows)
    gm.to_csv(os.path.join(R, "rob_google.csv"), index=False)

    # ---------------- 4. placebos
    pl = []
    # (a) within-country shuffle of the congestion series
    tstats = []
    for k in range(500):
        dp = d0.copy()
        dp["cong_innov4"] = dp.groupby("country")["cong_innov4"].transform(lambda s: s.sample(frac=1, random_state=int(rng.integers(1e9))).values)
        r = interaction_reg(dp, tgt, state, cluster=False)
        if r:
            tstats.append(r["t_inter"])
    tstats = np.array(tstats)
    pl.append({"placebo": "shuffle congestion within country (500 draws)",
               "actual_t_inter_noncluster": interaction_reg(d0, tgt, state, cluster=False)["t_inter"],
               "placebo_mean_t": tstats.mean(), "placebo_sd_t": tstats.std(),
               "share_placebo_t_ge_actual": float((tstats >= interaction_reg(d0, tgt, state, cluster=False)["t_inter"]).mean())})
    # (b) congestion shifted by 52 weeks
    ds = w.copy()
    ds["cong_innov4"] = ds.groupby("country")["cong_innov4"].shift(52)
    r = interaction_reg(exlock(ds), tgt, state)
    if r:
        pl.append({"placebo": "congestion lagged 52 weeks (pseudo-signal)", **r})
    pl = pd.DataFrame(pl)
    pl.to_csv(os.path.join(R, "rob_placebo.csv"), index=False)

    # ---------------- summary
    pd.set_option("display.width", 220)
    s = []
    s.append("=== 1. Alternative state variables (interaction coefficient and clustered t) ===")
    s.append(st.pivot_table(index=["state", "target"], columns="sample", values=["b_calm", "t_calm", "b_inter", "t_inter"]).round(3).to_string())
    s.append("\n=== 2. Moving-block bootstrap (8-week blocks, 1000 draws) for ETF 1-week x VIX>25, ex-lockdown ===")
    s.append(pd.DataFrame([bs]).round(4).to_string(index=False))
    s.append("\n=== 2b. Episode jackknife (drop each high-VIX episode) ===")
    s.append(jk.round(3).to_string(index=False))
    s.append("\n=== 3. Google mobility as alternative activity signal (VIX>25 state) ===")
    s.append(gm.round(3).to_string(index=False) if len(gm) else "Google mobility file not available")
    s.append("\n=== 4. Placebos ===")
    s.append(pl.round(3).to_string(index=False))
    s.extend(lines)
    txt = "\n".join(s)
    open(os.path.join(R, "rob_summary.txt"), "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
