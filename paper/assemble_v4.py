# Assemble MANUSCRIPT_v4.md from MANUSCRIPT_v3.md with the round-2 text changes and numbered tables.
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
v3 = open(os.path.join(HERE, "MANUSCRIPT_v3.md"), encoding="utf-8").read()
tables = open(os.path.join(HERE, "TABLES_v4.md"), encoding="utf-8").read()
fails = []
def rep(old, new, count=1):
    global v3
    if old not in v3:
        fails.append(old[:70]); return
    v3 = v3.replace(old, new, count)

# ---- title, header
rep("# Urban congestion as a real-time activity indicator for emerging markets: measurement, validation, and a seasonal placebo for mobility-based return predictability",
    "# A seasonal placebo for mobility-based return predictability: urban congestion in twelve emerging markets")
rep("Draft v3, 2026-10-28. Data-and-methods framing. Every number is from results/tables or the\nnotes listed in README.md; items in square brackets remain to be verified or produced.",
    "Draft v4, 2026-10-28. Submission-form draft: tables at the end, figures as separate files.")

# ---- abstract (about 150 words)
old_abs = v3[v3.index("## Abstract"):v3.index("## 1. Introduction")]
new_abs = """## Abstract

Daily urban congestion indices now cover the largest cities of every major emerging market and
are being used as real-time activity indicators and as return predictors. We assemble a panel
for 49 cities in 12 emerging markets (2020-2023), show that its weekly innovations track Google
workplaces mobility (correlation 0.72 outside the lockdown) and modestly improve pooled
production nowcasts, and then show how easily such a series generates spurious conditional
predictability. Congestion innovations carry a country-specific annual component that survives
weekday adjustment, differencing and calendar fixed effects. A regression of next-week
emerging-market returns on congestion innovations interacted with a VIX stress indicator yields
a sign switch with a t-statistic of 3.7 that is carried predominantly by each country's own
annual pattern coinciding with the risk-off weeks of 2022; a decomposition and placebo battery
shows this, while lag and seasonal-difference placebos are underpowered on three years. What
survives is a small, signed effect of bad activity news on next-week variance. The 2022 pattern
is recorded as a pre-registered hypothesis for a live sample.

"""
v3 = v3.replace(old_abs, new_abs)

# ---- introduction fixes
rep("reduces out-of-sample error by 14 percent, with a Diebold-Mariano p-value of 0.08 and a\ngain concentrated in disruptions;",
    "reduces out-of-sample error by 14 percent, a gain that is concentrated in disruptions and not\nstatistically secure on 21 evaluation months (Diebold-Mariano p = 0.19);")
rep("They look like noise but are not: the\nmean of the series by week of the year explains 55 percent of their variance at the city and\ncountry level and 67 percent of the variance of the cross-country factor, and their\nautocorrelation at a lag of 52 weeks is 0.3 to 0.6.",
    "They look like noise but are not: their\nautocorrelation at a lag of 52 weeks is 0.31 at the country level and 0.56 for the cross-country\nfactor, and a smooth annual seasonal is significant in about half the countries.")
rep("The same\nregression with the innovation lagged by exactly 52 weeks, a series that cannot contain news\nabout next week, gives a coefficient of 0.08 with a t-statistic of 1.2 on the same sample, and\nthe actual signal on that sample gives 0.19 with t of 2.6; with a real-time seasonal difference\nof the signal, the innovation minus its value 52 weeks earlier, the interaction is 0.05 with a\nt-statistic of 0.7. The result was a calendar pattern in congestion coinciding with the calendar\nclustering of the 2022 risk-off weeks.",
    "The same\nregression with the innovation lagged by exactly 52 weeks, a series that cannot contain news\nabout next week, gives a coefficient of 0.08 with a t-statistic of 1.2 on the same sample, and\nthe actual signal on that sample gives 0.19 with t of 2.6; with a real-time seasonal difference\nof the signal the interaction is 0.05 with a t-statistic of 0.7. These comparisons are\nsuggestive, and we show by simulation that on three years they are not decisive. What is\ndecisive is a decomposition that holds the calendar fixed: each country's own in-sample\nweek-of-year profile, with no week-to-week news in it, reproduces most of the interaction;\nanother country's profile reproduces none; a circular shift of the panel that breaks the\nalignment between calendar and stress weeks removes it; and the non-seasonal residual retains a\nmarginal effect. The result was predominantly a calendar pattern in congestion coinciding with\nthe calendar clustering of the 2022 risk-off weeks.")
