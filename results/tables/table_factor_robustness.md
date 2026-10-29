# Factor-specification results for Sections 3.4-3.7

## A. Next-week log realized variance on F and e (country x year + month FE, HAR + log VIX controls)

| target | sample | n | F | t | e | t | F x S | t |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| USD ETF | ex-lockdown | 1507 | -0.150 | -1.64 | -0.053 | -1.92 | -0.218 | -1.05 |
| USD ETF | 2021-2022 | 1155 | -0.170 | -1.67 | -0.039 | -1.25 | -0.117 | -0.60 |
| Local index | ex-lockdown | 724 | -0.175 | -1.91 | 0.015 | 0.25 | -0.236 | -1.03 |
| Local index | 2021-2022 | 554 | -0.181 | -1.66 | 0.008 | 0.12 | -0.092 | -0.36 |

## B. Quantile regressions

(i) Time series: basket next-week return (%) on F, F x S, S, controls (n = 138, ex-lockdown)

| tau | F calm | t | F x S | t |
|---|---:|---:|---:|---:|
| 0.1 | -2.544 | -5.19 | 6.338 | 4.51 |
| 0.25 | -1.918 | -3.41 | 2.958 | 2.34 |
| 0.5 | -1.114 | -1.88 | 4.021 | 2.70 |
| 0.75 | -0.245 | -0.38 | 2.393 | 1.76 |
| 0.9 | 0.062 | 0.09 | -2.726 | -1.78 |

(ii) Panel: USD ETF next-week return on F and e, country-year demeaned, week-block bootstrap SE (200 draws)

| tau | F | boot t | e | boot t |
|---|---:|---:|---:|---:|
| 0.1 | -0.051 | -0.25 | 0.128 | 1.99 |
| 0.25 | -0.152 | -1.11 | 0.025 | 0.87 |
| 0.5 | -0.184 | -1.48 | -0.000 | -0.00 |
| 0.75 | -0.196 | -1.55 | -0.047 | -1.54 |
| 0.9 | -0.203 | -1.58 | -0.025 | -0.61 |

## C. Robustness of the headline F x S (USD ETF, ex-lockdown, eq. 3)

### C1 alternative states

| state | n | F calm | t | F x S | t | share stress |
|---|---:|---:|---:|---:|---:|---:|
| S_vix20 | 1518 | 0.011 | 0.06 | -0.059 | -0.28 | 0.65 |
| S_vix25 | 1518 | -0.264 | -2.19 | 0.991 | 3.01 | 0.29 |
| S_terc | 1518 | -0.170 | -1.40 | 0.583 | 1.92 | 0.33 |
| S_vix30 | 1518 | -0.073 | -0.50 | -1.609 | -6.40 | 0.09 |
| S_emdd | 1518 | -0.046 | -0.24 | 0.057 | 0.23 | 0.30 |
| S_lvix | 1518 | -0.047 | -0.35 | 0.576 | 1.06 | 0.00 |

### C2 moving-block bootstrap (8-week blocks, 1000 draws): F x S = 0.991, boot SE 0.976, boot t 1.01, 95% CI [-0.002, 3.585], share > 0: 0.974

### C3 episode jackknife

| dropped episode | F x S | t |
|---|---:|---:|
| 2020-07-03..2020-07-24 (4 wks) | 0.859 | 2.53 |
| 2020-09-04..2020-10-30 (8 wks) | 0.970 | 4.50 |
| 2021-01-29..2021-01-29 (1 wks) | 1.001 | 3.08 |
| 2021-02-26..2021-02-26 (1 wks) | 0.962 | 2.52 |
| 2021-11-26..2021-12-03 (2 wks) | 0.992 | 3.01 |
| 2022-01-21..2022-03-11 (7 wks) | 0.993 | 2.57 |
| 2022-04-22..2022-07-01 (10 wks) | 1.308 | 1.73 |
| 2022-08-26..2022-10-28 (9 wks) | 0.861 | 3.04 |

### C4 country exclusion (factor recomputed without the dropped country)

| dropped | F x S | t |
|---|---:|---:|
| Brazil | 0.986 | 3.14 |
| Egypt | 1.038 | 3.03 |
| India | 0.898 | 2.87 |
| Indonesia | 1.165 | 3.08 |
| Malaysia | 1.016 | 3.69 |
| Mexico | 0.876 | 2.61 |
| Philippines | 0.898 | 2.84 |
| Poland | 0.893 | 2.87 |
| Saudi Arabia | 0.983 | 2.86 |
| South Africa | 0.951 | 2.97 |
| Thailand | 0.996 | 3.07 |
| Turkey | 0.966 | 2.91 |

### C5 placebos
- Circular block shift of the F series (500 draws, cross-section intact, clustered t): actual t = 3.01; placebo mean -0.06, SD 1.20, share >= actual 0.000
- F lagged 52 weeks, like-for-like sample (n = 946): actual F x S = 0.629 (t 3.22); placebo = 0.629 (t 2.19)

### C6 Google workplaces mobility common component (overlap window, n = 1331): correlation of Google and congestion factors 0.81; Google F x S = 0.153 (t 0.81), calm 0.032 (t 0.21); congestion in same window F x S = 1.003 (t 2.92)

## D. Basket timing rule on F (one position per week, equal-weight USD basket, ex-lockdown)

| portfolio | weeks | mean %/wk | SD % | t NW | Sharpe | max DD % | hit |
|---|---:|---:|---:|---:|---:|---:|---:|
| State rule, gross | 138 | 0.357 | 2.40 | 2.13 | 1.07 | -14.4 | 0.56 |
| State rule, net 10 bp one-way | 138 | 0.280 | 2.40 | 1.70 | 0.84 | -15.0 | 0.56 |
| State rule, net 25 bp one-way | 138 | 0.165 | 2.41 | 1.01 | 0.49 | -15.9 | 0.54 |
| Calm leg only | 138 | 0.269 | 1.81 | 2.01 | 1.07 | -12.1 | 0.38 |
| Stress leg only | 138 | 0.088 | 1.60 | 0.79 | 0.40 | -12.0 | 0.18 |
| Unconditional sign rule | 138 | -0.181 | 2.42 | -0.99 | -0.54 | -39.8 | 0.50 |
| Long-only basket | 138 | 0.148 | 2.43 | 0.74 | 0.44 | -21.8 | 0.53 |
| State rule, 2020 only | 26 | 0.251 | 2.98 | 0.57 | 0.61 | -13.1 | 0.58 |
| State rule, 2021 only | 53 | 0.351 | 2.11 | 1.36 | 1.20 | -9.6 | 0.53 |
| State rule, 2022 only | 52 | 0.257 | 2.48 | 1.03 | 0.75 | -11.5 | 0.54 |

Average weekly turnover (share of weeks with a position flip): 0.77; break-even one-way cost: 46 bp