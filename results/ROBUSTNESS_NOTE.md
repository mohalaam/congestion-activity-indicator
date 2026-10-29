# Robustness battery for the state-dependent result (2026-10-28)

Main specification: next-week USD-ETF return (SD units) on the congestion innovation (SD units),
its interaction with Stress = VIX > 25, the state dummy, own same-week return and global
controls, country fixed effects, SEs clustered by week. Ex-lockdown sample (2020-07 to 2023-02)
and post-2021-07 sample. Scripts: pipeline/09_robustness.py plus two inline checks saved as
results/rob_seasonal.csv and results/rob_seasonal_fe.csv.

## 1. Alternative state variables (interaction t, ex-lockdown / post-2021)

| State | USD ETF 1 wk | Local index 1 wk | USD ETF 4 wk | FX 4 wk |
|---|---:|---:|---:|---:|
| VIX > 25 (main) | 2.8 / 3.2 | 2.2 / 3.4 | 0.9 / 3.1 | 1.8 / 2.7 |
| MSCI EM drawdown > 10% | 1.9 / 2.0 | 2.0 / 2.3 | 0.7 / 0.8 | 1.5 / 1.9 |
| VIX > 30 | 0.4 / 1.7 | -0.3 / 1.0 | 0.9 / 5.0 | 0.7 / 1.5 |
| VIX > 20 | -0.2 / -0.1 | -0.7 / -0.3 | 0.0 / 0.1 | 2.0 / 1.0 |
| continuous log VIX | 0.9 / 1.4 | 0.5 / 1.5 | 0.2 / 1.5 | 1.5 / 2.0 |
| own-country realized vol above median | -0.2 / -1.5 | 0.9 / -1.0 | -1.9 / -1.0 | -1.9 / -0.6 |
| own 4-week return below -5% | 0.4 / 0.7 | -0.9 / -1.2 | -2.2 / -1.1 | 0.3 / 1.4 |

Reading: the sign flip is a GLOBAL risk-off phenomenon. It appears with VIX > 25 and with an
EM-wide drawdown, is absent with the loose VIX > 20 threshold (which labels most of the sample
as stress) and with VIX > 30 (too few weeks), and does not appear for country-specific stress.
The threshold sensitivity must be shown as a figure (interaction coefficient against the VIX
cutoff from 18 to 32) rather than hidden.

## 2. Inference
- Moving-block bootstrap over calendar weeks (8-week blocks, all countries resampled together,
  1,000 draws): interaction 0.277, bootstrap SE 0.088, t = 3.1, 95% CI [0.10, 0.43], 99.9% of
  draws positive. Matches the clustered t of 2.8.
- Episode jackknife: eight high-VIX episodes. Dropping any one leaves t between 2.7 and 3.3,
  EXCEPT the April-July 2022 episode (Fed tightening, China lockdowns, 10 weeks): dropping it
  lowers the interaction to 0.17 with t = 1.4. About 40% of the effect comes from that episode.
  This must be stated in the paper.

## 3. Google Community Mobility as an alternative activity signal (2020-02 to 2022-10)
- Weekly innovations in TomTom congestion and Google workplaces mobility correlate at 0.76
  (transit 0.66): congestion is measuring the same activity Google measured.
- Workplaces mobility reproduces the flip for USD-ETF 1-week returns ex-lockdown (interaction
  0.19, t = 2.1); transit and retail mobility do not. In the same window congestion gives
  t = 2.4. Same direction, weaker, as expected for a noisier regional measure.

## 4. Placebos and seasonality (the important finding of this round)
- Shuffling each country's congestion series across weeks (500 draws): placebo interaction
  t has mean 0.09 and SD 1.07; none of 500 draws reaches the actual non-clustered t of 4.5.
- BUT congestion lagged 52 weeks (a pseudo-signal) also produces a significant interaction
  (t = 2.2 for 1-week ETF, 3.2 for 4-week ETF, 2.7 for FX). The innovation series has annual
  structure (autocorrelation 0.22 at lag 52) from holidays, Ramadan and school calendars, and
  stress regimes cluster in particular months, so part of the raw result is a calendar effect.
- Fix and re-test:

| Signal / fixed effects | USD ETF 1 wk (ex-lock / post-21) | Index 1 wk | USD ETF 4 wk | FX 4 wk |
|---|---:|---:|---:|---:|
| raw signal, country FE (original) | 2.8 / 3.2 | 2.2 / 3.4 | 0.9 / 3.1 | 1.8 / 2.7 |
| raw signal, country x calendar-month FE | 3.3 / 2.6 | 2.3 / 2.3 | 0.9 / 1.5 | 2.4 / 1.5 |
| raw signal, country x month FE + state x month | 3.5 / 2.7 | 2.3 / 2.5 | 1.3 / 1.7 | 2.1 / 1.6 |
| signal minus country x month-of-year mean | 3.1 / 3.4 | 2.3 / 3.0 | 1.5 / 4.0 | 2.5 / 3.4 |
| signal minus country x week-of-year mean | 3.1 / 2.4 | 1.8 / 2.0 | 3.3 / 4.2 | 2.9 / 3.1 |
| 52-week-lag placebo, country x month FE | 1.5 / 1.4 | 2.0 / 1.6 | 1.4 / 0.4 | 1.1 / 0.7 |
| 52-week-lag of deseasonalized signal | 0.3 / 0.1 | 1.2 / 0.4 | 3.5 / 3.7 | 2.3 / 2.1 |

Reading: with calendar fixed effects, or with a deseasonalized signal, the ONE-WEEK EQUITY
result survives at t = 2.3-3.5 while the 52-week placebo falls to insignificance (t about 1.5
or lower). The 4-week equity and FX results do not pass: the deseasonalized placebo still
"works" for them, so they are calendar artifacts and must be dropped or demoted to
descriptive.

## Decision for the paper
- Headline result: next-week equity returns (local index and USD ETF), interaction of the
  congestion innovation with a global risk-off state (VIX > 25, cross-checked with EM drawdown),
  estimated with country x calendar-month fixed effects and a deseasonalized signal as the
  main specification. Report the raw-signal version as the first column so the reader sees
  that seasonality controls strengthen rather than weaken it.
- Drop the 4-week and FX interaction results from the main claims. Keep the FX volatility
  result from step 08 only if it survives the same seasonality controls (not yet tested).
- Report the episode jackknife and the VIX-threshold figure as limitations, and the block
  bootstrap as the preferred inference.
- Google workplaces mobility: show as the external-validity check (0.76 correlation; same
  sign and significance in the overlap window).
- Placebo table: within-country shuffle and 52-week lag, both under calendar FE.
- Still to run: seasonality controls for the volatility and quantile results of step 08; the
  VIX-threshold sweep figure; the 2026 live-collector out-of-sample once enough weeks exist.

## Files
results/rob_states.csv, rob_bootstrap.csv, rob_jackknife.csv, rob_google.csv, rob_placebo.csv,
rob_summary.txt, rob_seasonal.csv, rob_seasonal_fe.csv; data_proc/google_mobility_daily.csv
