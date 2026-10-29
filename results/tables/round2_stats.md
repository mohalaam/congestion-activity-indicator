# Round-2 statistics

## 1. Seasonality diagnostics on a true weekly time index (lockdown weeks NaN)

| level | n series | mean n | R2 woy (in-sample) | adj R2 | LOYO R2 | Fourier-3 R2 | share F p<0.05 | share HAC-Wald p<0.05 | mean ac(52) | share ac(52)>0.2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| city | 49 | 138 | 0.55 | 0.28 | -0.30 | 0.09 | 0.39 | 0.51 | 0.35 | 0.65 |
| country | 12 | 138 | 0.55 | 0.27 | -0.30 | 0.10 | 0.42 | 0.42 | 0.31 | 0.58 |
| factor | 1 | 138 | 0.67 | 0.47 | 0.08 | 0.13 | 1.00 | 1.00 | 0.56 | 1.00 |
| google_country | 12 | 121 | 0.57 | 0.24 | -0.48 | 0.07 | 0.25 | 0.25 | 0.33 | 0.50 |
| google_factor | 1 | 121 | 0.61 | 0.30 | -0.34 | 0.08 | 0.00 | 0.00 | 0.39 | 1.00 |

Country detail: Brazil: adj 0.48, LOYO -0.03, Fourier 0.06 (p 0.274), ac52 0.68; Egypt: adj 0.08, LOYO -0.44, Fourier 0.09 (p 0.042), ac52 0.14; India: adj 0.13, LOYO -0.77, Fourier 0.26 (p 0.000), ac52 0.08; Indonesia: adj -0.02, LOYO -0.74, Fourier 0.09 (p 0.050), ac52 -0.06; Malaysia: adj -0.03, LOYO -0.65, Fourier 0.16 (p 0.001), ac52 -0.07; Mexico: adj 0.48, LOYO 0.08, Fourier 0.11 (p 0.013), ac52 0.57; Philippines: adj 0.21, LOYO -0.21, Fourier 0.06 (p 0.178), ac52 0.40; Poland: adj 0.45, LOYO -0.03, Fourier 0.07 (p 0.126), ac52 0.59; Saudi Arabia: adj 0.26, LOYO -0.42, Fourier 0.05 (p 0.393), ac52 0.24; South Africa: adj 0.67, LOYO 0.42, Fourier 0.15 (p 0.001), ac52 0.74; Thailand: adj 0.51, LOYO 0.03, Fourier 0.08 (p 0.098), ac52 0.46; Turkey: adj 0.00, LOYO -0.79, Fourier 0.06 (p 0.205), ac52 0.01

Chance level of in-sample R2 with k cells on n obs: about (k-1)/(n-1) = 0.37 for n=138.

## 2. Attenuation bound (placebo-sample, n = 946)

Observed: actual x (calm -0.019, inter 0.157, t 2.03); lag-52 placebo (inter 0.109, t 1.77); seasonal diff (inter -0.009, t -0.18). Observed ratios: placebo/actual = 0.69, seasonal-diff/actual = -0.06.

H_news (y responds to actual x): expected placebo/actual = 0.12 [5-95%: -1.50, 1.70]; expected seasonal-diff/actual = 0.33 [-0.87, 1.56]; median t placebo 0.17, median t seasonal-diff 0.69; share of sims with seasonal-diff ratio <= observed -0.06: 0.210

H_seasonal (y responds to seasonal component of x only): expected placebo/actual = 0.19 [5-95%: -2.51, 2.86]; expected seasonal-diff/actual = 0.28 [-1.90, 2.35]; median t placebo 0.41, median t seasonal-diff 0.44; share of sims with seasonal-diff ratio <= observed -0.06: 0.267

## 3. Calendar-preserving and persistence-preserving placebos (full ex-lockdown sample)

| placebo | n | calm | t | inter | t |
|---|---:|---:|---:|---:|---:|
| actual x | 1518 | -0.054 | -1.83 | 0.259 | 3.69 |
| own in-sample week-of-year profile (pure seasonal) | 1617 | -0.041 | -1.64 | 0.156 | 2.86 |
| another country's week-of-year profile (rotated) | 1617 | -0.001 | -0.03 | 0.007 | 0.13 |
| x minus own in-sample profile (in-sample deseasonalized) | 1518 | -0.024 | -0.94 | 0.102 | 2.00 |

Circular block shift of the whole country panel (300 draws, calendar broken, persistence and cross-section kept): actual t 3.69; placebo mean 0.18, SD 1.02, share >= actual 0.000

## 4. The 2022 anchor, one standardization (SD of F - F_52 over the ex-lockdown sample = 0.754)

| version | sample | n | F calm | t | F x S | t |
|---|---|---:|---:|---:|---:|---:|
| seasonal diff, standardized (carry this) | 2022 | 52 | -0.87 | -1.14 | 2.02 | 2.23 |
| seasonal diff, standardized (carry this) | ex-lockdown | 100 | 0.03 | 0.25 | 0.66 | 1.22 |
| seasonal diff, standardized (carry this) | 2021 | 41 | 0.14 | 1.36 | -1.27 | -0.37 |
| seasonal diff, standardized (carry this) + holiday shares | 2022 | 52 | -0.63 | -0.84 | 2.00 | 2.44 |
| seasonal diff, standardized (carry this) + holiday shares | ex-lockdown | 100 | -0.06 | -0.39 | 0.98 | 2.19 |
| seasonal diff, standardized (carry this) + holiday shares | 2021 | 41 | 0.01 | 0.05 | -1.26 | -0.35 |
| seasonal diff, unstandardized (note's 2.68) | 2022 | 52 | -1.15 | -1.14 | 2.68 | 2.23 |
| seasonal diff, unstandardized (note's 2.68) | ex-lockdown | 100 | 0.04 | 0.25 | 0.88 | 1.22 |
| seasonal diff, unstandardized (note's 2.68) | 2021 | 41 | 0.19 | 1.36 | -1.69 | -0.37 |
| seasonal diff, unstandardized (note's 2.68) + holiday shares | 2022 | 52 | -0.84 | -0.84 | 2.65 | 2.44 |
| seasonal diff, unstandardized (note's 2.68) + holiday shares | ex-lockdown | 100 | -0.08 | -0.39 | 1.31 | 2.19 |
| seasonal diff, unstandardized (note's 2.68) + holiday shares | 2021 | 41 | 0.01 | 0.05 | -1.67 | -0.35 |