rep("The unconditional claims of the single-city literature\nfare no better: in country-by-country regressions of next-week index returns on the country's\ncongestion innovation, no country is significant at the 5 percent level in any of the three\nversions,",
    "The unconditional relations reported in the single-city literature\nare not found here: in country-by-country regressions of next-week index returns on the\ncountry's congestion innovation, no country is significant at the 5 percent level in any of the\nthree versions,")
rep("Not everything disappears. Congestion innovations predict lower next-week realized variance of\nUS-dollar emerging-market returns, with a coefficient of -0.075 log points per standard\ndeviation (t = -2.6) that is absent for the 52-week-lagged placebo (t = 0.4) and survives the\nreal-time seasonal difference (-0.06, t = -2.2). Resolution of uncertainty about activity is\npriced as lower volatility, which is consistent with the information content documented in the\nvalidation exercise and does not require a directional bet. Finally, within 2022 the\nstate-dependent pattern remains after seasonal differencing (interaction 2.7 percent per\nstandard deviation of the factor, t = 2.2, 52 weeks).",
    "Not everything disappears. Congestion innovations predict lower next-week realized variance of\nUS-dollar emerging-market returns, with a coefficient of -0.065 log points per standard\ndeviation (t = -2.3 clustered, -2.7 by block bootstrap) that is absent for the 52-week-lagged\nplacebo, passes a circular-shift placebo, and comes from negative innovations: bad activity\nnews raises next-week variance. The effect is small, about three percent of weekly volatility\nper standard deviation, and is not detectable within any single year. Finally, within 2022 the\nstate-dependent pattern remains after seasonal differencing and with lockdown-stringency and\nfuel-price controls (interaction 1.7 percent per standard deviation of the factor, t = 2.3, 52\nweeks).")
rep("First, it provides the first multi-country, validated\ndaily congestion panel for emerging-market research",
    "First, it provides, to our knowledge, the first multi-country daily congestion panel for\nemerging-market research, compared against independent activity measures,")
rep("Third, it reports what does survive:\na modest nowcasting gain concentrated in disruptions and a robust volatility effect.",
    "Third, it reports what does survive:\na modest nowcasting gain concentrated in disruptions and a small, signed volatility effect.")
rep("The paper\nis related to the literature on alternative data and asset prices (Froot, Kang, Ozik and Sadka,\n2017; Zhu, 2019; Katona, Painter, Patatoukas and Zeng, 2024), to the Google-attention strand in\nthis journal (Duz Tan and Tas, 2019), and to the state-dependent pricing of macroeconomic news\n(Boyd, Hu and Jagannathan, 2005; McQueen and Roley, 1993), whose prediction our exploratory\nresult appeared to confirm and whose test we now defer to the pre-registered sample.",
    """The paper
belongs to three literatures. The first is the literature on spurious and seasonal
predictability: Novy-Marx (2014) shows that weather, sunspots and planetary positions "predict"
anomaly returns in short samples; Heston and Sadka (2008) and Keloharju, Linnainmaa and Nyberg
(2016) document annual seasonality in returns themselves; Stambaugh (1999) and Ferson,
Sarkissian and Simin (2003) show how persistent regressors produce spurious predictability;
Harvey, Liu and Zhu (2016) and Harvey (2017) set the multiple-testing hurdles that a searched
result must clear; and Hirshleifer, Jiang and DiGiovanni (2020) show that mood proxies inherit
return seasonality, which bears directly on the investor-mood reading of the single-city
congestion studies. Holiday effects in the markets we study are documented by Bialkowski,
Etebari and Wisniewski (2012) for Ramadan and by Seyyed, Abraham and Al-Hajji (2005) for Saudi
Arabia, which is why moving-holiday dummies are part of every specification. The second is the
literature on alternative data: the Google Flu Trends episode (Lazer, Kennedy, King and
Vespignani, 2014) is the closest precedent for a high-frequency proxy that tracked its target
until a structural change and a seasonal confound broke it, and the finance strand (Froot, Kang,
Ozik and Sadka, 2017; Zhu, 2019; Katona, Painter, Patatoukas and Zeng, 2024; Duz Tan and Tas,
2019, in this journal) has not generally applied seasonal placebos. The third is the
nowcasting strand (Sampi and Jooste, 2020; Woloszko, 2024), where central-bank uses of mobility
data during the pandemic mostly worked with year-on-year or versus-2019 baselines, an implicit
seasonal difference that the finance applications dropped. The state-dependent pricing of
macroeconomic news (Boyd, Hu and Jagannathan, 2005; McQueen and Roley, 1993) is the prediction
our exploratory result appeared to confirm and whose test we defer to the pre-registered sample.""")
rep("For readers of this journal the\nTurkish case is instructive rather than confirmatory: Turkey has the deepest city coverage in\nour panel, ten cities, yet its country-specific response is not significant and goes the other\nway, which is consistent with a market whose policy regime in 2021-2022 did not follow the\npattern of its peers; we return to this in Section 3.5.",
    "For readers of this journal the\nTurkish case is instructive rather than confirmatory, and Section 3.6 reports it separately.")

