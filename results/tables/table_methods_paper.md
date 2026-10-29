# Core tables for the data-and-methods paper

## A. Seasonality diagnosis of weekly innovations (ex-lockdown): autocorrelations and share of variance explained by week-of-year

| level | n | mean ac(1) | mean ac(4) | mean ac(52) | share ac(52) > 0.2 | mean week-of-year R2 |
|---|---:|---:|---:|---:|---:|---:|
| city | 49 | 0.40 | -0.18 | 0.35 | 0.65 | 0.55 |
| country | 12 | 0.48 | -0.13 | 0.31 | 0.58 | 0.55 |
| factor | 1 | 0.53 | -0.15 | 0.56 | 1.00 | 0.67 |
| google_country | 12 | 0.31 | -0.19 | 0.33 | 0.50 | 0.57 |
| google_factor | 1 | 0.28 | -0.21 | 0.39 | 1.00 | 0.61 |

Country detail (congestion): Brazil ac52=0.68; Egypt ac52=0.14; India ac52=0.08; Indonesia ac52=-0.06; Malaysia ac52=-0.07; Mexico ac52=0.57; Philippines ac52=0.40; Poland ac52=0.59; Saudi Arabia ac52=0.24; South Africa ac52=0.74; Thailand ac52=0.46; Turkey ac52=0.01

## B. Single-country regressions of next-week return on the country congestion innovation (HAC 4), ex-lockdown

| country | target | actual b | t | 52-wk placebo b | t | real-time seasonal diff b | t |
|---|---|---:|---:|---:|---:|---:|---:|
| Brazil | local index | 0.124 | 0.39 | -0.194 | -1.10 | 0.394 | 1.35 |
| India | local index | -0.012 | -0.07 | 0.144 | 0.83 | -0.154 | -0.83 |
| Indonesia | local index | 0.093 | 0.54 | -0.028 | -0.16 | 0.052 | 0.31 |
| Malaysia | local index | 0.057 | 0.39 | 0.127 | 1.22 | -0.147 | -1.23 |
| Mexico | local index | -0.254 | -0.82 | -0.297 | -1.08 | 0.252 | 1.94 |
| South Africa | local index | -0.448 | -1.86 | -0.286 | -1.64 | -0.085 | -0.56 |
| Turkey | local index | -0.389 | -1.33 | 0.107 | 0.34 | -0.175 | -0.68 |
| Brazil | USD ETF | 0.404 | 0.88 | -0.336 | -1.19 | 0.721 | 1.54 |
| India | USD ETF | -0.070 | -0.30 | 0.279 | 1.98 | -0.324 | -1.96 |
| Indonesia | USD ETF | 0.273 | 0.85 | -0.162 | -0.52 | 0.309 | 0.99 |
| Malaysia | USD ETF | 0.041 | 0.26 | 0.124 | 1.12 | -0.151 | -1.15 |
| Mexico | USD ETF | -0.200 | -0.51 | -0.461 | -1.37 | 0.421 | 2.25 |
| Philippines | USD ETF | -0.539 | -2.28 | -0.022 | -0.11 | -0.276 | -1.52 |
| Poland | USD ETF | -0.259 | -0.60 | -0.469 | -1.20 | 0.305 | 0.69 |
| Saudi Arabia | USD ETF | -0.205 | -0.77 | -0.226 | -1.25 | -0.030 | -0.11 |
| South Africa | USD ETF | -0.513 | -1.33 | -0.399 | -1.27 | -0.247 | -0.93 |
| Thailand | USD ETF | -0.151 | -0.66 | 0.054 | 0.32 | -0.026 | -0.16 |
| Turkey | USD ETF | -0.440 | -1.14 | 0.409 | 1.03 | -0.358 | -0.92 |

local index: countries with |t|>1.96: actual 0/7, placebo 0/7, seasonal-diff 0/7; mean |t|: 0.77 / 0.91 / 0.99

USD ETF: countries with |t|>1.96: actual 1/11, placebo 1/11, seasonal-diff 1/11; mean |t|: 0.87 / 1.03 / 1.11

### Pooled panel, next-week return (%) on signal, country x month FE, week-clustered

| target | version | n | b | t |
|---|---|---:|---:|---:|
| local index | actual | 963 | -0.183 | -1.22 |
| local index | 52-wk placebo | 697 | 0.044 | 0.39 |
| local index | seasonal diff | 697 | -0.076 | -0.71 |
| USD ETF | actual | 1518 | -0.198 | -1.17 |
| USD ETF | 52-wk placebo | 1098 | 0.015 | 0.09 |
| USD ETF | seasonal diff | 1098 | -0.113 | -0.73 |

## C. The state-dependent specification (eq. 3, USD ETF, SD units, full FE and controls) under the three signal versions

| version | n | x calm | t | x x S | t |
|---|---:|---:|---:|---:|---:|
| actual (raw) | 1518 | -0.054 | -1.83 | 0.259 | 3.69 |
| 52-wk placebo | 1098 | 0.025 | 0.74 | 0.082 | 1.22 |
| real-time seasonal diff | 1098 | -0.036 | -1.09 | 0.049 | 0.67 |
| actual, placebo sample | 1098 | -0.028 | -0.81 | 0.189 | 2.57 |

## D. Correlation of weekly innovations, congestion vs Google workplaces mobility

| country | all overlap | ex-lockdown | post-2021-07 |
|---|---:|---:|---:|
| Brazil | 0.91 | 0.89 | 0.91 |
| Egypt | 0.85 | 0.83 | 0.86 |
| India | 0.87 | 0.79 | 0.67 |
| Indonesia | 0.66 | 0.60 | 0.66 |
| Malaysia | 0.73 | 0.56 | 0.71 |
| Mexico | 0.81 | 0.77 | 0.84 |
| Philippines | 0.48 | 0.43 | 0.47 |
| Poland | 0.86 | 0.86 | 0.91 |
| Saudi Arabia | 0.40 | 0.48 | 0.50 |
| South Africa | 0.90 | 0.85 | 0.88 |
| Thailand | 0.80 | 0.80 | 0.70 |
| Turkey | 0.84 | 0.82 | 0.81 |
| pooled | 0.75 | 0.72 | 0.75 |

## E. Next-week log realized variance (USD ETF) on the country signal, HAR + log VIX, country x year + month FE

| version | n | b | t |
|---|---:|---:|---:|
| actual | 1507 | -0.075 | -2.61 |
| 52-wk placebo | 1087 | 0.012 | 0.39 |
| seasonal diff | 1087 | -0.060 | -2.17 |