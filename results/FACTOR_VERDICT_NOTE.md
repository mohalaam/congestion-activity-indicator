# Verdict on the factor specification (2026-10-28)

Scripts: pipeline/14_factor_robustness.py (results/tables/table_factor_robustness.md) and an
inline seasonal check reproduced below. All on the ex-lockdown sample, USD returns.

## What the battery shows for the EM activity factor F (cross-country mean innovation)

| Test | Result | Reading |
|---|---|---|
| Headline F x S, week-clustered | 0.99, t = 3.0 | as in v2 |
| Moving-block bootstrap, 8-week blocks | boot SE 0.98, t = 1.0, 95% CI [0.00, 3.59] | clustered t badly overstates precision: F is one time series, so the effective sample is 138 weeks in 8 stress episodes, not 1,518 country-weeks |
| Alternative states | VIX>20: 0; top tercile: 0.58 (t 1.9); VIX>30: -1.6 (t -6.4, 9% of weeks); EM drawdown: 0.06 (t 0.2); continuous log VIX: t 1.1 | the reversal exists only for cutoffs around 23-27 and not for the EM-specific state |
| Episode jackknife | all t >= 2.5 except dropping Apr-Jul 2022 (t 1.7) | as before |
| Country exclusion | 0.88-1.17, t 2.6-3.7 | not a country effect |
| Circular block shift of F (500) | placebo mean -0.06, SD 1.2, 0/500 >= actual | passes |
| F lagged 52 weeks, same sample | placebo 0.63 (t 2.2) vs actual 0.63 (t 3.2) | FAILS: last year's factor predicts as well as this year's |
| Google workplaces common factor | corr with F = 0.81; Google F x S = 0.15 (t 0.8) | FAILS to replicate |
| Volatility (F on next-week log RV) | -0.15 (t -1.6) ETF, -0.18 (t -1.9) index | weak |
| Basket timing rule | gross Sharpe 1.07, net 10 bp 0.84; calm leg alone Sharpe 1.07, stress leg 0.40 | the money is in the calm-state leg |

## The seasonal check that decides it (basket time series, % per week, HAC)

| Factor version | Sample | F calm | t | F x S | t |
|---|---|---:|---:|---:|---:|
| Raw F | ex-lockdown (138) | -1.19 | -3.3 | 3.11 | 4.2 |
| Raw F | 2022 | -2.05 | -2.4 | 5.01 | 6.0 |
| F lagged 52 weeks (placebo) | ex-lockdown (100) | -0.41 | -2.2 | 1.11 | 1.4 |
| F lagged 52 weeks (placebo) | 2022 | -1.44 | -1.6 | 2.09 | 2.1 |
| F seasonally differenced, real time (F - F_{t-52}) | ex-lockdown (100) | 0.04 | 0.3 | 0.88 | 1.2 |
| F seasonally differenced, real time | 2022 | -1.15 | -1.1 | 2.68 | 2.2 |
| F week-of-year demeaned, in-sample (look-ahead) | ex-lockdown (138) | -0.82 | -2.0 | 3.41 | 3.5 |

The factor has a 52-week autocorrelation of 0.29 in the time series (0.56 in the panel sample).
Averaging across countries removes idiosyncratic noise and leaves the shared calendar: year-end,
Ramadan and Eid, Lunar New Year, Easter, school holidays. A placebo built from last year's factor
reproduces the calm-state coefficient (t = -2.2) and, in 2022, the interaction (t = 2.1). Once
the factor is seasonally differenced in real time, the calm-state response disappears (0.04)
and the interaction is insignificant (t = 1.2) outside 2022; within 2022 a reversal remains
(2.68, t = 2.2) on 52 weeks. In-sample week-of-year demeaning preserves the result, but it uses
the full sample and is not available to an investor.

## Conclusion

The state-dependent pricing claim does not survive on the factor specification once seasonality
is handled without look-ahead. The country-signal version in v1 survived its 52-week placebo for
USD returns, but the panel showed that result was carried by the common component, and the
common component is what fails here. The chain closes against the claim: what looked like
state-dependent pricing of activity news is, to a large extent, a calendar pattern in emerging-
market congestion interacting with the calendar clustering of 2022's risk-off weeks.

What is left standing:
1. The data set and pipeline (49 cities, 12 countries, daily, 2020-2023; live collector since
   October 2026).
2. A clear methodological finding: congestion and mobility signals carry strong annual
   calendar structure that survives weekday adjustment, month fixed effects and even
   country-by-year effects; return-predictability results built on them are not credible
   without a real-time seasonal difference and a 52-week-lag placebo. This generalizes to the
   single-city literature (Khanthavit; Tang; Thaker), none of which ran such a test.
3. A modest nowcasting result (pooled bridge, 14% RMSE gain concentrated in disruptions).
4. A weak, unconditional negative link from congestion innovations to next-week realized
   variance (t -1.6 to -2.2 depending on specification).
5. A 2022-only reversal (t 2.2 after real-time deseasonalization) that is a hypothesis for the
   2026 out-of-sample test, not a finding.

## Recommendation
Do not write Sections 3.4-3.7 and the conclusion around the factor pricing claim; they would be
built on a result that fails its own placebo. Two honest routes:
A. A data-and-methods paper: "Urban congestion as a real-time activity indicator for emerging
   markets: measurement, validation, and a seasonal placebo for mobility-based return
   predictability." Main results = validation (Google, nowcast), the seasonality diagnosis
   with the placebo that overturns the single-city literature, the volatility link, and the
   2022 reversal as a pre-registered hypothesis for the live sample. Fits Borsa Istanbul
   Review's scope less tightly but is defensible and useful.
B. Hold the asset-pricing paper until the 2026 collector gives a second risk-off period and
   test the pre-specified hypothesis there. Meanwhile submit the nowcasting/data contribution
   to a transport or applied-economics venue.
