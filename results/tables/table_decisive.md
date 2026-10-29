# Decisive re-estimation (raw signal, S = VIX>25, week-clustered t)


## ret_etf_f1, ex_lockdown

| spec | n | b calm | t | b inter | t | b stress |
|---|---:|---:|---:|---:|---:|---:|
| L1 country x month FE | 1518 | -0.107 | -2.90 | 0.307 | 3.26 | 0.200 |
| L2 + state x month FE | 1518 | -0.101 | -2.68 | 0.292 | 3.44 | 0.191 |
| L3 + year FE | 1518 | -0.101 | -2.63 | 0.291 | 3.35 | 0.189 |
| L4 country x year FE | 1518 | -0.104 | -2.63 | 0.297 | 3.35 | 0.193 |
| L5 + holiday dummies | 1518 | -0.065 | -1.87 | 0.243 | 2.94 | 0.178 |
| L6 + S x controls, log VIX | 1518 | -0.072 | -2.06 | 0.274 | 3.35 | 0.202 |
| L7 everything, Driscoll-Kraay(4) | 1518 | -0.072 | -2.48 | 0.274 | 4.00 | 0.202 |
| L8 common vs idiosyncratic (L6 FE) common | 1518 | -0.257 | -1.99 | 1.000 | 2.93 | 0.743 |
| L8 common vs idiosyncratic (L6 FE) idiosyncratic | 1518 | -0.042 | -1.35 | 0.124 | 1.96 | 0.083 |
| L9 within 2021 only | 583 | -0.004 | -0.09 | -0.181 | -1.22 | -0.185 |
| L9 within 2020H2 only | 286 | -0.139 | -1.89 | 0.218 | 1.32 | 0.078 |
| L9 within 2022 only | 572 | -0.124 | -2.00 | 0.315 | 3.45 | 0.192 |

## ret_etf_f1, post_2021-07

| spec | n | b calm | t | b inter | t | b stress |
|---|---:|---:|---:|---:|---:|---:|
| L1 country x month FE | 946 | -0.109 | -1.96 | 0.273 | 2.58 | 0.164 |
| L2 + state x month FE | 946 | -0.102 | -1.77 | 0.282 | 2.72 | 0.180 |
| L3 + year FE | 946 | -0.095 | -1.58 | 0.273 | 2.67 | 0.179 |
| L4 country x year FE | 946 | -0.104 | -1.78 | 0.273 | 2.55 | 0.169 |
| L5 + holiday dummies | 946 | -0.034 | -0.64 | 0.159 | 1.74 | 0.125 |
| L6 + S x controls, log VIX | 946 | -0.021 | -0.44 | 0.108 | 1.31 | 0.086 |
| L7 everything, Driscoll-Kraay(4) | 946 | -0.021 | -0.46 | 0.108 | 1.39 | 0.086 |
| L8 common vs idiosyncratic (L6 FE) common | 946 | -0.107 | -0.68 | 0.588 | 2.83 | 0.481 |
| L8 common vs idiosyncratic (L6 FE) idiosyncratic | 946 | -0.007 | -0.15 | 0.036 | 0.39 | 0.029 |
| L9 within 2021 only | 297 | 0.072 | 1.24 | -0.485 | -1.57 | -0.413 |
| L9 within 2022 only | 572 | -0.124 | -2.00 | 0.315 | 3.45 | 0.192 |

## ret_idx_f1, ex_lockdown

| spec | n | b calm | t | b inter | t | b stress |
|---|---:|---:|---:|---:|---:|---:|
| L1 country x month FE | 963 | -0.098 | -1.85 | 0.210 | 2.32 | 0.112 |
| L2 + state x month FE | 963 | -0.093 | -1.73 | 0.191 | 2.24 | 0.098 |
| L3 + year FE | 963 | -0.093 | -1.75 | 0.190 | 2.23 | 0.096 |
| L4 country x year FE | 963 | -0.097 | -1.82 | 0.192 | 2.18 | 0.094 |
| L5 + holiday dummies | 963 | -0.060 | -1.16 | 0.150 | 1.80 | 0.090 |
| L6 + S x controls, log VIX | 963 | -0.074 | -1.46 | 0.192 | 2.32 | 0.118 |
| L7 everything, Driscoll-Kraay(4) | 963 | -0.074 | -1.57 | 0.192 | 2.82 | 0.118 |
| L8 common vs idiosyncratic (L6 FE) common | 963 | -0.114 | -0.79 | 0.758 | 2.21 | 0.644 |
| L8 common vs idiosyncratic (L6 FE) idiosyncratic | 963 | -0.066 | -1.23 | 0.084 | 1.08 | 0.018 |
| L9 within 2021 only | 371 | -0.041 | -0.64 | -0.069 | -0.33 | -0.110 |
| L9 within 2020H2 only | 182 | -0.093 | -0.78 | 0.034 | 0.19 | -0.059 |
| L9 within 2022 only | 361 | -0.114 | -1.01 | 0.323 | 2.50 | 0.209 |

## ret_idx_f1, post_2021-07

| spec | n | b calm | t | b inter | t | b stress |
|---|---:|---:|---:|---:|---:|---:|
| L1 country x month FE | 599 | -0.111 | -1.80 | 0.241 | 2.25 | 0.130 |
| L2 + state x month FE | 599 | -0.112 | -1.79 | 0.263 | 2.47 | 0.151 |
| L3 + year FE | 599 | -0.106 | -1.68 | 0.258 | 2.44 | 0.152 |
| L4 country x year FE | 599 | -0.112 | -1.77 | 0.260 | 2.34 | 0.148 |
| L5 + holiday dummies | 599 | -0.050 | -0.64 | 0.189 | 1.67 | 0.139 |
| L6 + S x controls, log VIX | 599 | -0.044 | -0.58 | 0.179 | 1.54 | 0.136 |
| L7 everything, Driscoll-Kraay(4) | 599 | -0.044 | -0.51 | 0.179 | 1.75 | 0.136 |
| L8 common vs idiosyncratic (L6 FE) common | 599 | 0.084 | 0.47 | 0.541 | 2.28 | 0.626 |
| L8 common vs idiosyncratic (L6 FE) idiosyncratic | 599 | -0.070 | -0.78 | 0.154 | 1.22 | 0.085 |
| L9 within 2021 only | 189 | 0.055 | 0.71 | 0.183 | 0.36 | 0.238 |
| L9 within 2022 only | 361 | -0.114 | -1.01 | 0.323 | 2.50 | 0.209 |