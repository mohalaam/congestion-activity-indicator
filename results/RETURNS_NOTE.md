# Return predictability: first results (2026-10-28)

Script: pipeline/07_return_predictability.py. Sample: 12 main EM countries, weekly 2020-01 to
2023-02 (about 152 weeks per country), monthly 2020-01 to 2023-01. Signals and returns are
standardized within country, so betas are in standard-deviation units. Weekly regressions have
country fixed effects, same-week global controls (MSCI EM, VIX, Brent, DXY, US 10y) and the own
same-week return, with standard errors clustered by week. Monthly regressions use Newey-West.

## A. Weekly panel, next-week and next-4-week returns

| Return | Horizon | Signal | beta (ex-lockdown) | t | beta (post-2021-07) | t |
|---|---|---|---:|---:|---:|---:|
| Local index | 1 wk | innov4 | -0.040 | -0.9 | -0.040 | -0.7 |
| Local index | 4 wk | innov4 | -0.060 | -1.9 | -0.050 | -0.9 |
| USD ETF | 4 wk | innov4 | -0.039 | -1.4 | -0.042 | -0.9 |
| FX (+ = appreciation) | 4 wk | innov4 | -0.067 | -2.6 | -0.084 | -2.0 |
| FX | 4 wk | innov13 | -0.028 | -1.1 | -0.087 | -2.3 |

Reading: within a country, a positive congestion innovation is followed by slightly LOWER
equity returns and currency depreciation over the next month. Effects are small (0.04-0.09 SD
per SD of signal) and only the FX results reach conventional significance.

## B. Weekly cross-country sort (long top third, short bottom third of congestion innovation, USD ETFs)

| Sample | Weeks | Mean weekly return | t (NW) | Annualized Sharpe | Hit rate |
|---|---:|---:|---:|---:|---:|
| Full | 152 | 0.23% | 1.43 | 0.83 | 0.56 |
| Ex-lockdown | 138 | 0.29% | 1.72 | 1.03 | 0.57 |
| Post-2021-07 | 86 | 0.32% | 1.33 | 1.05 | 0.62 |

Reading: ACROSS countries the sign flips. Countries whose congestion rose most relative to the
others earn higher USD returns the following week. Sharpe near 1 but t below 2, so suggestive,
not conclusive, with 12 countries and 150 weeks. The time-series (within-country) and
cross-sectional (across-country) channels differ and must be presented as such.

## C. Monthly panel

| Return | Horizon | Signal | beta (post-2021-07) | t (NW) | beta (ex-lockdown) | t |
|---|---|---|---:|---:|---:|---:|
| USD ETF | 1 m | intra-month congestion slope | -0.248 | -3.5 | -0.113 | -1.9 |
| USD ETF | 1 m | pooled-bridge nowcast surprise | -0.097 | -2.1 | -0.028 | -0.7 |
| FX | 1 m | intra-month congestion slope | -0.148 | -2.1 | -0.105 | -2.2 |
| FX | 1 m | nowcast surprise | -0.158 | -2.7 | -0.078 | -1.6 |
| FX | 1 m | nowcast level | -0.150 | -2.4 | -0.064 | -1.2 |
| Local index | 1 m | congestion slope | -0.146 | -1.3 | -0.090 | -1.2 |

Reading: the strongest and most consistent signal is the INTRA-MONTH SLOPE of congestion
(activity accelerating into month end), which negatively predicts next-month USD returns and
currency moves after mid-2021. The nowcast surprise built from the pooled bridge also predicts
FX depreciation (t = -2.7 post-2021). Monthly congestion level changes and innovations do not
predict anything.

## D. Sectors (Turkey, India only; Polish sector tickers returned no data)
No significant next-week effects. Turkish industrials and Indian energy are negative with
t around -1.6. Sector evidence is too thin to carry a section.

## Honest assessment
1. There is NO strong, robust return predictability from congestion at weekly or monthly
   horizons in this sample. Most coefficients are within one standard error of zero.
2. What survives: (i) a negative relation between accelerating congestion and next-month USD
   equity and currency returns after mid-2021 (t = -2 to -3.5); (ii) a cross-country
   long-short sort with Sharpe about 1 but t < 2. Neither would convince a referee alone.
3. The negative within-country sign is economically interpretable: rising activity in an EM
   raises expected tightening or inflation, or reflects the investor-stress channel of
   Khanthavit; the positive cross-country sign is the "relative momentum in activity" story.
   The paper would need to pick one and test it, not report both as discoveries.
4. Power is low: 12 countries, about 150 weeks, 36 months, dominated by 2020-2021. Many
   specifications were run, so the t-statistics near 2 should be discounted.

## Recommended next tests before deciding the paper's spine
- Volatility rather than returns: does congestion (or its slope) predict next-week realized
  volatility or GARCH variance? Activity signals often price risk rather than mean returns.
- Crisis states: quantile regressions and interaction with VIX; congestion may matter only
  when uncertainty is high (the one place the nowcast added value too).
- Announcement-day tests: returns on IP release days as a function of the congestion
  nowcast surprise (direct test of the information channel; small n but clean).
- Wait for the 2026 collector sample for a true out-of-sample check of the sort strategy.

## Files
results/returns_weekly.csv, returns_monthly.csv, returns_sort.csv, returns_sort_series.csv,
returns_sectors.csv
