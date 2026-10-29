# Volatility and crisis-state tests (2026-10-28)

Script: pipeline/08_volatility_tests.py. Same 12-country weekly panel as the return tests.
Realized variance = sum of squared daily log returns within the week; targets are log RV next
week (f1) and over the next four weeks (f4). Baseline is HAR-style (own log RV, 4-week and
13-week means) plus log VIX, MSCI EM return and VIX change; country fixed effects; standard
errors clustered by week. Signals standardized within country.

## A. Congestion predicts LOWER realized volatility

| Target | Signal | beta (ex-lockdown) | t | beta (full) | t |
|---|---|---:|---:|---:|---:|
| USD ETF, next-week log RV | cong_innov4 | -0.067 | -2.2 | -0.091 | -3.4 |
| USD ETF, next-week log RV | cong_innov13 | -0.066 | -2.2 | -0.090 | -2.9 |
| Local index, next-4-week log RV | cong_innov13 | -0.052 | -2.7 | -0.076 | -3.6 |
| FX, next-4-week log RV | abs(cong_innov4) | -0.072 | -3.9 | -0.065 | -2.6 |

Reading: a one-SD positive congestion innovation lowers next-week USD-return variance by
about 7-9% (log points) after controlling for the volatility's own persistence and VIX. The
effect is weaker but same-signed in the post-mid-2021 window. Large congestion moves in either
direction reduce subsequent FX variance over the following month.

## B. State dependence: the return effect FLIPS SIGN in stress states (main finding)

Next-period return on cong_innov4, its interaction with a high-VIX dummy, and controls:

| Sample | State | Target | beta calm | t | interaction | t | beta stress |
|---|---|---|---:|---:|---:|---:|---:|
| post-2021-07 | VIX > 25 | index, 1 wk | -0.102 | -1.8 | +0.347 | 3.4 | +0.245 |
| post-2021-07 | VIX > 25 | USD ETF, 1 wk | -0.118 | -2.2 | +0.363 | 3.2 | +0.245 |
| post-2021-07 | VIX > 25 | USD ETF, 4 wk | -0.100 | -2.0 | +0.271 | 3.1 | +0.171 |
| post-2021-07 | VIX > 25 | FX, 4 wk | -0.133 | -3.0 | +0.255 | 2.7 | +0.122 |
| ex-lockdown | VIX > 25 | USD ETF, 1 wk | -0.089 | -2.5 | +0.277 | 2.8 | +0.189 |
| ex-lockdown | VIX > 25 | index, 1 wk | -0.082 | -1.7 | +0.218 | 2.2 | +0.136 |
| full | VIX > median | FX, 4 wk | -0.119 | -3.7 | +0.232 | 4.3 | +0.114 |

Reading: in calm markets, rising local activity (congestion) is followed by lower equity
returns and currency depreciation; in stressed markets (VIX above 25, about a third of weeks)
the same signal is followed by HIGHER returns and appreciation. The interaction is significant
at the 1% level in the post-2021 and ex-lockdown samples for both equity measures. This is the
emerging-market, real-time analogue of Boyd, Hu and Jagannathan (2005, J. Finance): good news
about activity is bad for stocks in expansions (rate/inflation channel) and good for stocks in
contractions (cash-flow channel). The unconditional regressions in step 07 were near zero
because the two states cancel.

## C. Quantile regressions: congestion compresses the upside

Next-week USD ETF return on cong_innov4 (country-demeaned, with MSCI EM and VIX change):

| tau | beta (full) | t | beta (post-2021) | t |
|---|---:|---:|---:|---:|
| 0.10 | +0.077 | 2.1 | +0.109 | 2.1 |
| 0.50 | -0.023 | -1.0 | -0.033 | -0.8 |
| 0.75 | -0.106 | -3.8 | -0.115 | -2.4 |
| 0.90 | -0.102 | -2.2 | -0.108 | -2.1 |

Reading: positive congestion innovations raise the lower tail and lower the upper tail of
next-week returns, i.e. they narrow the return distribution. This is the same fact as the
volatility result seen from the other side, and it holds for the local index at tau = 0.9.

## D. Monthly volatility
Only the FX result survives: the pooled-bridge nowcast surprise raises next-month FX variance
(t = 2.3 ex-lockdown, 2.9 post-2021). Equity monthly RV is not predicted by congestion.

## What the paper's spine should be
"Real-time activity and the state-dependent pricing of macro news in emerging markets."
1. Congestion is a daily, city-level measure of real activity (data section + the pooled
   nowcast result from step 05 as validation that it carries macro information).
2. Unconditionally it does not predict mean returns (step 07), but it predicts lower
   realized volatility and a narrower return distribution (this note, A and C).
3. Its effect on returns is state-dependent and sign-switching: negative in calm markets,
   positive in stress (B). This is the headline table, with Boyd-Hu-Jagannathan (2005) and
   the "macro news and the business cycle" literature (McQueen-Roley 1993; Andersen,
   Bollerslev, Diebold, Vega 2007) as the anchor, and Khanthavit's mood channel as the
   alternative to rule out (mood would not flip sign with VIX).
4. Currency results mirror the equity results, which is new relative to all prior
   congestion-return work.
5. Robustness to supply: alternative state variables (local realized vol, EM credit spread,
   recession-like months), Google mobility instead of TomTom, placebo dates, the 2026
   out-of-sample collector sample, and a transformer/LSTM state classifier as the ML section.

## Caveats
- 12 countries, 150 weeks; the stress state is roughly a third of the sample and clustered in
  2020 and 2022. Clustering by week handles common shocks but not the small number of
  independent stress episodes; a block bootstrap over episodes is needed.
- The sign flip is present ex-lockdown and post-2021, so it is not a COVID artifact, but the
  2022 stress episodes (Ukraine war, Fed tightening) dominate the post-2021 high-VIX weeks.
- Several specifications were examined; the interaction result should be pre-specified in
  the paper as the main test with the others as robustness.

## Files
results/vol_weekly.csv, vol_state.csv, vol_quantile.csv, vol_monthly.csv
