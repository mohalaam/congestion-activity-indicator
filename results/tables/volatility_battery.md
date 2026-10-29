# Volatility battery (next-week log realized variance)

| spec | n | coefficient(s) | t |
|---|---:|---|---|
| B1 baseline, signed x | 1507 | x_raw: -0.075 | -2.61 |
| B2 + holiday dummies | 1507 | x_raw: -0.065 | -2.27 |
| B3 per-trading-day variance + holidays | 1507 | x_raw: -0.065 | -2.25 |
| B4 Driscoll-Kraay(4), B2 spec | 1507 | x_raw: -0.065 | -2.60 |
| B5 moving-block bootstrap (8 wk, 500 draws), B2 spec | 1507 | x_raw: -0.065; boot SE 0.024; 95% CI [-0.104, -0.013] | -2.70 |
| B6 |x| (resolution of uncertainty) | 1507 | abs_x: 0.055 | 1.27 |
| B7 x+ and x- separately | 1507 | x_pos: -0.031; x_neg: -0.087 | -0.56; -1.83 |
| B8 within 2020 H2 (country + month FE) | 286 | x_raw: -0.081 | -1.51 |
| B8 within 2021 (country + month FE) | 583 | x_raw: -0.029 | -0.73 |
| B8 within 2022 (country + month FE) | 572 | x_raw: -0.019 | -0.37 |
| B9 circular block shift placebo (300) | | actual t -2.27; placebo mean 0.02, SD 1.08 | share <= actual 0.010 |
| B10 local index target, B2 spec | 724 | x_raw: -0.047 | -0.79 |
| B11 factor F and residual e, B2 spec | 1507 | F: -0.130; e: -0.054 | -1.11; -1.94 |
| B12 52-week lag placebo, B2 spec | 1087 | x52: 0.025 | 0.88 |
| B12 real-time seasonal difference, B2 spec | 1087 | x_sd: -0.053 | -1.84 |

B13 economic size: R2 0.422 without x vs 0.424 with x (increment 0.0021); SD of next-week log RV 1.08; a 1-SD x moves it by -0.065 log points = -6.3% of variance, -3.2% of volatility.