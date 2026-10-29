# Fuel-price proxy and Oxford stringency controls

Stringency: 12 countries, 2020-01-03 to 2023-01-06; share of ex-lockdown weeks with |d_strin| > 10: 0.021

## Eq. (1), USD ETF, ex-lockdown, holiday dummies, with and without stringency change and lagged local-currency oil price (each also x S)

| signal | controls | n | calm | t | inter | t |
|---|---|---:|---:|---:|---:|---:|
| actual | baseline | 1518 | -0.054 | -1.83 | 0.259 | 3.69 |
| actual | + stringency + fuel | 1518 | -0.057 | -1.90 | 0.273 | 3.76 |
| lag-52 placebo | baseline | 1098 | 0.025 | 0.74 | 0.082 | 1.22 |
| lag-52 placebo | + stringency + fuel | 1098 | 0.027 | 0.78 | 0.078 | 1.16 |
| seasonal diff | baseline | 1098 | -0.040 | -1.29 | 0.030 | 0.43 |
| seasonal diff | + stringency + fuel | 1098 | -0.043 | -1.35 | 0.037 | 0.54 |
| actual | + controls, drop weeks with abs(d_strin) > 10 | 1485 | -0.059 | -1.91 | 0.279 | 3.93 |
| actual | + controls + stringency level | 1518 | -0.061 | -2.05 | 0.275 | 3.74 |

Controls' own coefficients (actual spec): d_strin -0.0056 (t -0.91), d_strin x S 0.0217 (t 1.61); fuel_l1 0.033 (t 0.04), fuel x S 0.036 (t 0.02). Correlation of x with d_strin: -0.126; with fuel_l1: 0.015

## Volatility (B2 spec) with stringency and fuel

| controls | n | x | t |
|---|---:|---:|---:|
| baseline + holidays | 1507 | -0.065 | -2.27 |
| + stringency + fuel | 1507 | -0.065 | -2.21 |

## A4 basket time series on the seasonally differenced factor, with holiday shares, stringency and fuel (HAC 4)

| sample | controls | n | F calm | t | F x S | t |
|---|---|---:|---:|---:|---:|---:|
| 2022 | holidays only | 52 | -0.63 | -0.84 | 2.00 | 2.44 |
| 2022 | + stringency + fuel | 52 | -0.41 | -0.57 | 1.69 | 2.28 |
| ex-lockdown | holidays only | 100 | -0.06 | -0.39 | 0.98 | 2.19 |
| ex-lockdown | + stringency + fuel | 100 | -0.02 | -0.15 | 1.00 | 2.23 |
| 2021 | holidays only | 41 | 0.01 | 0.05 | -1.26 | -0.35 |
| 2021 | + stringency + fuel | 41 | 0.20 | 1.08 | -7.90 | -1.89 |