# Volatility battery and non-seasonal confounders (2026-10-28)

Scripts: pipeline/18_volatility_battery.py (results/tables/volatility_battery.md),
pipeline/19_fuel_stringency.py (results/tables/fuel_stringency.md).

## Volatility: next-week log realized variance of USD country-fund returns on the signed country innovation

| spec | coefficient | t |
|---|---:|---:|
| baseline (v3 Table 7) | -0.075 | -2.6 |
| + moving-holiday dummies | -0.065 | -2.3 |
| per-trading-day variance target + holidays | -0.065 | -2.3 |
| Driscoll-Kraay(4) | -0.065 | -2.6 |
| moving-block bootstrap, 8-week blocks, 500 draws | SE 0.024, 95% CI [-0.104, -0.013] | -2.7 |
| + stringency change + lagged local-currency oil price | -0.065 | -2.2 |
| absolute innovation instead of signed | +0.055 | 1.3 |
| positive part / negative part | -0.031 / -0.087 | -0.6 / -1.8 |
| within 2020 H2 / 2021 / 2022 | -0.081 / -0.029 / -0.019 | -1.5 / -0.7 / -0.4 |
| circular block shift placebo, 300 draws | placebo mean 0.02, SD 1.08 | 1.0% of draws <= actual |
| local index target | -0.047 | -0.8 |
| factor F / residual e | -0.130 / -0.054 | -1.1 / -1.9 |
| 52-week lag placebo | +0.025 | 0.9 |
| real-time seasonal difference | -0.053 | -1.8 |
| economic size | R2 0.422 -> 0.424; 1 SD of x = -6.3% of variance, -3.2% of volatility | |

Reading:
1. The pooled effect is stable across the inference corrections and the holiday, per-day,
   stringency and fuel controls (t -2.2 to -2.7), passes the circular-shift placebo (1% of
   draws), and is absent for the 52-week lag.
2. It is signed, not symmetric: |x| has the wrong sign and is insignificant, and the effect
   comes from negative innovations (bad activity news raises variance, t -1.8) rather than
   positive ones (t -0.6). "Resolution of uncertainty" is the wrong label; the pattern is the
   volatility-feedback asymmetry (bad news raises variance) in the literature on asymmetric
   volatility.
3. It is a pooled effect that is not significant within any single year, is absent for the
   local index, and is marginal for the factor (t -1.1) and the residual (t -1.9).
4. It is small: 0.2 percentage points of R2 and about 3 percent of weekly volatility per SD.
5. The real-time seasonal difference keeps it at t -1.8, the lag placebo shows nothing: it is
   not seasonal, but it is weak.
Adjectives for the paper: "small, signed, pooled; survives the inference and placebo battery;
not detectable year by year".

## Stringency and fuel (eq. 1 state example, USD ETF, ex-lockdown)
- Oxford stringency: 12 countries, weekly mean and change; only 2.1% of ex-lockdown weeks
  have a change above 10 points. Fuel proxy: log Brent plus log local-currency-per-USD, weekly
  change, lagged one week (retail fuel prices adjust with a lag; a proxy, not pump prices).
- Adding both, each interacted with the state: actual interaction 0.259 (t 3.7) -> 0.273 (3.8);
  lag placebo 0.082 -> 0.078; seasonal difference 0.030 -> 0.037; dropping weeks with
  |d_strin| > 10: 0.279 (t 3.9); adding the stringency level: 0.275 (3.7).
- Controls' own coefficients: stringency change -0.006 (t -0.9), x S 0.022 (t 1.6); fuel 0.03
  (t 0.04), x S 0.04 (t 0.02). Correlation of the signal with the stringency change is -0.13,
  with the fuel proxy 0.02.
- Volatility: -0.065 (t -2.3) -> -0.065 (t -2.2).
- 2022 anchor (basket, seasonally differenced factor, holiday shares): 2.00 (t 2.4) -> 1.69
  (t 2.3) with stringency and fuel; ex-lockdown 0.98 (t 2.2) -> 1.00 (t 2.2); 2021 -1.26
  (t -0.4) -> -7.9 (t -1.9, 41 weeks, unstable).
Reading: the 2022 pattern and the volatility effect are not fuel-price or domestic-lockdown
artifacts, within the limits of a fuel proxy. The within-2021 estimate becomes unstable with the
extra controls on 41 weeks, which is one more reason to treat the year-by-year estimates as
descriptive.

## Numbers to carry
- Volatility headline: -0.065 (t -2.3 clustered, -2.6 DK, -2.7 bootstrap) with holiday
  dummies; signed; year-by-year not significant; 3 percent of volatility per SD.
- 2022 anchor with all controls: 1.7 percent per SD (t 2.3); pre-registration primary
  specification to include d_strin and the fuel proxy (each x S) as controls.
