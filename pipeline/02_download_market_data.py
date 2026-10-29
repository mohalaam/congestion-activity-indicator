"""
Step 02: download daily equity indices, sector proxies, FX and global controls (free sources
via yfinance) for the study countries, 2019-01-01 to today.

Outputs: data_proc/market_daily.csv   (long format: date, country, series, value)
         data_proc/market_coverage.json
Run:  py -I pipeline/02_download_market_data.py
Note: sector indices for small markets are not all on Yahoo; missing ones are listed in the
coverage file so they can be fetched manually from investing.com / exchange websites.
"""
import json
import os
import pandas as pd
import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data_proc")
os.makedirs(OUT, exist_ok=True)
START = "2019-01-01"

# ticker -> (country, series name). Yahoo tickers; sector tickers where available.
TICKERS = {
    # Headline equity indices
    "XU100.IS": ("Turkey", "index"), "XULAS.IS": ("Turkey", "sector_transport"),
    "XBANK.IS": ("Turkey", "sector_banks"), "XELKT.IS": ("Turkey", "sector_electricity"),
    "XGIDA.IS": ("Turkey", "sector_food"), "XTCRT.IS": ("Turkey", "sector_retail"),
    "XUSIN.IS": ("Turkey", "sector_industrials"), "XHOLD.IS": ("Turkey", "sector_holdings"),
    "WIG20.WA": ("Poland", "index"), "WIG.WA": ("Poland", "index_broad"),
    "WIG-BANKI.WA": ("Poland", "sector_banks"), "WIG-PALIWA.WA": ("Poland", "sector_energy"),
    "^BVSP": ("Brazil", "index"),
    "^J203.JO": ("South Africa", "index"), "^J200.JO": ("South Africa", "index_top40"),
    "^NSEI": ("India", "index"), "^CNXAUTO": ("India", "sector_auto"), "^CNXENERGY": ("India", "sector_energy"),
    "^NSEBANK": ("India", "sector_banks"), "^CNXFMCG": ("India", "sector_fmcg"),
    "^TASI.SR": ("Saudi Arabia", "index"),
    "^MXX": ("Mexico", "index"),
    "^JKSE": ("Indonesia", "index"),
    "^SET.BK": ("Thailand", "index"),
    "^CASE30": ("Egypt", "index"),
    "^KLSE": ("Malaysia", "index"),
    "PSEI.PS": ("Philippines", "index"),
    # Secondary panel
    "^IPSA": ("Chile", "index"), "^COLCAP": ("Colombia", "index"), "^SPBLPGPT": ("Peru", "index"),
    "^MERV": ("Argentina", "index"), "^BUX": ("Hungary", "index"), "^BETI": ("Romania", "index"),
    "GD.AT": ("Greece", "index"),
    # FX (USD per local, Yahoo convention is local per USD for most)
    "TRY=X": ("Turkey", "fx"), "PLN=X": ("Poland", "fx"), "BRL=X": ("Brazil", "fx"),
    "ZAR=X": ("South Africa", "fx"), "INR=X": ("India", "fx"), "SAR=X": ("Saudi Arabia", "fx"),
    "MXN=X": ("Mexico", "fx"), "IDR=X": ("Indonesia", "fx"), "THB=X": ("Thailand", "fx"),
    "EGP=X": ("Egypt", "fx"), "MYR=X": ("Malaysia", "fx"), "PHP=X": ("Philippines", "fx"),
    "CLP=X": ("Chile", "fx"), "COP=X": ("Colombia", "fx"), "PEN=X": ("Peru", "fx"),
    "ARS=X": ("Argentina", "fx"), "HUF=X": ("Hungary", "fx"), "RON=X": ("Romania", "fx"),
    # Global controls
    "^VIX": ("GLOBAL", "vix"), "EEM": ("GLOBAL", "msci_em_etf"), "BZ=F": ("GLOBAL", "brent"),
    "DX-Y.NYB": ("GLOBAL", "dxy"), "^TNX": ("GLOBAL", "us10y"), "^GSPC": ("GLOBAL", "sp500"),
    # Country ETFs in USD (liquid, consistent, useful as alternative return measure)
    "TUR": ("Turkey", "etf_usd"), "EPOL": ("Poland", "etf_usd"), "EWZ": ("Brazil", "etf_usd"),
    "EZA": ("South Africa", "etf_usd"), "INDA": ("India", "etf_usd"), "KSA": ("Saudi Arabia", "etf_usd"),
    "EWW": ("Mexico", "etf_usd"), "EIDO": ("Indonesia", "etf_usd"), "THD": ("Thailand", "etf_usd"),
    "EGPT": ("Egypt", "etf_usd"), "EWM": ("Malaysia", "etf_usd"), "EPHE": ("Philippines", "etf_usd"),
    "ECH": ("Chile", "etf_usd"), "GXG": ("Colombia", "etf_usd"), "EPU": ("Peru", "etf_usd"),
    "ARGT": ("Argentina", "etf_usd"), "GREK": ("Greece", "etf_usd"),
}


def main():
    rows, coverage = [], {}
    for tk, (country, series) in TICKERS.items():
        try:
            h = yf.Ticker(tk).history(start=START, auto_adjust=True)
        except Exception as e:  # noqa
            h = pd.DataFrame()
        if h is None or h.empty:
            coverage[tk] = {"country": country, "series": series, "status": "MISSING"}
            continue
        h = h[["Close"]].rename(columns={"Close": "value"})
        h.index = pd.to_datetime(h.index).tz_localize(None).normalize()
        h = h[~h.index.duplicated()]
        coverage[tk] = {"country": country, "series": series, "status": "ok",
                        "start": str(h.index.min().date()), "end": str(h.index.max().date()),
                        "n": int(len(h))}
        for dt_, v in h["value"].items():
            rows.append({"date": dt_, "country": country, "series": series, "ticker": tk, "value": float(v)})
    df = pd.DataFrame(rows).sort_values(["country", "series", "date"])
    df.to_csv(os.path.join(OUT, "market_daily.csv"), index=False)
    json.dump(coverage, open(os.path.join(OUT, "market_coverage.json"), "w"), indent=2)
    miss = [k for k, v in coverage.items() if v["status"] == "MISSING"]
    print(f"{len(df)} rows, {len(coverage)-len(miss)} series ok, {len(miss)} missing: {miss}")


if __name__ == "__main__":
    main()
