"""
TomTom Traffic Index live-feed collector.

Fetches the rolling 7-day hourly feed for every city in tomtom_city_ids.txt and appends
new (city, date, hour) rows to data/tomtom_live_hourly.csv, de-duplicated. Run at least once
every 5 days; twice a day is recommended (Windows Task Scheduler, see setup_task.ps1).

Fields per row: city_id, country (ISO3), date, hour (local), updateTime (ms epoch),
trafficIndexLive, trafficIndexHistoric, relTravelTimeLive, relTravelTimeHistoric,
jamsCount, jamsLength (km), jamsDelay (min), collected_at (UTC).

Source: https://www.tomtom.com/traffic-index/api/live-traffic.json?city=<id>
Terms: TomTom Traffic Index content may be used for non-commercial purposes with attribution.
"""
import csv
import os
import sys
import time
import random
import datetime as dt
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
IDS_FILE = os.path.join(HERE, "tomtom_city_ids.txt")
OUT_DIR = os.path.join(HERE, "data")
OUT_FILE = os.path.join(OUT_DIR, "tomtom_live_hourly.csv")
LOG_FILE = os.path.join(OUT_DIR, "collector.log")
URL = "https://www.tomtom.com/traffic-index/api/live-traffic.json?city={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/152.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.tomtom.com/traffic-index/ranking/",
}
FIELDS = ["city_id", "country", "date", "hour", "updateTime", "trafficIndexLive",
          "trafficIndexHistoric", "relTravelTimeLive", "relTravelTimeHistoric",
          "jamsCount", "jamsLength", "jamsDelay", "collected_at"]


def log(msg):
    line = f"{dt.datetime.utcnow().isoformat(timespec='seconds')}Z {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_existing_keys():
    keys = set()
    if not os.path.exists(OUT_FILE):
        return keys
    with open(OUT_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys.add((row["city_id"], row["date"], row["hour"]))
    return keys


def fetch(city_id, session, retries=3):
    for attempt in range(retries):
        try:
            r = session.get(URL.format(city_id), headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (403, 429, 503):
                time.sleep(20 * (attempt + 1))
            else:
                return None
        except requests.RequestException:
            time.sleep(5 * (attempt + 1))
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(IDS_FILE, encoding="utf-8") as f:
        ids = [ln.strip() for ln in f if ln.strip()]
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    if only:
        ids = [i for i in ids if i.split("_")[0] in only]
    existing = load_existing_keys()
    new_rows = []
    failed = []
    now = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    session = requests.Session()
    for n, cid in enumerate(ids, 1):
        j = fetch(cid, session)
        if not j or "data" not in j:
            failed.append(cid)
        else:
            country = cid.split("_")[0]
            for d in j["data"]:
                key = (cid, str(d.get("date")), str(d.get("hour")))
                if key in existing:
                    continue
                existing.add(key)
                new_rows.append({
                    "city_id": cid, "country": country, "date": d.get("date"),
                    "hour": d.get("hour"), "updateTime": d.get("updateTime"),
                    "trafficIndexLive": d.get("trafficIndexLive"),
                    "trafficIndexHistoric": d.get("trafficIndexHistoric"),
                    "relTravelTimeLive": d.get("relTravelTimeLive"),
                    "relTravelTimeHistoric": d.get("relTravelTimeHistoric"),
                    "jamsCount": d.get("jamsCount"), "jamsLength": d.get("jamsLength"),
                    "jamsDelay": d.get("jamsDelay"), "collected_at": now,
                })
        time.sleep(random.uniform(0.4, 1.0))
        if n % 50 == 0:
            log(f"{n}/{len(ids)} cities fetched, {len(new_rows)} new rows so far")
    write_header = not os.path.exists(OUT_FILE)
    with open(OUT_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            w.writeheader()
        w.writerows(new_rows)
    log(f"done: {len(ids)} cities, {len(new_rows)} new rows, {len(failed)} failed"
        + (f" -> {failed[:10]}" if failed else ""))


if __name__ == "__main__":
    main()