# ---- Section 2.5 self-reference
rep("This is the most demanding specification a referee asked us for in an earlier version of this work, and it is\nthe one in which the seasonal placebo still bites.",
    "Country-by-year effects absorb any year contrast; state-by-month effects absorb any tendency of\nstress weeks to fall in particular months; the holiday dummies handle moving holidays that\nneither absorbs; and the interacted controls prevent the interaction from loading on global\nfactors that co-move with congestion in stress weeks. Table 6, Panel A reports the ladder from\ncountry-by-month effects alone to this specification. We also add, as a check on non-seasonal\nconfounders, the weekly change in the Oxford stringency index and the lagged weekly change in\nthe local-currency oil price (log Brent plus log local currency per dollar), a proxy for retail\nfuel prices, each interacted with the state.")
# ---- new Section 2.6 specification search
rep("## 3. Results\n",
    """### 2.6 What we tried

Because this paper reports a result that we first believed and then rejected, we list the
exploratory path. The project began as a test of whether congestion innovations predict
emerging-market returns. We estimated, in this order: unconditional weekly and monthly
predictive panels for index, fund and currency returns at one-, four- and twelve-week horizons;
a cross-country sort; monthly regressions on an intra-month congestion slope and on a nowcast
surprise; volatility and quantile regressions; and then the VIX interaction, first with a cutoff
of 25 and subsequently with cutoffs of 20 and 30, a continuous VIX, an emerging-market
drawdown, and country-specific stress measures. Four-week and currency interactions were
significant with the raw signal and were dropped when they failed the seasonal placebo; the
monthly slope, nowcast-surprise and sort results were never placebo-tested and are not reported;
a currency-volatility result was dropped for the same reason. Across roughly 150 return
specifications and 40 volatility specifications, the interaction reported in Table 6 and the
volatility coefficient in Table 7 are the two that we examined most closely, which is why the
first is subjected to the placebo battery of Section 3.3 and the second to that of Section 3.4,
and why the surviving 2022 pattern is treated as a hypothesis rather than a finding.

## 3. Results
""")
# ---- 3.1 numbers
rep("between 0.43 (Philippines) and 0.48 (Saudi Arabia) to 0.85-0.89 (Brazil, South Africa, Poland, Egypt,\nTurkey) outside the lockdown.",
    "between 0.43 (Philippines) and 0.48 (Saudi Arabia) to 0.82-0.89 (Turkey, Egypt, South Africa,\nPoland, Brazil) outside the lockdown.")
rep("Congestion measures what location data measure, and continues to do so after Google's series\nended.",
    "Congestion measures what location data measure, and continues to do so after Google's series\nended. Both are built from smartphone and probe-device locations, so the agreement is between\ntwo readings of the same underlying behaviour rather than a validation against output; the\nindependent target is industrial production, to which we turn next.")
