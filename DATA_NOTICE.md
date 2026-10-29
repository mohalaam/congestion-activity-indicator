# Data notice

The files under `data/` are derived aggregates produced by the code in this repository. They
contain standardized weekly and monthly congestion innovations at the country level, market
returns computed from public price series, state indicators, holiday dummies, stringency
changes and macro series. They do not contain the provider's daily congestion values.

Sources and terms:

- TomTom Traffic Index (TomTom International BV). Daily city values for 2019-12-30 to
  2023-02-14 were obtained from the public archive maintained by the ActiveConclusion
  COVID19_mobility project on GitHub (file tomtom_reports/tomtom_trafic_index.csv), which
  preserved values displayed on TomTom's public city pages. TomTom permits non-commercial use
  of Traffic Index content with attribution. The raw values are not redistributed here; to
  rebuild the panels, download that file into `data_raw/` and run `pipeline/01_...`.
- TomTom live feed (collector/). Hourly values collected from the public per-city feed since
  2026-10-21 are not redistributed. The collector is provided so the collection can be
  reproduced; users are responsible for complying with the provider's terms.
- Google LLC, COVID-19 Community Mobility Reports (CC BY), https://www.google.com/covid19/mobility/
- World Bank Global Economic Monitor and IMF International Financial Statistics, via DBnomics.
- Hale et al. (2021), Oxford COVID-19 Government Response Tracker (CC BY 4.0).
- Price series from Yahoo Finance and Stooq, re-downloaded by `pipeline/02_...`.

Please cite the paper and the sources above when using these files.
