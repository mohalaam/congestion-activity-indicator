"""
Step 03: download monthly macro targets from DBnomics (IMF IFS mirror) for all study countries.

Series tried per country (IMF IFS, monthly):
  AIP_SA_IX  industrial production, SA index   (fallback AIP_IX, then AIPMA_IX manufacturing)
  ARS_IX     retail sales index
Outputs: data_proc/macro_monthly.csv (long: date, country, series, value, source_code)
         data_proc/macro_coverage.json
Run: py -I pipeline/03_download_macro.py
PMI (S&P Global) is not on DBnomics; collect manually from press releases if needed.
"""
import json
import os
import time
import pandas as pd
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data_proc")
os.makedirs(OUT, exist_ok=True)

COUNTRIES = {"Turkey": "TR", "Poland": "PL", "Brazil": "BR", "South Africa": "ZA", "India": "IN",
             "Saudi Arabia": "SA", "Mexico": "MX", "Indonesia": "ID", "Thailand": "TH",
             "Egypt": "EG", "Malaysia": "MY", "Philippines": "PH",
             "Chile": "CL", "Colombia": "CO", "Peru": "PE", "Argentina": "AR",
             "Hungary": "HU", "Romania": "RO", "Greece": "GR"}
TARGETS = {"ip": ["AIP_SA_IX", "AIP_IX", "AIPMA_IX"], "retail": ["ARS_IX"]}
API = "https://api.db.nomics.world/v22/series/IMF/IFS/M.{cc}.{ind}?observations=1&format=json"
# World Bank Global Economic Monitor (monthly, long and consistent): tried first.
ISO3 = {"Turkey": "TUR", "Poland": "POL", "Brazil": "BRA", "South Africa": "ZAF", "India": "IND",
        "Saudi Arabia": "SAU", "Mexico": "MEX", "Indonesia": "IDN", "Thailand": "THA", "Egypt": "EGY",
        "Malaysia": "MYS", "Philippines": "PHL", "Chile": "CHL", "Colombia": "COL", "Peru": "PER",
        "Argentina": "ARG", "Hungary": "HUN", "Romania": "ROU", "Greece": "GRC"}
WB_TARGETS = {"ip": ["IPTOTSAKD", "IPTOTNSKD"], "retail": ["RETSALESSA"]}
WB_API = "https://api.db.nomics.world/v22/series/WB/GEM/M.{ind}.{cc}?observations=1&format=json"


def fetch(cc, ind, s, api=API):
    for attempt in range(3):
        try:
            r = s.get(api.format(cc=cc, ind=ind), timeout=60)
            if r.status_code != 200:
                time.sleep(2); continue
            j = r.json()
            docs = j.get("series", {}).get("docs", [])
            if not docs:
                return None
            d = docs[0]
            per, val = d.get("period"), d.get("value")
            if not per:
                return None
            df = pd.DataFrame({"period": per, "value": val})
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna()
            df["date"] = pd.PeriodIndex(df["period"], freq="M").to_timestamp("M")
            return df[["date", "value"]]
        except Exception:
            time.sleep(2)
    return None


def main():
    s = requests.Session()
    rows, cov = [], {}
    for country, cc in COUNTRIES.items():
        for target, codes in TARGETS.items():
            got = None
            for code in WB_TARGETS[target]:  # World Bank GEM first
                df = fetch(ISO3[country], code, s, api=WB_API)
                if df is not None and (df["date"] >= "2019-01-01").sum() >= 24:
                    got = ("WB_GEM:" + code, df); break
            for code in ([] if got else codes):  # IMF IFS fallback
                df = fetch(cc, code, s)
                if df is not None and (df["date"] >= "2019-01-01").sum() >= 24:
                    got = ("IMF_IFS:" + code, df); break
            if got is None:
                cov[f"{country}:{target}"] = {"status": "MISSING"}
                continue
            code, df = got
            df = df[df["date"] >= "2015-01-01"]
            cov[f"{country}:{target}"] = {"status": "ok", "code": code,
                                          "start": str(df["date"].min().date()),
                                          "end": str(df["date"].max().date()), "n": int(len(df))}
            for dt_, v in zip(df["date"], df["value"]):
                rows.append({"date": dt_, "country": country, "series": target, "value": v, "source_code": code})
            time.sleep(0.3)
    out = pd.DataFrame(rows).sort_values(["country", "series", "date"])
    out.to_csv(os.path.join(OUT, "macro_monthly.csv"), index=False)
    json.dump(cov, open(os.path.join(OUT, "macro_coverage.json"), "w"), indent=2)
    for k, v in cov.items():
        print(k, v)


if __name__ == "__main__":
    main()