rep("The gain is therefore real in magnitude but not statistically secure on 21 to 25\nevaluation months.", "The gain is therefore real in magnitude but not statistically secure on 21 and 19\nevaluation months.")
rep("so that the effective sample is the 21 to 25 evaluation months", "so that the effective sample is the 21 and 19 evaluation months")
# ---- 3.3 wording
rep("The unconditional congestion-return relation reported for Bangkok and Kuala\nLumpur in earlier work is not present in a twelve-country panel that includes Thailand and\nMalaysia.",
    "The unconditional congestion-return relation reported for Bangkok and Kuala\nLumpur in earlier work, at daily frequency on other providers' indices, is not found at weekly\nfrequency in a twelve-country panel; Malaysia is among the seven local-index countries and\nThailand among the eleven fund countries. The daily designs of those studies are exposed to\nday-of-year structure in the same way, and none ran a placebo of the kind we propose.")
rep("Table 6 reports the worked example, specification (1), for next-week US-dollar fund returns in\nthe ex-lockdown sample. With the actual signal the calm-state coefficient is -0.054 (t = -1.8)\nand the interaction 0.259 (t = 3.7):",
    "Table 6 reports the worked example for next-week US-dollar fund returns in the ex-lockdown\nsample. Panel A shows that the interaction is 0.31 (t = 3.3) with country-by-month effects\nalone and remains between 0.24 and 0.30 (t = 2.9 to 4.0, the last with Driscoll-Kraay errors)\nas state-by-month effects, year and country-by-year effects, holiday dummies, state-interacted\ncontrols and the log VIX level are added; fixed effects do not remove it. In specification (1)\nthe calm-state coefficient is -0.054 (t = -1.8) and the interaction 0.259 (t = 3.7), 0.273 (t =\n3.8) with the stringency and fuel controls:")
# ---- 3.5 bracket, collector disclosure
rep("Appendix Table\nA4). The same regression", "Appendix Table\nA4 and Table 8). The same regression")
rep("which we have\ncollected for all 490 cities since October 2026 (Appendix B, with a time-stamped deposit).",
    """which we have
collected for all 490 cities since 21 October 2026 (Appendix B; the pre-registration will be
deposited with a time stamp before submission). The collector is a script that requests each
city's public seven-day feed twice daily, identifies itself with a standard browser user-agent
string, and stores the hourly values; it runs on a single machine under a scheduler, so that a
gap of more than seven days loses data irrecoverably, and Figure 4 reports its coverage. We are
seeking the provider's written confirmation that automated collection of the public feed for
research is within its terms, and we will not rely on the live sample without it.""")
# ---- 3.6 "free"
rep("congestion is\na free, daily, validated indicator of large movements in activity,", "congestion is\na daily indicator of large movements in activity that tracks independent mobility measures,")
# ---- Turkey paragraph as 3.6 (rename old 3.6 to 3.7)
rep("### 3.6 Implications", """### 3.6 The Turkish case

Turkey has the deepest coverage in the panel, ten cities, and its congestion innovations track
Google workplaces mobility at 0.82 outside the lockdown. It is also the clearest example of the
moving-holiday problem: its 52-week autocorrelation is 0.01 and a three-harmonic seasonal
explains six percent of variance (p = 0.21), so no seasonal filter finds annual structure, yet
Ramadan and the two Eids shift Istanbul traffic by more than any ordinary week's news and are
absorbed only by the explicit holiday dummies. In the country-by-country regressions of Table 5
the Turkish coefficients are negative and insignificant with every signal version (local index
-0.39, t = -1.3; fund -0.44, t = -1.1). In the state-dependent specification estimated for
Turkey alone the interaction is -0.28 (t = -1.4), the opposite sign to the pooled estimate,
and the Turkish volatility coefficient is 0.13 (t = 1.1), also the opposite sign. The pooled
results of this paper are therefore not Turkish results, and a reader interested in the
Istanbul market should take from this paper the diagnostics rather than the point estimates;
the 2021-2022 period, in which Turkish monetary policy and the lira followed a path unlike any
other market in the sample, is a natural case for the country-specific analysis that a longer
live sample will allow.

### 3.7 Implications""")
# ---- conclusion
rep("shown that its strong annual seasonality\nproduces spurious return-predictability results, including a textbook-looking state-dependent\nsign switch with a t-statistic of 3.7 that a 52-week-lagged copy of the signal reproduces and a\nreal-time seasonal difference eliminates. The unconditional claims of the earlier single-city\nliterature do not replicate. The volatility effect of congestion innovations survives both\ndiagnostics.",
    "shown that its country-specific annual structure\nproduces spurious conditional predictability, including a textbook-looking state-dependent\nsign switch with a t-statistic of 3.7 that each country's own calendar profile reproduces,\nanother country's does not, and a circular shift of the panel removes, while the lag and\nseasonal-difference placebos that a short sample allows are informative but underpowered. The\nunconditional relations of the earlier single-city literature are not found here. A small,\nsigned effect of bad activity news on next-week variance survives every diagnostic.")
