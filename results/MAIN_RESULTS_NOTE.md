# Main results for the paper (2026-10-28)

Script: pipeline/10_main_tables.py. Outputs in results/tables and results/figures.
Headline specification: next-week return (SD units) on the deseasonalized congestion innovation
(country x month-of-year mean removed, standardized), its interaction with Stress = 1[VIX > 25],
the state dummy, own same-week return and global controls, country x calendar-month fixed
effects, standard errors clustered by week. Column (4) of Table 1.

## Table 1 (headline), ex-lockdown sample, 12 countries, 138 weeks

| | USD ETF next week | Local index next week |
|---|---:|---:|
| Congestion innovation, calm state | -0.101*** (0.035) | -0.094* (0.050) |
| Innovation x Stress | 0.257*** (0.086) | 0.184** (0.089) |
| Innovation in stress state (sum) | 0.156** (0.078) | 0.090 (0.076) |
| Observations | 1,518 | 963 |

Post-2021-07 sample: USD ETF interaction 0.218** (0.100), local index 0.175* (0.104).
Across the four specifications (raw or deseasonalized signal; country or country x month FE)
the USD-ETF interaction ranges 0.246-0.307 ex-lockdown, all significant at 1%; the local-index
interaction ranges 0.184-0.218, significant at 5%. Seasonality controls do not weaken it.

Economic size: a one-SD congestion innovation moves next-week USD returns by -0.10 SD in calm
weeks and +0.16 SD in stress weeks. With a weekly USD-ETF return SD of roughly 4%, that is about
-0.4% versus +0.6% per week, a swing of one percentage point between states.

## Figure 1 (VIX cutoff sweep)
The interaction is zero for cutoffs below 22, rises to a plateau of 0.20-0.26 for cutoffs
23-27, and falls (with wide intervals) above 28 where fewer than 10% of weeks qualify. The
result is therefore about a "risk-off" regime that covers roughly the top 30% of VIX weeks,
not about extreme crises only. This should be presented openly: it is a regime effect with a
threshold region, and the EM-drawdown state (step 09) is the cross-check.

## Figure 2
Calm-state response negative in all four target/sample combinations; stress-state response
positive, significant for the USD ETF, with wide intervals for the local index.

## Table 2 (seasonality-controlled volatility and quantiles)
- Next-week log realized variance of USD-ETF returns: -0.070** (t = -2.2) per SD of
  congestion innovation ex-lockdown; -0.083* (t = -1.7) post-2021. The state interaction is
  not significant: the volatility effect is unconditional. Local-index volatility: nothing.
- Quantile regressions (USD ETF, ex-lockdown): tau 0.10 +0.03 (ns), 0.50 -0.06**, 0.75
  -0.11***, 0.90 -0.09**. Local index: 0.75 -0.11***, 0.90 -0.11*. Congestion innovations
  compress the upper tail of next-week returns; the lower tail is unaffected once seasonality is
  controlled (the earlier positive lower-tail effect was partly seasonal).

## Table 3 (placebos under the headline specification)
| Placebo | USD ETF ex-lock | USD ETF post-21 | Index ex-lock | Index post-21 |
|---|---:|---:|---:|---:|
| Within-country shuffle, 500 draws: p-value | 0.000 | 0.002 | 0.012 | 0.034 |
| Signal lagged 52 weeks: interaction t | 1.49 | 1.35 | 2.03 | 1.54 |

The 52-week placebo is insignificant for the USD ETF in both samples; for the local index it
is borderline ex-lockdown (t = 2.0) with fewer observations. The USD-ETF result is the one to
lead with; the local index corroborates.

## What goes in the paper
1. Table 1 with all four columns, both targets, both samples (8 panels or a compact 4x4).
2. Figure 1 and Figure 2.
3. Table 2 as "distributional effects": lower volatility, compressed upside.
4. Table 3 placebos plus the block bootstrap and episode jackknife from step 09.
5. Alternative-state table from step 09 (VIX > 25, EM drawdown, local stress).
6. Google workplaces mobility replication (step 09).
7. Pooled-bridge nowcast result (step 05) as evidence that congestion carries macro information.

## Remaining caveats to write explicitly
- One 2022 episode supplies ~40% of the effect (jackknife).
- Local-index evidence is weaker and its 52-week placebo is borderline.
- 12 countries; results are about a global risk-off regime, not country-specific stress.
- The 2026 live-collector sample will provide the only true out-of-sample test; report it in
  the revision if available.

## Files
results/tables/table1_headline.csv, table1_headline.md, table2_volatility_quantile.csv,
table3_placebos.csv, table4_descriptives.csv; results/figures/fig1_vix_threshold_sweep.png,
fig2_state_betas.png
