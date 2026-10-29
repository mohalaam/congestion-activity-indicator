# Round-2 statistics: what changed (2026-10-28)

Script: pipeline/17_round2_stats.py; table results/tables/round2_stats.md.

## 1. Seasonality is real but much smaller than v3 claimed
On a true weekly time index (lockdown weeks set to missing, so lags are genuine 52-week lags):

| level | in-sample week-of-year R2 | adjusted R2 | leave-one-year-out R2 | Fourier-3 R2 | share with Fourier F p<0.05 | mean ac(52) |
|---|---:|---:|---:|---:|---:|---:|
| 49 cities | 0.55 | 0.28 | -0.30 | 0.09 | 0.39 | 0.35 |
| 12 countries | 0.55 | 0.27 | -0.30 | 0.10 | 0.42 | 0.31 |
| EM factor | 0.67 | 0.47 | 0.08 | 0.13 | 1.00 | 0.56 |
| Google, 12 countries | 0.57 | 0.24 | -0.48 | 0.07 | 0.25 | 0.33 |

The in-sample R2 of 0.55 is overfitting: 52 cells on 138 weeks (chance level about 0.37).
Out of sample (leave one year out) the week-of-year profile predicts nothing; a smooth 3-harmonic
seasonal explains 9-13 percent of variance and is significant in 42 percent of countries (India,
Malaysia, South Africa, Mexico, Egypt, Indonesia at the margin) and for the factor. The honest
statement: congestion innovations contain a modest, country-specific annual component
(ac(52) 0.31 at the country level, 0.56 for the factor; a smooth seasonal of about 10 percent of
variance), concentrated in countries with fixed-date holidays (Brazil, South Africa, Poland,
Mexico, Thailand: ac(52) 0.46-0.74) and absent in Turkey, India, Indonesia and Malaysia.
Abstract figures "55 percent / 67 percent" must be withdrawn.

## 2. The attenuation argument is not decisive at this sample size
Monte Carlo on the placebo sample (n = 946 after requiring the lagged signal and all controls):
observed actual interaction 0.157 (t 2.0), lag-52 placebo 0.109 (t 1.8), seasonal difference
-0.009 (t -0.2). Simulating returns under "x is entirely news" with noise calibrated to the
actual fit, the ratio placebo/actual has median 0.12 but a 5-95 percent range of [-1.5, 1.7];
the seasonal-difference ratio has median 0.33 and range [-0.9, 1.6]; 21 percent of news-only
simulations produce a seasonal-difference ratio at or below the observed one. Under "y responds
only to the seasonal component" the distributions are similar (27 percent). With interaction
t-statistics around 2, the three-version comparison cannot discriminate the hypotheses; the
Methodology seat's analytic bound assumes away sampling noise that dominates here. The
Devil's Advocate's objection is sustained: on three years the lag placebo and the seasonal
difference are informative about the signal's structure, not decisive about the return result.

## 3. What the calendar-preserving placebos show (full ex-lockdown sample, n = 1,518-1,617)
| regressor | calm | t | interaction | t |
|---|---:|---:|---:|---:|
| actual x | -0.054 | -1.8 | 0.259 | 3.7 |
| own in-sample week-of-year profile (pure seasonal component) | -0.041 | -1.6 | 0.156 | 2.9 |
| another country's week-of-year profile (rotated) | -0.001 | 0.0 | 0.007 | 0.1 |
| x minus own in-sample profile (non-seasonal residual) | -0.024 | -0.9 | 0.102 | 2.0 |
| circular block shift of the whole panel, 300 draws | | | placebo t mean 0.18, SD 1.02; 0/300 >= 3.69 | |

Reading: the interaction decomposes into a part carried by each country's own annual pattern
(0.16, t 2.9) and a part carried by the non-seasonal residual (0.10, t 2.0). Another country's
calendar does nothing, and breaking the alignment between the calendar and the 2022 stress
weeks (circular shift) removes it entirely. The result is therefore tied to each country's own
seasonal pattern coinciding with the risk-off weeks of 2022, with a residual non-seasonal
component that is marginal. "Calendar artifact" is too strong; "predominantly, and not
separably on three years" is right.

## 4. The 2022 anchor
One standardization (SD of F - F_52 over the ex-lockdown sample = 0.754): within 2022 the
seasonally differenced factor interaction is 2.02 percent per SD (t 2.2); with holiday-share
controls 2.00 (t 2.4); ex-lockdown 0.66 (t 1.2) and 0.98 (t 2.2) with holiday shares; 2021
-1.27 (t -0.4). The note's 2.68 was the unstandardized coefficient. Carry 2.02 (2.00 with
holidays) into the text and the pre-registration; quote all three sub-periods.

## Consequences for MANUSCRIPT_v3
- Abstract/Sec. 2.3/3.2: replace the R2 claims with ac(52), Fourier, and the fixed-vs-moving
  holiday contrast; Turkey/India sentence rewritten (no annual structure found by any test).
- Sec. 3.3: replace "reproduced / disappears" with the decomposition in (3) and the
  simulation in (2); state that the diagnostics cannot settle the question on three years.
- Sec. 3.5/Pre-registration: anchor 2.02 (t 2.2), 2.00 with holidays; all sub-periods quoted.
- The paper's thesis becomes: conditional predictability results on mobility signals are
  entangled with the signals' own calendar structure; on short samples the available placebos
  are informative but underpowered; hence pre-registration and a second risk-off period.
