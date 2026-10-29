# Nowcasting benchmarks: first results (2026-10-28)

Script: pipeline/05_nowcast_benchmarks.py. Target: month-on-month log growth of seasonally
adjusted industrial production (IP), 17 countries with both IP and daily congestion.
Expanding-window pseudo real-time evaluation, first out-of-sample month 2021-01, last 2023-01.
Set EXCL_LOCK=1 to drop March-June 2020 from every training window (files with suffix _exlock).

## Headline numbers (pooled over countries, RMSE relative to the AR(1) benchmark)

| Model | Trained on all months | Lockdown months excluded from training |
|---|---:|---:|
| AR(1) | 1.000 | 1.000 |
| Bridge (month-end monthly congestion change) | 1.151 | 1.024 |
| Bridge, first 15 days only | 1.172 | 1.025 |
| Bridge with 2 lags | 1.194 | 0.974 |
| Unrestricted MIDAS (4 weekly blocks + prev month) | 1.419 | 3.049 |
| Almon MIDAS (60 daily lags, 2 params) | 1.083 | 1.194 |
| Pooled bridge, country fixed effects | 0.968 | **0.860** (DM t = 1.74, p = 0.08) |
| Pooled unrestricted MIDAS | 0.997 | 0.948 |

Ex-COVID evaluation window (2021-07 onward), lockdown excluded from training: pooled bridge
0.919 (DM p = 0.11), directional accuracy 57% vs 53% for AR. All other models >= AR.

## What this means
1. The strong congestion-IP comovement in the raw data is a lockdown artifact. Pooled
   correlation of yoy congestion with yoy IP is 0.39 over the full sample but 0.04 once
   March-June 2020 is removed, and 0.05 within countries after mid-2021.
2. Country-by-country models have 12-25 training months and overfit; every single-country
   congestion model is worse than AR. Pooling across countries is what makes congestion useful:
   the pooled bridge gives a 14% RMSE reduction (8% ex-COVID), marginally significant.
3. High-parameter MIDAS specifications are hopeless at this sample size. Daily detail must be
   compressed (Almon or a learned encoder) and estimated pooled, with shrinkage.
4. Monthly IP growth is close to white noise outside crises (AR RMSE ex-COVID 0.027 log
   points), so there is little variance to explain. The value of congestion is concentrated in
   turning points, which is consistent with the central-bank "timeliness, not accuracy" view.

## Implications for the paper
- Reframe the nowcasting section honestly: congestion nowcasts help in a pooled panel with
  fixed effects and during disruptions; they do not beat a univariate benchmark country by
  country in calm months. This is itself a finding and matches Woloszko (2020) and
  Gamtkitsulashvili and Plekhanov (2023).
- The deep-learning section should be a pooled, regularized model (shared encoder across
  countries, early stopping, lockdown dummy), evaluated with the same rolling design, not 17
  separate models. Expect gains in turning points, not in average RMSE.
- The return-predictability tests should use the POOL_BRIDGE surprise (saved in
  data_proc/nowcast_surprises.csv, lockdown-excluded version) and, separately, the raw
  congestion innovation. If congestion predicts returns while barely improving IP nowcasts, the
  channel is information about activity that official data never fully reveal, or attention.
- Alternative targets worth testing: retail sales (8 countries), 3-month IP growth, and the
  level of IP relative to its pre-COVID trend (less noisy than m/m).

## Files
results/nowcast_benchmarks_summary.csv, _bycountry.csv (all months in training)
results/nowcast_benchmarks_summary_exlock.csv, _bycountry_exlock.csv (lockdown excluded)
results/nowcast_predictions.csv, nowcast_predictions_exlock.csv (country-month nowcasts)
data_proc/nowcast_surprises.csv (currently the lockdown-excluded POOL_BRIDGE version)
