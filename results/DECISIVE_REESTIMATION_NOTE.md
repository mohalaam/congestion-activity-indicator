# Decisive re-estimation: does the state-dependent result survive? (2026-10-28)

Script: pipeline/12_decisive_reestimation.py. Raw congestion innovation (no full-sample
deseasonalization, so the look-ahead objection is moot), S = 1[VIX > 25], week-clustered t
unless stated. Full ladder in results/tables/table_decisive.md.

## Headline target: next-week USD ETF return, ex-lockdown sample (n = 1,518)

| Specification | b calm | t | b interaction | t | b stress |
|---|---:|---:|---:|---:|---:|
| L1 country x month FE (old headline) | -0.107 | -2.9 | 0.307 | 3.3 | 0.200 |
| L2 + state x month FE | -0.101 | -2.7 | 0.292 | 3.4 | 0.191 |
| L3 + year FE | -0.101 | -2.6 | 0.291 | 3.4 | 0.189 |
| L4 country x year FE | -0.104 | -2.6 | 0.297 | 3.4 | 0.193 |
| L5 + moving-holiday dummies | -0.065 | -1.9 | 0.243 | 2.9 | 0.178 |
| L6 + state x all controls + log VIX level | -0.072 | -2.1 | 0.274 | 3.4 | 0.202 |
| L7 = L6 with Driscoll-Kraay(4) errors | -0.072 | -2.5 | 0.274 | 4.0 | 0.202 |

VERDICT 1: In the ex-lockdown sample the interaction SURVIVES year and country-by-year fixed
effects, moving-holiday dummies, state-interacted controls, the log VIX level and
Driscoll-Kraay errors (0.27, t = 3.4 clustered, 4.0 DK). The Devil's Advocate's "year contrast"
and "Ramadan 2022" explanations are rejected for this sample. The calm-state coefficient
weakens with holiday dummies (-0.07, t = -2.1) but keeps its sign.

## But: the effect is a 2022 phenomenon

| Sub-period (country FE + holidays) | n | b calm | t | b interaction | t |
|---|---:|---:|---:|---:|---:|
| within 2020 H2 only | 286 | -0.139 | -1.9 | 0.218 | 1.3 |
| within 2021 only | 583 | -0.004 | -0.1 | -0.181 | -1.2 |
| within 2022 only | 572 | -0.124 | -2.0 | 0.315 | 3.5 |
| post-2021-07 sample, full ladder L6 | 946 | -0.021 | -0.4 | 0.108 | 1.3 |

VERDICT 2: The sign switch is present in 2022 (t = 3.5), directionally present but imprecise
in 2020 H2 (t = 1.3), and ABSENT, with the wrong sign, within 2021 (t = -1.2). The post-2021
sample, which mixes 2021 H2 (null) with 2022 (strong), loses significance once holiday dummies
and state-interacted controls are added (0.11, t = 1.3). The panel's "one episode" concern is
confirmed in a sharper form: the result is identified by the 2022 risk-off year.

## And: it is carried by the common EM component, not country-specific activity

| L8 decomposition, L6 fixed effects and controls | b calm | t | b interaction | t |
|---|---:|---:|---:|---:|
| Common component (cross-country weekly mean of x), ex-lockdown | -0.257 | -2.0 | 1.000 | 2.9 |
| Idiosyncratic component (country minus mean), ex-lockdown | -0.042 | -1.4 | 0.124 | 2.0 |
| Common, post-2021 | -0.107 | -0.7 | 0.588 | 2.8 |
| Idiosyncratic, post-2021 | -0.007 | -0.2 | 0.036 | 0.4 |

VERDICT 3: The interaction loads mainly on the cross-country common component of congestion
innovations (coefficient 1.0, t = 2.9), i.e. weeks in which activity rises in all emerging
markets at once. Country-specific activity surprises carry a small interaction (0.12, t = 2.0)
ex-lockdown and nothing post-2021. The domain reviewer's alternative, "global growth news in
risk-off regimes rather than country activity", is largely correct.

## Local index returns
Ex-lockdown: survives the ladder at a lower level (0.19, t = 2.3 clustered, 2.8 DK), weakens
to t = 1.8 with holiday dummies alone. Post-2021: fails (0.18, t = 1.5). Within 2022: 0.32,
t = 2.5. Same picture as the USD target with less precision.

## What this means for the paper

The honest statement of the finding is:

"In risk-off weeks of 2022, a common rise in urban congestion across emerging markets was
followed by higher USD returns on emerging-market equities, while in calm weeks it was
followed by lower returns. The pattern is robust to year, country-by-year and calendar fixed
effects, moving-holiday dummies, state-interacted global controls and Driscoll-Kraay inference
in the July 2020 to February 2023 sample, but it is not present within 2021, and it is carried
by the cross-country common component of congestion rather than by country-specific surprises."

Consequences:
1. The paper's spine shifts from "country activity signals are priced state-dependently" to
   "a daily, congestion-based EM real-activity factor and its state-dependent pricing". The
   common component becomes the object of interest; the idiosyncratic component is a secondary
   result with a t of 2.0 at best.
2. The identification rests on 2022. The paper must say so in the abstract. The 2026 live
   collector becomes essential rather than optional: it is the only way to show the pattern in
   a second risk-off period. Until then the result is a documented hypothesis.
3. The raw signal with country-by-year and state-by-month fixed effects, holiday dummies and
   state-interacted controls (L6/L7) should be the headline specification. It removes the
   look-ahead and threshold-adjacent objections at no cost in the ex-lockdown sample.
4. The post-2021 sample should be replaced by within-year estimates (2020 H2, 2021, 2022) in
   the main table, because it is a misleading mixture.
5. A channel test is now sharper: if the common component is global EM growth news, the
   natural test is its interaction with US monetary-policy surprises and with the BEX
   risk-aversion component, as the domain reviewer proposed, rather than local yields.

## Files
results/tables/table_decisive.csv, table_decisive.md