# ---- figures cited
rep("### 3.1 Validation\n", "### 3.1 Validation\n\nFigure 1 plots the weekly congestion level for the 12 countries with the lockdown months and\nthe VIX-above-25 weeks shaded; the lockdown collapse, the recovery, and the recurring holiday\ndips that motivate Section 2.3 are visible in every panel.\n")
# ---- appendix + tables
old_app = v3[v3.index("## Appendix"):v3.index("## References")]
new_app = """## Tables

""" + tables + """

## Figures

Figure 1. Weekly congestion level, 12 emerging markets, 2020-2023 (results/figures/fig1_congestion_series.png).
Figure 2. Week-of-year profile of congestion and Google workplaces innovations (fig2_seasonal_profile.png).
Figure 3. State-dependent response under the three signal versions (fig3_three_versions.png).
Figure 4. Live-feed collector coverage since 21 October 2026 (fig4_collector_coverage.png).

## Appendix

A1 City list, population weights, coverage: results/tables/appendix_A1_cities.csv.
A2 Moving-holiday calendar: results/tables/appendix_A2_holidays.csv.
A3 Nowcast gain by country, both training variants: results/tables/appendix_A3_nowcast_bycountry.csv.
A4 Basket time-series regressions under the three signal versions: results/tables/appendix_A4_2022_timeseries.md and fuel_stringency.md.
A5 Weighting and inclusion robustness: results/tables/appendix_A5_weights_inclusion.md. With equal city weights, the largest city only, or Taiwan, the UAE and Greece added, the Table 6 interaction is 0.21-0.28 (t 3.5-4.3) on the actual signal and 0.04-0.07 (t 0.6-0.9) on the seasonally differenced signal; the volatility coefficient is -0.06 to -0.08 (t -2.5 to -2.6); in single-city countries alone it is -0.05 (t -1.2).
A6 Simulation of placebo attenuation under a news-only null: results/tables/round2_stats.md, Section 2.
B Pre-registration: paper/PREREGISTRATION.md.

"""
v3 = v3.replace(old_app, new_app)
# ---- references
old_ref = v3[v3.index("## References"):]
new_ref = """## References

Bialkowski, J., Etebari, A., Wisniewski, T. P. (2012). Fast profits: Investor sentiment and stock returns during Ramadan. Journal of Banking and Finance, 36(3), 835-845.
Beyer, R. C. M., Franco-Bedoya, S., Galdo, V. (2021). Examining the economic impact of COVID-19 in India through daily electricity consumption and nighttime light intensity. World Development, 140, 105287.
Boyd, J. H., Hu, J., Jagannathan, R. (2005). The stock market's reaction to unemployment news: Why bad news is usually good for stocks. Journal of Finance, 60(2), 649-672.
Cao, Z., Qian, Y., Zhang, B. (2024). The price of the slow lane: Traffic congestion and stock block trading premium. International Review of Finance, 24(1), 30-52.
Duz Tan, S., Tas, O. (2019). Investor attention and stock returns: Evidence from Borsa Istanbul. Borsa Istanbul Review, 19(2), 106-116.
Eraslan, S., Gotz, T. (2020). An unconventional weekly economic activity index for Germany. Deutsche Bundesbank Technical Paper 02/2020.
Ferson, W. E., Sarkissian, S., Simin, T. T. (2003). Spurious regressions in financial economics? Journal of Finance, 58(4), 1393-1413.
Froot, K., Kang, N., Ozik, G., Sadka, R. (2017). What do measures of real-time corporate sales say about earnings surprises and post-announcement returns? Journal of Financial Economics, 125(1), 143-162.
Gamtkitsulashvili, T., Plekhanov, A. (2023). Mobility and economic activity around the world during the Covid-19 crisis. Applied Economics Letters, 30(5), 608-614.
Harvey, C. R. (2017). Presidential address: The scientific outlook in financial economics. Journal of Finance, 72(4), 1399-1440.
Harvey, C. R., Liu, Y., Zhu, H. (2016). ... and the cross-section of expected returns. Review of Financial Studies, 29(1), 5-68.
Heston, S. L., Sadka, R. (2008). Seasonality in the cross-section of stock returns. Journal of Financial Economics, 87(2), 418-445.
Hirshleifer, D., Jiang, D., DiGiovanni, Y. M. (2020). Mood beta and seasonalities in stock returns. Journal of Financial Economics, 137(1), 272-295.
Katona, Z., Painter, M., Patatoukas, P. N., Zeng, J. (2024). On the capital market consequences of big data: Evidence from outer space. Journal of Financial and Quantitative Analysis, forthcoming. [verify volume and pages]
Keloharju, M., Linnainmaa, J. T., Nyberg, P. (2016). Return seasonalities. Journal of Finance, 71(4), 1557-1590.
Khanthavit, A. (2021). Bangkok traffic congestion, stressed investors, and Thai stock-market returns. ABAC Journal, 41(4), 1-23.
Khanthavit, A. (2022). The relationship between traffic congestion and stock market returns. ABAC Journal, 42(1), 1-15. [verify pages]
Lazer, D., Kennedy, R., King, G., Vespignani, A. (2014). The parable of Google Flu: Traps in big data analysis. Science, 343(6176), 1203-1205.
Lewis, D. J., Mertens, K., Stock, J. H., Trivedi, M. (2022). Measuring real activity using a weekly economic index. Journal of Applied Econometrics, 37(4), 667-687.
McQueen, G., Roley, V. V. (1993). Stock prices, news, and business conditions. Review of Financial Studies, 6(3), 683-707.
Novy-Marx, R. (2014). Predicting anomaly performance with politics, the weather, global warming, sunspots, and the stars. Journal of Financial Economics, 112(2), 137-146.
Sampi, J., Jooste, C. (2020). Nowcasting economic activity in times of COVID-19: An approximation from the Google Community Mobility Report. World Bank Policy Research Working Paper 9247.
Seyyed, F. J., Abraham, A., Al-Hajji, M. (2005). Seasonality in stock returns and volatility: The Ramadan effect. Research in International Business and Finance, 19(3), 374-383.
Stambaugh, R. F. (1999). Predictive regressions. Journal of Financial Economics, 54(3), 375-421.
Tang, T. C. (2008). Do vehicles on highways help to predict the Malaysian stock market? IUP Journal of Applied Economics, 7(2), 25-30. [verify]
Thaker, H. M. T. (2022). COVID-19, mobility and stock markets performance: Evidence from ASEAN-5. Asian Economics Letters, 3(4). [verify article number]
Woloszko, N. (2024). Tracking activity in real time with Google Trends. International Journal of Forecasting, forthcoming. [verify; OECD Economics Department Working Paper 1634, 2020]
Zhu, C. (2019). Big data as a governance mechanism. Review of Financial Studies, 32(5), 2021-2061.

Data: ActiveConclusion, COVID19_mobility repository (GitHub), file tomtom_reports/tomtom_trafic_index.csv, archived daily TomTom Traffic Index values, 2019-12-30 to 2023-02-14 (data remain the property of TomTom International BV). Google LLC, COVID-19 Community Mobility Reports. World Bank Global Economic Monitor; IMF International Financial Statistics (via DBnomics). Hale, T., et al. (2021), Oxford COVID-19 Government Response Tracker, Nature Human Behaviour, 5, 529-538.
"""
v3 = v3.replace(old_ref, new_ref)
open(os.path.join(HERE, "MANUSCRIPT_v4.md"), "w", encoding="utf-8").write(v3)
body = v3[:v3.index("## Tables")]
print("words (body, before tables):", len(re.findall(r"\w+", body)), "| total:", len(re.findall(r"\w+", v3)))
print("abstract words:", len(re.findall(r"\w+", v3[v3.index("## Abstract") + 11:v3.index("## 1. Introduction")])))
print("FAILED replacements:", fails if fails else "none")
print("leftover brackets:", re.findall(r"\[[^\]]{0,60}\]", body)[:10])
