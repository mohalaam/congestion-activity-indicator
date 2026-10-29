# Pre-registered out-of-sample test (to be time-stamped and deposited before the 2026 data are analysed)

Registered: 2026-10-28 (draft; deposit on OSF or AsPredicted with a hash of this file).

## Hypothesis H1 (from the 2020-2023 exploratory sample)
In weeks in which the VIX closes above 25, a positive innovation in the emerging-market
congestion factor is followed by a higher next-week US-dollar return on an equal-weight basket
of emerging-market country funds than in weeks in which the VIX closes at or below 25
(b_2 > 0 in the specification below). The exploratory estimates, on the real-time
seasonally differenced factor standardized by its ex-lockdown standard deviation, are
b_2 = 2.0 percent per standard deviation within 2022 (t = 2.2; 2.0, t = 2.4, with holiday-share
controls, 52 weeks), 0.7 (t = 1.2) over July 2020 to February 2023 (1.0, t = 2.2, with holiday
controls), and -1.3 (t = -0.4) within 2021. The primary object is the stress-state response
b_1 + b_2; b_2 is secondary. We make no prediction about the calm-state coefficient b_1, which
did not survive seasonal differencing in the exploratory sample. Cutoffs of 20 and 30 were
examined in the exploratory sample and did not produce the pattern; 25 is retained because it
is the only cutoff that did, which is a reason for caution, not confidence.

## Data (fixed in advance)
- Signal: TomTom live-feed hourly congestion ("trafficIndexLive") collected by our own
  collector from 2026-10-21 for all 490 cities, aggregated to daily city means, weekday-adjusted
  log deviations (trailing 52-week same-weekday mean once available; until then the 2026
  weekday mean), population-weighted to the same 12 countries with the same city lists and
  weights as the 2020-2023 sample, averaged to Friday-ending weeks, innovation = week minus
  trailing 4-week mean, real-time seasonal difference = innovation minus the innovation 52
  weeks earlier (so the test window begins 52 weeks after collection starts, i.e. October 2027),
  standardized by the trailing 52-week standard deviation. Factor F_t = cross-country mean.
- Returns: the same eleven US-dollar country funds, equal weight, Friday close to Friday close,
  position taken at the following Monday open for the trading-rule evaluation.
- State: S_t = 1[VIX close on Friday t > 25]. No other cutoff will be reported as a primary test.
- Controls: own basket return week t, MSCI EM fund return, change in log VIX, Brent return,
  change in log DXY, change in US 10-year yield, log VIX level, the country-average weekly
  change in the Oxford stringency index (or its successor; zero if discontinued), and the
  country-average lagged weekly change in the local-currency oil price (log Brent plus log local
  currency per USD) as a fuel-price proxy, each also interacted with S_t. Exploratory estimate
  with this full control set, within 2022: b_2 = 1.7 percent per SD (t = 2.3).
- Holiday dummies: the same calendar as the exploratory sample, extended to the test years.

## Specification (primary)
basket_r_{t+1} = a + b_1 F_t + b_2 F_t S_t + b_3 S_t + g' z_t + k' z_t S_t + h' H_t + u_{t+1},
Newey-West with 4 lags, on all weeks from October 2027 to the pre-announced end date
(24 months after the start of the test window, or the first date at which at least 30 weeks
with S_t = 1 have accumulated, whichever is later).

## Decision rule
H1 is supported if b_2 > 0 with a one-sided p-value below 0.05 under Newey-West and a
moving-block bootstrap (8-week blocks) 95 percent interval that excludes zero. H1 is rejected
if the point estimate is negative or the one-sided p-value exceeds 0.20. Otherwise the test
is inconclusive and will be reported as such. No alternative state variable, horizon,
signal version or target will be substituted for the primary test; any such analysis will be
labelled exploratory.

## Secondary, pre-specified
S1. Next-week log realized variance of the basket on F_t with HAR controls: predicted
negative (exploratory estimate -0.06 to -0.08 per SD, t about -2.2 to -2.6).
S2. The same primary regression with the Google-mobility-free period acknowledged: no Google
replication is possible after 2022.

## Known threats recorded now
- The TomTom live feed is a different series from the 2020-2023 archive (post-2023 methodology);
  the test is therefore of the hypothesis, not of a spliced series.
- The sample will contain whatever risk-off episodes occur; if fewer than 30 stress weeks
  accumulate by the end date the test is underpowered and will be reported as inconclusive.
- Collector gaps longer than 7 days lose data; gaps will be logged and reported.
