"""
Step 04: build the analysis datasets.

A. weekly_panel.csv  (country x week, Friday-ending)
   congestion features: weekly mean of dow-adjusted log congestion (cong), its change (d_cong),
   4-week and 13-week innovations (cong minus trailing mean), weekday-only version,
   market: log return of local index (ret_idx), USD ETF (ret_etf), FX (ret_fx), sectors;
   next-week returns (ret_*_f1) and 4-week-ahead cumulative (ret_*_f4);
   global controls: d_vix, ret_em, ret_brent, d_dxy, d_us10y.
B. monthly_panel.csv (country x month)
   congestion monthly mean + intra-month path features (mean of first/second half, slope),
   ip and retail log-levels, yoy and mom growth; monthly returns and forward returns.
C. daily_for_nowcast.csv: daily country congestion with month id for mixed-frequency models.

Run: py -I pipeline/04_build_features.py
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data_proc")

cd = pd.read_csv(os.path.join(P, "country_daily.csv"), parse_dates=["date"])
mk = pd.read_csv(os.path.join(P, "market_daily.csv"), parse_dates=["date"])
mac_path = os.path.join(P, "macro_monthly.csv")
mac = pd.read_csv(mac_path, parse_dates=["date"]) if os.path.exists(mac_path) else pd.DataFrame()

# ---------- market wide tables ----------
def wide(series):
    w = mk[mk.series == series].pivot_table(index="date", columns="country", values="value")
    return w.sort_index()

idx, etf, fx = wide("index"), wide("etf_usd"), wide("fx")
# drop index series with fewer than 200 obs (the one-day Yahoo failures)
idx = idx.loc[:, idx.count() > 200]
glob = mk[mk.country == "GLOBAL"].pivot_table(index="date", columns="series", values="value").sort_index()
sectors = mk[mk.series.str.startswith("sector_")].copy()

# ---------- A. weekly panel ----------
cw = cd.set_index("date").groupby("country")[["congestion", "log_c", "log_c_dowadj", "log_c_detr"]] \
       .resample("W-FRI").mean()
cw.columns = ["cong_level", "log_c", "cong", "cong_detr"]
cw = cw.reset_index()

def weekly_logret(w):
    return np.log(w.resample("W-FRI").last()).diff()

r_idx, r_etf, r_fx = weekly_logret(idx), weekly_logret(etf), -weekly_logret(fx)  # fx: + = local appreciation
g = pd.DataFrame({
    "d_vix": np.log(glob["vix"]).resample("W-FRI").last().diff(),
    "ret_em": np.log(glob["msci_em_etf"]).resample("W-FRI").last().diff(),
    "ret_brent": np.log(glob["brent"]).resample("W-FRI").last().diff(),
    "d_dxy": np.log(glob["dxy"]).resample("W-FRI").last().diff(),
    "d_us10y": glob["us10y"].resample("W-FRI").last().diff(),
    "ret_sp500": np.log(glob["sp500"]).resample("W-FRI").last().diff(),
})

rows = []
for c, gdf in cw.groupby("country"):
    gdf = gdf.set_index("date").sort_index()
    gdf["d_cong"] = gdf["cong"].diff()
    gdf["cong_innov4"] = gdf["cong"] - gdf["cong"].rolling(4).mean().shift(1)
    gdf["cong_innov13"] = gdf["cong"] - gdf["cong"].rolling(13).mean().shift(1)
    for name, tbl in (("idx", r_idx), ("etf", r_etf), ("fx", r_fx)):
        if c in tbl.columns:
            gdf[f"ret_{name}"] = tbl[c].reindex(gdf.index)
            gdf[f"ret_{name}_f1"] = tbl[c].shift(-1).reindex(gdf.index)
            gdf[f"ret_{name}_f4"] = tbl[c].rolling(4).sum().shift(-4).reindex(gdf.index)
    sec = sectors[sectors.country == c]
    for sname, sdf in sec.groupby("series"):
        s = np.log(sdf.set_index("date")["value"].sort_index().resample("W-FRI").last()).diff()
        gdf[f"ret_{sname}"] = s.reindex(gdf.index)
        gdf[f"ret_{sname}_f1"] = s.shift(-1).reindex(gdf.index)
    gdf = gdf.join(g)
    gdf["country"] = c
    rows.append(gdf.reset_index())
weekly = pd.concat(rows, ignore_index=True)
weekly = weekly[(weekly["date"] >= "2020-01-03")]
weekly.to_csv(os.path.join(P, "weekly_panel.csv"), index=False)

# ---------- B. monthly panel ----------
cm_rows = []
for c, gdf in cd.groupby("country"):
    gdf = gdf.set_index("date").sort_index()
    m = gdf["log_c_dowadj"].resample("ME")
    out = pd.DataFrame({"cong_m": m.mean(), "cong_m_level": gdf["congestion"].resample("ME").mean()})
    # intra-month path: first-half vs second-half mean and linear slope
    def half(s, first=True):
        n = len(s); return s.iloc[: n // 2].mean() if first else s.iloc[n // 2:].mean()
    out["cong_h1"] = m.apply(lambda s: half(s, True))
    out["cong_h2"] = m.apply(lambda s: half(s, False))
    out["cong_slope"] = m.apply(lambda s: np.polyfit(np.arange(len(s)), s.values, 1)[0] if s.notna().sum() > 5 else np.nan)
    out["d_cong_m"] = out["cong_m"].diff()
    out["cong_m_innov"] = out["cong_m"] - out["cong_m"].rolling(3).mean().shift(1)
    for name, tbl in (("idx", idx), ("etf", etf)):
        if c in tbl.columns:
            r = np.log(tbl[c].resample("ME").last()).diff()
            out[f"ret_{name}_m"] = r.reindex(out.index)
            out[f"ret_{name}_m_f1"] = r.shift(-1).reindex(out.index)
            out[f"ret_{name}_m_f3"] = r.rolling(3).sum().shift(-3).reindex(out.index)
    if c in fx.columns:
        r = -np.log(fx[c].resample("ME").last()).diff()
        out["ret_fx_m"], out["ret_fx_m_f1"] = r.reindex(out.index), r.shift(-1).reindex(out.index)
    if not mac.empty:
        for sname in ("ip", "retail"):
            s = mac[(mac.country == c) & (mac.series == sname)].set_index("date")["value"].sort_index()
            if len(s):
                s.index = s.index.to_period("M").to_timestamp("M")
                ls = np.log(s)
                out[f"{sname}_log"] = ls.reindex(out.index)
                out[f"{sname}_mom"] = ls.diff().reindex(out.index)
                out[f"{sname}_yoy"] = ls.diff(12).reindex(out.index)
    out["country"] = c
    cm_rows.append(out.reset_index().rename(columns={"index": "date"}))
monthly = pd.concat(cm_rows, ignore_index=True)
monthly = monthly[monthly["date"] >= "2020-01-31"]
monthly.to_csv(os.path.join(P, "monthly_panel.csv"), index=False)

# ---------- C. daily for mixed-frequency nowcasting ----------
dn = cd[["country", "date", "congestion", "log_c_dowadj", "log_c_detr", "n_cities"]].copy()
dn["month"] = dn["date"].dt.to_period("M").astype(str)
dn["day_of_month"] = dn["date"].dt.day
dn.to_csv(os.path.join(P, "daily_for_nowcast.csv"), index=False)

print("weekly_panel:", weekly.shape, "countries:", weekly.country.nunique())
print("monthly_panel:", monthly.shape, "cols:", [c for c in monthly.columns if c.startswith(('ip_', 'retail_'))])
print("daily_for_nowcast:", dn.shape)
