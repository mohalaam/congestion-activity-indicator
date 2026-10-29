# A seasonal placebo for mobility-based return predictability: urban congestion in twelve emerging markets

Code, derived data, results and the pre-registration for the paper of the same title.
Manuscript draft: `paper/MANUSCRIPT_v4.md`. Pre-registration: `paper/PREREGISTRATION.md`.

## What is here

| Folder | Contents |
|---|---|
| `pipeline/` | Numbered scripts 01-20 that build the panels, run every estimate and produce every table and figure |
| `collector/` | Live-feed collector for the TomTom per-city feed (490 city ids) and a Windows scheduler script |
| `data/` | Derived country-week and country-month panels (no raw provider values; see DATA_NOTICE.md) |
| `results/tables`, `results/figures` | Every table and figure in the paper, plus working notes in `results/*.md` |
| `paper/` | Manuscript, pre-registration, and the assembly scripts |

## Rebuilding from scratch

1. Install Python 3.11 and `pip install -r requirements.txt`.
2. Download the archived daily TomTom file (see DATA_NOTICE.md) to `data_raw/tomtom_trafic_index.csv`.
   Optional: Google `Global_Mobility_Report.csv` and the OxCGRT compact national CSV to `data_raw/`.
3. Run, in order: `01_build_congestion_panel.py`, `02_download_market_data.py`, `03_download_macro.py`,
   `04_build_features.py`. These recreate `data_proc/` (the committed `data/` folder is the
   derived subset of it).
4. Estimation and tables: `05_nowcast_benchmarks.py` (run twice, the second time with
   `EXCL_LOCK=1`), `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`.
   Scripts 06 was not used. Each script states its outputs in its header docstring.
5. Manuscript assembly: `paper/assemble_v4.py`, then `patch_v4_consistency.py`, then `patch_v4_refs.py`.

Running everything takes about an hour on a laptop; the bootstraps and placebos in 09, 14,
17 and 18 are the slow parts. Seeds are fixed inside the scripts.

## Live collector

`collector/collect_tomtom_live.py` fetches the public seven-day hourly feed for each city id in
`tomtom_city_ids.txt` and appends de-duplicated rows to `collector/data/tomtom_live_hourly.csv`.
Run it at least every five days; `setup_task.ps1` registers a twice-daily Windows task. The
collected data are not committed. The pre-registered test in `paper/PREREGISTRATION.md`
specifies how they will be used.

## Publishing this repository

```bash
git remote add origin https://github.com/<your-account>/congestion-activity-indicator.git
git push -u origin main
```

## Licence

Code: MIT (see LICENSE). Data: see DATA_NOTICE.md.
