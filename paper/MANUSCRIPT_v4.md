# A seasonal placebo for mobility-based return predictability: urban congestion in twelve emerging markets



JEL: C53, E32, G14, G15, R41
Keywords: alternative data; urban congestion; nowcasting; emerging markets; seasonality; placebo tests

## Abstract

Daily urban congestion indices cover the largest cities of every major emerging market and are
used as real-time activity indicators and return predictors. We assemble a panel for 49 cities
in 12 emerging markets (2020-2023), show that its weekly innovations track Google workplaces
mobility (correlation 0.72 outside the lockdown) and modestly improve pooled production
nowcasts, and then show how easily such a series generates spurious conditional predictability.
Congestion innovations carry a country-specific annual component that survives weekday
adjustment, differencing and calendar fixed effects. Next-week emerging-market returns regressed
on congestion innovations interacted with a VIX stress indicator show a sign switch with a
t-statistic of 3.7 that each country's own annual profile reproduces, another country's does
not, and a circular shift of the panel removes. What survives is a small, signed effect of bad
activity news on next-week variance. The 2022 pattern is recorded as a hypothesis we pre-register (Appendix B).

## 1. Introduction

Investors and policymakers in emerging markets face the longest lags between economic activity
and its measurement. Industrial production and retail sales arrive five to eight weeks after the
month they describe and are revised; survey indicators are monthly and cover only some
markets. Since 2019 a navigation-data provider has published, for several hundred cities, a daily
index of road congestion that is a physical footprint of commuting, deliveries and shopping
trips, available with no lag. Central banks and international institutions adopted mobility,
electricity, truck-toll and flight data as high-frequency activity indicators during the
pandemic (Eraslan & Götz, 2020; Lewis, Mertens, Stock & Trivedi, 2022; Sampi and Jooste,
2020; Woloszko, 2024; Beyer, Franco-Bedoya & Galdo, 2021), and a small finance literature has
used city congestion to predict stock returns, reading a negative coefficient as commuter stress
affecting investor mood (Khanthavit, 2021, 2022), finding Granger causality from highway counts
to prices (Tang, 2008), or documenting a trading-friction channel (Cao, Qian & Zhang, 2024).
This paper asks two questions about such data that the literature has not answered: how good a
measure of real activity is a daily congestion index in emerging markets, and what can go wrong
when it is used to predict returns.

We assemble, from an archived copy of the provider's public daily series, a panel of 49 cities
in 12 emerging markets, Turkey, Poland, Brazil, South Africa, India, Saudi Arabia, Mexico,
Indonesia, Thailand, Egypt, Malaysia and the Philippines, from 30 December 2019 to 14 February
2023, and aggregate it to population-weighted country indices and a cross-country factor. We
validate the panel in two ways that use independent information. Over the period in which
Google's Community Mobility Reports exist, weekly innovations in congestion and in Google
workplaces mobility correlate at 0.72 outside the lockdown months, between 0.43 and 0.89 by
country, so congestion tracks the same activity that location data track and does so after 2022
when Google's series ended. In a pseudo-real-time nowcasting exercise, a pooled bridge
regression that adds congestion to an autoregressive model of monthly industrial-production
growth reduces out-of-sample error by 14 percent, a gain that is concentrated in disruptions and not
statistically secure on 21 evaluation months (Diebold-Mariano p = 0.19); country-by-country models do not beat the benchmark, and the
within-country correlation between congestion and production outside the lockdown is close to
zero. Congestion is a good indicator of the direction of activity when activity moves a lot,
and a weak one in ordinary months.

Our main finding concerns what happens when such a series is used to predict asset returns.
Congestion innovations, the standard object in this literature, are the weekly value minus the
trailing four-week mean of a weekday-adjusted log index. They look like noise but are not: their
autocorrelation at a lag of 52 weeks is 0.31 at the country level and 0.56 for the cross-country
factor, and a smooth annual seasonal is significant in about half the countries. Ramadan, Eid, Lunar New Year, Easter, school
holidays and year-end closures recur at nearly the same dates each year and shift traffic by
amounts that dwarf week-to-week activity surprises. Google mobility innovations have the same
property. This structure is not removed by weekday adjustment, by four-week differencing, by
calendar-month fixed effects, or even by country-by-year fixed effects, because it is a
within-year, within-month pattern. We show the consequence with a specification that is
typical of the state-dependent asset-pricing literature: next-week US-dollar returns on
emerging-market country funds regressed on the congestion innovation, its interaction with a
VIX-above-25 indicator, and a full set of fixed effects and interacted controls. The interaction
is 0.26 standard deviations with a t-statistic of 3.7, an apparently clean example of good
activity news being bad for stocks in calm markets and good in stressed ones. The same
regression with the innovation lagged by exactly 52 weeks, a series that cannot contain news
about next week, gives a coefficient of 0.08 with a t-statistic of 1.2 on the same sample, and
the actual signal on that sample gives 0.19 with t of 2.6; with a real-time seasonal difference
of the signal the interaction is 0.05 with a t-statistic of 0.7. These comparisons are
suggestive, and we show by simulation that on three years they are not decisive. What is
decisive is a decomposition that holds the calendar fixed: each country's own in-sample
week-of-year profile, with no week-to-week news in it, reproduces most of the interaction;
another country's profile reproduces none; a circular shift of the panel that breaks the
alignment between calendar and stress weeks removes it; and the non-seasonal residual retains a
marginal effect. The result was predominantly a calendar pattern in congestion coinciding with
the calendar clustering of the 2022 risk-off weeks. The unconditional relations reported in the single-city literature
are not found here: in country-by-country regressions of next-week index returns on the
country's congestion innovation, no country's local-index coefficient is significant at the 5 percent level in any of the three versions, and in a pooled panel the coefficient is -0.18 percent per standard deviation with a
t-statistic of -1.2.

Not everything disappears. Congestion innovations predict lower next-week realized variance of
US-dollar emerging-market returns, with a coefficient of -0.065 log points per standard
deviation (t = -2.3 clustered, -2.7 by block bootstrap) that is absent for the 52-week-lagged
placebo, passes a circular-shift placebo, and comes from negative innovations: bad activity
news raises next-week variance. The effect is small, about three percent of weekly volatility
per standard deviation, and is not detectable within any single year. Finally, within 2022 the
state-dependent pattern remains after seasonal differencing and with lockdown-stringency and
fuel-price controls (interaction 1.7 percent per standard deviation of the factor, t = 2.3, 52
weeks). We treat it as a hypothesis, not a
finding, and we have begun collecting the provider's live feed for all 490 cities in order to
test it out of sample under a specification, state variable and decision rule fixed in advance
and reported in the appendix.

The paper makes three contributions. First, it provides, to our knowledge, the first multi-country daily congestion panel for
emerging-market research, compared against mobility and production data, and documents its properties, provenance
and limits, including the provider's 2023 methodology change that ended the public daily
series. Second, it identifies annual seasonality as a first-order problem for mobility-based
predictability research and supplies two cheap diagnostics, a 52-week-lag placebo and a
real-time seasonal difference, that any such study can run; applied to our own best result and
to the single-city literature's claims, they overturn both. Third, it reports what does survive:
a modest nowcasting gain concentrated in disruptions and a small, signed volatility effect. The paper
belongs to three literatures. The first is the literature on spurious and seasonal
predictability: Novy-Marx (2014) shows that weather, sunspots and planetary positions "predict"
anomaly returns in short samples; Heston and Sadka (2008) and Keloharju, Linnainmaa and Nyberg
(2016) document annual seasonality in returns themselves; Stambaugh (1999) and Ferson,
Sarkissian and Simin (2003) show how persistent regressors produce spurious predictability;
Harvey et al. (2016) and Harvey (2017) set the multiple-testing hurdles that a searched
result must clear; and Hirshleifer et al. (2020) show that mood proxies inherit
return seasonality, which bears directly on the investor-mood reading of the single-city
congestion studies. Holiday effects in the markets we study are documented by Bialkowski,
Etebari and Wisniewski (2012) for Ramadan and by Seyyed et al. (2005) for Saudi
Arabia, which is why moving-holiday dummies are part of every specification. The second is the
literature on alternative data: the Google Flu Trends episode (Lazer, Kennedy, King and
Vespignani, 2014) is the closest precedent for a high-frequency proxy that tracked its target
until a structural change and a seasonal confound broke it, and the finance strand (Froot, Kang,
Ozik & Sadka, 2017; Zhu, 2019; Katona, Painter, Patatoukas & Zeng, 2024; Duz Tan and Tas,
2019, in this journal) has not generally applied seasonal placebos. The third is the
nowcasting strand (Sampi & Jooste, 2020; Woloszko, 2024), where central-bank uses of mobility
data during the pandemic mostly worked with year-on-year or versus-2019 baselines, an implicit
seasonal difference that the finance applications dropped. The state-dependent pricing of
macroeconomic news (Boyd, Hu & Jagannathan, 2005; McQueen & Roley, 1993) is the prediction
our exploratory result appeared to confirm and whose test we defer to the pre-registered sample.

Section 2 describes the data, the construction of the signal, the seasonality diagnosis and the
designs. Section 3 reports the validation, the placebo results, the volatility effect and the
pre-registered hypothesis. Section 4 concludes.

For readers of this journal, Section 3.6 reports the Turkish case separately: the deepest-covered market in the panel, and one where the pooled patterns do not hold.

## 2. Data and methodology

### 2.1 The congestion index and its public archive

The index is TomTom's city-level congestion level, computed from anonymized probe data
(navigation applications and fleet devices) on the covered road network of a metropolitan area.
For each road segment the provider compares observed travel times with a free-flow reference
estimated from its own low-traffic periods; the city index is the traffic-weighted percentage of
extra travel time, so that 30 means trips took 30 percent longer than at free flow. Because
congestion is a convex function of traffic volume, a given change in trips produces a larger
index change on a saturated network than on an uncongested one; the index is therefore a
monotone but nonlinear indicator of activity, and comparisons across cities are in standardized
units throughout.

From 2020 to early 2023 the provider displayed daily values on its public city pages, and an
open-source project archived them daily (ActiveConclusion, COVID19_mobility repository). The
archive holds 414 cities in 57 countries from 30 December 2019 to 14 February 2023 and includes
the provider's own ratio of each day to the same weekday of 2019. The repository's MIT licence
covers the scraper and the compiled file; the underlying data remain the provider's, whose terms
permit non-commercial use with attribution. We use the archive under those terms and do not
redistribute it; the processed country-week panel and all code are released. In 2023 the
provider redesigned the index, changed the headline metric to travel time per 10 kilometres with
separate centre and metro boundaries, and now publishes only monthly values for the two most
recent years, so the archive is the only public source of daily history and the post-2023
series is not a continuation of it. A live hourly feed for the trailing seven days remains
available per city; we have collected it for all 490 cities in the current index, more than the 414 in the archive, since 21 October 2026 and describe
its use in Section 3.5.

### 2.2 Sample and aggregation

The main sample is the 12 emerging markets with at least one major city in the archive, a
liquid equity market and a US-dollar country fund: Turkey (10 cities), Poland (12), Brazil (9),
South Africa (6), India (4), Saudi Arabia (2) and one city each for Mexico, Indonesia, Thailand,
Egypt, Malaysia and the Philippines, 49 cities in all. Russia is excluded because its market
closed in 2022; Morocco, Vietnam, Nigeria and Pakistan are absent from the archive; Taiwan and
the United Arab Emirates are classified as developed or frontier by major index providers and
are excluded, as is Greece; Appendix Table A5 shows that adding all three leaves the Table 6 interaction and the volatility coefficient within their ranges. Six countries are represented by a single city, which we flag because
a city-specific disruption then becomes a national signal; Appendix Table A5 reports the
placebo and volatility results separately for single-city and multi-city countries. Cities are
combined with metropolitan population weights listed in Appendix Table A1; equal weights and
the largest city alone give the same results (Appendix Table A5). Fewer than one percent of city-days are missing and are linearly interpolated
when the gap is at most three days. Table 1 reports descriptives.

### 2.3 Signal construction and the seasonality problem

The standard signal in this literature, which we adopt so that our results speak to it, is
built in three steps: the log daily index minus its trailing 52-week mean for the same weekday
(lagged one day, so no future information is used), aggregated to the country and averaged over
Friday-ending weeks; and the innovation, the week's value minus the mean of the preceding four
weeks, standardized within country. The construction removes the weekly cycle and slow trends.
It does not remove the annual cycle, and Table 2 measures that cycle on a true weekly time
index with the lockdown weeks set to missing, so that lags are genuine 52-week lags. For the 49
city series the mean autocorrelation of the weekly innovation at lag 52 is 0.35; for the 12
country series 0.31; for the cross-country factor 0.56; for Google workplaces innovations 0.33 by
country and 0.39 for the Google factor. A smooth three-harmonic seasonal explains 9 to 13
percent of the variance of the series and is significant at the 5 percent level in 42 percent
of countries and for the factor. We also report the in-sample week-of-year R-squared, which is
0.55 at the city and country level, because it is the statistic a researcher would naively
compute; it is overfitted (52 cell means on 138 weeks, chance level about 0.37, adjusted value
0.27) and predicts nothing out of sample (leave-one-year-out R-squared is negative), so it
should not be read as the seasonal share of variance. The annual component is concentrated in
countries with fixed-date holidays and school calendars (Brazil, South Africa, Poland, Mexico,
Thailand: 52-week autocorrelations of 0.46 to 0.74), while in Turkey, India, Indonesia and Malaysia, where Ramadan and other moving holidays shift by eleven days a year and do not align week to week, the 52-week autocorrelation is near zero; a smooth seasonal is nonetheless significant in India, Malaysia and, marginally, Indonesia, and absent only in Turkey. For moving-holiday countries the explicit holiday dummies, not a seasonal filter, are the relevant safeguard. Figure 2 plots the mean week-of-year profile.

Two features make this a problem for predictability research rather than a nuisance. The
seasonal pattern is within-year and within-month, so year, calendar-month and even
country-by-year fixed effects leave it in the regressor; only a model of the week-of-year
profile removes it. And the market states used in conditional asset pricing, high-VIX weeks,
crises, announcement windows, are themselves clustered in calendar time within a short sample,
so a seasonal regressor and a clustered state can produce an interaction that reflects nothing
but the calendar. We therefore accompany every return regression with two diagnostics.

The 52-week-lag placebo replaces the signal by its own value 52 weeks earlier. The lagged series
has the same seasonal profile and no information about next week's return; if it produces a
coefficient comparable to the actual signal, the actual coefficient is not evidence of
information. Because the lag costs the first year of data, the actual signal is re-estimated on
the same reduced sample for a like-for-like comparison. The real-time seasonal difference
replaces the signal by its value minus its value 52 weeks earlier, re-standardized, which an
investor could compute in real time and which removes any pattern that repeats annually; it
also costs the first year and adds noise, so it is a conservative test. In-sample alternatives,
removing full-sample week-of-year or month-of-year means, use future information and are not
available in real time; we report them only to show that they can preserve a spurious result.

### 2.4 Validation design

Google's Community Mobility Reports give daily visits to workplaces, transit stations and
retail locations relative to a January 2020 baseline, at the country level, from February 2020
to October 2022, built from location histories of Android users who opted in. We compute weekly
innovations in workplaces mobility exactly as for congestion and report their correlation with
congestion innovations by country, in the full overlap, excluding March to June 2020, and after
June 2021, so that agreement cannot be attributed to the lockdown collapse that both series
share.

The nowcasting exercise, in the spirit of the mobility-based nowcasts of Sampi and Jooste (2020) and the elasticity estimates of Gamtkitsulashvili and Plekhanov (2023), targets month-on-month growth of seasonally adjusted industrial
production from the World Bank's Global Economic Monitor and the IMF's International Financial
Statistics for the 17 countries in the broader archive with such data, in an expanding-window
pseudo-real-time design from January 2021 to January 2023 with current-vintage data and the
previous month's production treated as known. Models are a first-order autoregression, a
country-level bridge regression adding the monthly change in congestion, an Almon-restricted
mixed-data-sampling regression on 60 daily lags, and a pooled bridge with country fixed effects.
The lockdown months are excluded from training in the reported version; the version with them
included is in Appendix Table A3 and performs worse. Forecast comparisons use the
Diebold-Mariano statistic computed on the monthly average of the loss differential across
countries, so that the effective sample is the 21 and 19 evaluation months, with the pooled
country-month version reported for comparison.

### 2.5 Return-predictability designs

Returns are weekly log returns, Friday to Friday, on local equity indices and on US-dollar
country funds (Egypt has no fund), with realized variance the sum of squared daily log returns
within the week; prices from Yahoo Finance and Stooq. Global controls are the MSCI emerging-
markets fund return, the change in log VIX, the Brent return, the change in log DXY, the change
in the US ten-year yield and the log VIX level. Three designs are used. The single-country
regression of the prior literature regresses the next-week return on the country's innovation,
its own same-week return and the controls, with heteroskedasticity-and-autocorrelation-robust
errors, for each country separately. The pooled panel adds country-by-calendar-month fixed
effects and clusters standard errors by week. The state-dependent specification, which we use as
the worked example, is

r_{i,t+1} = a_{i,y(t)} + a_{S,m(t)} + b_1 x_{i,t} + b_2 x_{i,t} S_t + b_3 S_t + h' H_{i,t}
            + g' z_{i,t} + k' z_{i,t} S_t + u_{i,t+1},                                        (1)

with S_t = 1[VIX_t > 25], country-by-year and state-by-calendar-month fixed effects, moving-
holiday dummies H (Appendix Table A2: the Ramadan month and the Eid weeks for Muslim-majority countries, Diwali,
Lunar New Year, Easter and the year-end weeks), the own return and the global controls, each
also interacted with the state, and standard errors clustered by week. Country-by-year effects absorb any year contrast; state-by-month effects absorb any tendency of stress weeks to fall in particular months; the holiday dummies handle moving holidays that neither absorbs; and the interacted controls prevent the interaction from loading on global factors that co-move with congestion in stress weeks.

Table 6, Panel A reports the ladder from country-by-month effects alone to this specification. We also add, as a check on non-seasonal confounders, the weekly change in the Oxford stringency index (Hale et al., 2021) and the lagged weekly change in the local-currency oil price (log Brent plus log local currency per dollar), a proxy for retail fuel prices, each interacted with the state.

Each design is estimated with the actual signal, the 52-week-lagged placebo and the real-time seasonal difference. The volatility regression replaces the return by next-week log realized variance and adds the own log
variance, its four- and thirteen-week means and the log VIX, a heterogeneous-autoregressive
specification with the signal added.

### 2.6 What we tried

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

### 3.1 Validation

Figure 1 plots the weekly congestion level for the 12 countries with the lockdown months and
the VIX-above-25 weeks shaded; the lockdown collapse, the recovery, and the recurring holiday
dips that motivate Section 2.3 are visible in every panel.

Table 3 reports the correlation between weekly congestion innovations and Google workplaces
mobility innovations by country. Pooled across countries the correlation is 0.75 in the full
overlap, 0.72 excluding the lockdown months and 0.75 after June 2021; by country it ranges from
0.43 (Philippines) and 0.48 (Saudi Arabia) to 0.82-0.89 (Turkey, Egypt, South Africa, Poland, Brazil) outside the lockdown. The agreement is not a lockdown artifact, is strongest in Brazil, South Africa, Poland, Egypt and Turkey, and is weakest where the single
covered city is a small share of the national economy or where the network is uncongested.
Congestion measures what location data measure, and continues to do so after Google's series
ended. Both are built from smartphone and probe-device locations, so the agreement is between
two readings of the same underlying behaviour rather than a validation against output; the
independent target is industrial production, to which we turn next.

Table 4 reports the nowcasting results. Relative to the autoregressive benchmark, the
country-level bridge has a root mean squared error ratio of 1.02 and the restricted
mixed-data-sampling model 1.19; neither helps. The pooled bridge with country fixed effects has a
ratio of 0.86 over 2021-2023 and 0.92 after June 2021, and raises the share of correctly
signed nowcasts from 52 to 57 percent. The Diebold-Mariano statistic computed on the monthly
average of the loss differential across countries, which respects the fact that the 17
countries share each month's shocks, is 1.35 (p = 0.19) over the full evaluation window and
1.75 (p = 0.10) after June 2021; the pooled country-month version gives p = 0.08 and overstates
precision. The gain is therefore real in magnitude but not statistically secure on 21 and 19
evaluation months. The gain comes from months in which activity moved
sharply; the within-country correlation between monthly congestion changes and production
growth is 0.27 in the full sample and 0.09 once the lockdown months are removed, and the
year-on-year correlation falls from 0.39 to 0.04. Congestion is a disruption indicator. That is
useful, because disruptions are when official data are slowest, but it should not be oversold:
in an ordinary month monthly production growth is close to unpredictable and congestion does
not change that.

### 3.2 Seasonality

Table 2 and Figure 2 establish the facts described in Section 2.3. Three points deserve
emphasis. The seasonality is as strong in Google mobility as in congestion, so it is a property
of activity data, not of one provider's index. It survives the four-week innovation filter
because holiday effects last one to four weeks and recur annually, which the filter treats as
news each year. And it is heterogeneous: fixed-calendar holidays (Christmas, Carnival, school terms) produce high 52-week autocorrelation and significant Fourier seasonals, while moving holidays (Ramadan, Eid, Diwali) do not align week to week and can escape both statistics, as the Turkish series shows. For those countries no seasonal filter is a safeguard; only explicit holiday dummies are, which is why every specification in this paper carries them.

### 3.3 The placebo at work

Table 5 reports the single-country regressions. For next-week local index returns in the seven
countries with usable index data on a common calendar, no coefficient is significant at the 5
percent level with the actual signal, with the lagged placebo, or with the seasonal difference;
the mean absolute t-statistic is 0.8, 0.9 and 1.0. For US-dollar fund returns in eleven
countries, one coefficient is significant in each version, a different country each time
(Philippines, India, Mexico), which is what chance produces. The pooled panel coefficient is
-0.18 percent per standard deviation (t = -1.2) for local returns and -0.20 (t = -1.2) for
dollar returns. The unconditional congestion-return relation reported for Bangkok and Kuala
Lumpur in earlier work, at daily frequency on other providers' indices, is not found at weekly
frequency in a twelve-country panel; Malaysia is among the seven local-index countries and
Thailand among the eleven fund countries. The daily designs of those studies are exposed to
day-of-year structure in the same way, and none ran a placebo of the kind we propose.

Table 6 reports the worked example for next-week US-dollar fund returns in the ex-lockdown
sample. Panel A shows that the interaction is 0.31 (t = 3.3) with country-by-month effects alone and remains between 0.24 and 0.30 (t = 2.9 to 4.0, the last with Driscoll-Kraay errors) as state-by-month effects, year and country-by-year effects, holiday dummies, state-interacted controls and the log VIX level are added on top of the country-by-month effects; fixed effects do not remove it. Specification (1), which replaces the country-by-month effects with country-by-year and state-by-month effects, gives a calm-state coefficient of -0.054 (t = -1.8) and an interaction of 0.259 (t = 3.7), 0.273 (t = 3.8) with the stringency and fuel controls: the response to a congestion innovation switches from
negative when the VIX is at or below 25 to positive when it is above, with country-by-year and
state-by-month fixed effects, holiday dummies and state-interacted controls all in place, a
result that reads as the real-time counterpart of the state-dependent reaction to macro news.
With the signal lagged 52 weeks, on the 1,098 observations that remain, the interaction is 0.082
(t = 1.2); the actual signal on those same observations gives 0.189 (t = 2.6), so last year's
congestion recovers about 40 percent of the coefficient. With the real-time seasonal difference
the interaction is 0.049 (t = 0.7). Figure 3 plots the calm-state and stress-state coefficients
under the three versions. These two comparisons are suggestive but, we show, not decisive. A
signal with 52-week autocorrelation of 0.3 to 0.6 would mechanically hand part of a genuine
coefficient to its own lag, and a seasonal difference adds noise; simulating returns that respond only to the actual signal, with noise calibrated to the observed fit on the 946 country-weeks that have the lagged signal and all controls (where the actual interaction is 0.157, t = 2.0, the lagged placebo 0.109, t = 1.8, and the seasonal difference -0.009), the ratio of the placebo to the actual coefficient has a median of 0.12 but a 5-95 percent range from -1.5 to 1.7, and 21 percent of such simulations produce a seasonal-difference ratio at or below the observed one (Appendix A6).
With interaction t-statistics near 2, the three-version comparison cannot separate a calendar
coincidence from a persistent priced signal on three years of data.

What does discriminate is a decomposition that holds the calendar fixed. Replacing the signal by
each country's own in-sample week-of-year profile, the pure seasonal component with no
week-to-week news, gives an interaction of 0.156 (t = 2.9); replacing it by another country's
profile gives 0.007 (t = 0.1); the non-seasonal residual, the signal minus its own profile, gives
0.102 (t = 2.0); and shifting the whole panel circularly in time, which keeps every country's
persistence and the cross-section intact but breaks the alignment between its calendar and the
stress weeks, gives a placebo t-statistic with mean 0.2 and standard deviation 1.0 that never
reaches the actual 3.7 in 300 draws. The sign switch is therefore carried predominantly by each
country's own annual pattern coinciding with the risk-off weeks of 2022, with a marginal
contribution from non-seasonal movements that the data cannot resolve further. In-sample deseasonalization by full-sample month-of-year means preserves the result (0.257, t = 3.0, with country-by-month effects) because it leaves most of the week-level structure in place, which is why it is not a substitute for
the tests above.

The lesson generalizes. Any predictability study that uses a mobility, traffic, footfall,
electricity or search-volume innovation, and any conditional study whose state variable
clusters in calendar time, should report the 52-week-lag placebo and the real-time seasonal
difference. Neither requires new data, and in our case both would have taken an afternoon to
run.

### 3.4 What survives: volatility

Table 7 reports the volatility regression and the battery we apply to it. With moving-holiday
dummies added to the heterogeneous-autoregressive specification, the coefficient on the
congestion innovation in the regression of next-week log realized variance of US-dollar fund
returns is -0.065, with t-statistics of -2.3 clustered by week, -2.6 with Driscoll-Kraay errors
and -2.7 from a moving-block bootstrap (95 percent interval -0.10 to -0.01). It is unchanged
when the target is variance per trading day, which removes the mechanical effect of holiday
weeks with fewer trading days, and when the stringency change and the fuel-price proxy of Section 2.5 are added. The 52-week-lagged placebo gives 0.025 (t = 0.9); the real-time seasonal
difference gives -0.053 (t = -1.8); and in 300 circular shifts of the panel only one percent of
placebo t-statistics are as negative as the actual one. The effect is therefore not a seasonal
pattern. It is also small and specific. It adds 0.2 percentage points to an R-squared of 0.42,
and a one-standard-deviation innovation moves next-week volatility by about three percent. It
is signed rather than symmetric: the absolute innovation has the wrong sign and is insignificant
(0.055, t = 1.3), and the effect comes from negative innovations (-0.087, t = -1.8) rather than
positive ones (-0.031, t = -0.6), so the right description is the familiar asymmetry in which
bad news raises subsequent variance, not resolution of uncertainty. It is a pooled effect that
is not significant within any single year (t = -1.5, -0.7 and -0.4 in the second half of 2020,
2021 and 2022), is absent for local index returns (t = -0.8), and is marginal for the
cross-country factor (t = -1.1) and the country-specific residual (t = -1.9); it is weaker
in single-city countries (Appendix Table A5). We report it because it is the one return-related
estimate in our exploratory work that survives every diagnostic we apply, and we describe it as
what it is: a small, signed, pooled effect of bad activity news on next-week variance.

### 3.5 The 2022 reversal as a hypothesis, and a pre-registered test

Within calendar year 2022, a sample of 52 weeks containing three global risk-off episodes, the
state-dependent pattern survives the real-time seasonal difference: in a time-series regression
of the equal-weight basket's next-week return on the seasonally differenced cross-country
factor, the interaction with the VIX indicator is 2.0 percent per standard deviation of the
differenced factor (t = 2.2; 2.0, t = 2.4, with holiday-share controls; 1.7, t = 2.3, when the
weekly change in the Oxford stringency index and the lagged change in the local-currency oil
price, a proxy for retail fuel prices, are added with their state interactions; Appendix Table
A4 and Table 8). The same regression gives 0.7 (t = 1.2) over the whole ex-lockdown sample, 1.0 (t = 2.2)
with holiday and confounder controls, and -1.3 (t = -0.4) within 2021, where the estimate is
unstable on 41 weeks. The stringency and fuel controls also leave the Table 6 interaction and
the volatility coefficient within rounding, their own coefficients are insignificant, and
congestion innovations correlate at -0.13 with the stringency change and 0.02 with the fuel
proxy, so neither domestic lockdown waves nor fuel-price shocks are behind the patterns we
report, within the limits of a fuel proxy rather than pump prices. Fifty-two weeks, one year, and a result found
after the fact are not evidence; they are a hypothesis. We have therefore fixed, before any new data are analysed, the
signal construction, the state variable, the specification, the sample window and the decision
rule under which the hypothesis will be tested on the provider's live feed, which we have
collected for all 490 cities since 21 October 2026 (Appendix B). The collector is a script that requests each
city's public seven-day feed twice daily, identifies itself with a standard browser user-agent
string, and stores the hourly values; it runs on a single machine under a scheduler, so that a
gap of more than seven days loses data irrecoverably, and Figure 4 reports its coverage. We are
seeking the provider's written confirmation that automated collection of the public feed for
research is within its terms, and we will not rely on the live sample without it. The
test window begins when 52 weeks of live data allow a real-time seasonal difference and runs
until at least 30 stress weeks have accumulated. Because the live feed is a different series from
the archive, the test is of the hypothesis, not of a spliced sample.

### 3.6 The Turkish case

Turkey has the deepest coverage in the panel, ten cities, and its congestion innovations track
Google workplaces mobility at 0.82 outside the lockdown. It is also the clearest example of the
moving-holiday problem: its 52-week autocorrelation is 0.01 and a three-harmonic seasonal
explains six percent of variance (p = 0.21), so no seasonal filter finds annual structure, yet
Ramadan and the two Eids shift Istanbul traffic by more than any ordinary week's news and are
absorbed only by the explicit holiday dummies. In the country-by-country regressions of Table 5
the Turkish coefficients are negative and insignificant with every signal version (local index
-0.39, t = -1.3; fund -0.44, t = -1.1). In the state-dependent specification estimated for Turkey alone, with calendar-month effects and HAC errors, the interaction is -0.28 (t = -1.4), the opposite sign to the pooled estimate,
and the Turkish volatility coefficient is 0.13 (t = 1.1), also the opposite sign. The pooled
results of this paper are therefore not Turkish results, and a reader interested in the
Istanbul market should take from this paper the diagnostics rather than the point estimates;
the 2021-2022 period, in which Turkish monetary policy and the lira followed a path unlike any
other market in the sample, is a natural case for the country-specific analysis that a longer
live sample will allow.

### 3.7 Implications

For researchers, the implication is procedural: mobility-type signals must be treated as
seasonal series and conditional results must be shown to survive a placebo built from the
signal's own past. For central banks and statistical offices in emerging markets, congestion is
a daily indicator of large movements in activity that tracks independent mobility measures, best used in a pooled model
and in disruptions, and not a substitute for official data in calm months. For investors, the usable content is in volatility: negative activity surprises raise next-week variance, which matters for
risk budgeting, while directional rules built on congestion are, on the evidence of 2020-2023,
calendar effects in disguise. For the data provider and for the research community, the
discontinuation of the public daily series in 2023 removed a resource whose value this paper
documents; the live feed partly replaces it, at the cost of continuous collection.

## 4. Conclusion

We have assembled a daily congestion panel for 49 cities in 12 emerging markets
over 2020-2023, shown that it tracks activity as well as location-based mobility data and
improves production nowcasts in disruptions, and shown that its country-specific annual structure
produces spurious conditional predictability, including a textbook-looking state-dependent
sign switch with a t-statistic of 3.7 that each country's own calendar profile reproduces,
another country's does not, and a circular shift of the panel removes, while the lag and
seasonal-difference placebos that a short sample allows are informative but underpowered. The
unconditional relations of the earlier single-city literature are not found here. A small,
signed effect of bad activity news on next-week variance survives every diagnostic. The 2022 state-dependent pattern is recorded as a pre-registered hypothesis for a
live sample now being collected. The limitations are a three-year sample dominated by the
pandemic and its recovery, twelve countries of which six are represented by one city, a
provider index that is nonlinear in traffic volume and was redefined in 2023, and validation
against mobility data that share the index's measurement base. The main contribution is a
warning and the tools to act on it, and we would rather publish that than the result it
overturned.

## Tables

**Table 1. Sample and descriptive statistics, January 2020 to February 2023 excluding March-June 2020 (147 weeks per country; regressions that need lagged signals use 138).**
Mean congestion is the average weekly congestion level in percent extra travel time; the innovation is the weekly deviation from the trailing four-week mean of the weekday-adjusted log index, standardized within country; returns are weekly log returns on the US-dollar country fund (Egypt has none); share stress is the fraction of weeks with the VIX above 25.

| Country | Cities | Weeks | Mean congestion (%) | Mean USD return (%/wk) | SD USD return (%/wk) |
|---|---|---|---|---|---|
| Brazil | 9 | 147 | 28.0 | 0.01 | 4.57 |
| Egypt | 1 | 147 | 16.9 |  |  |
| India | 4 | 147 | 31.1 | 0.20 | 2.51 |
| Indonesia | 1 | 147 | 32.9 | 0.08 | 3.03 |
| Malaysia | 1 | 147 | 28.5 | -0.08 | 2.00 |
| Mexico | 1 | 147 | 32.4 | 0.40 | 3.27 |
| Philippines | 1 | 147 | 56.2 | -0.07 | 3.07 |
| Poland | 12 | 147 | 29.9 | -0.14 | 4.52 |
| Saudi Arabia | 2 | 147 | 10.6 | 0.17 | 2.38 |
| South Africa | 6 | 147 | 23.1 | 0.06 | 4.04 |
| Thailand | 1 | 147 | 35.6 | -0.06 | 2.83 |
| Turkey | 10 | 147 | 30.0 | 0.22 | 5.73 |


**Table 2. Annual structure in weekly innovations, ex-lockdown, on a true weekly time index.**
ac(52) is the autocorrelation at a 52-week lag; Fourier R² is from a three-harmonic annual seasonal; the in-sample week-of-year R² (52 cell means on about 138 weeks, chance level about 0.37) is reported with its adjusted and leave-one-year-out values to show that it is overfitted.

| Series | N | Mean ac(52) | Share ac(52) > 0.2 | Fourier R² | Share Fourier F p < 0.05 | Week-of-year R² (in-sample) | Adjusted | Leave-one-year-out |
|---|---|---|---|---|---|---|---|---|
| Congestion, 49 cities | 49 | 0.35 | 0.65 | 0.09 | 0.39 | 0.55 | 0.28 | -0.30 |
| Congestion, 12 countries | 12 | 0.31 | 0.58 | 0.10 | 0.42 | 0.55 | 0.27 | -0.30 |
| Congestion, cross-country factor | 1 | 0.56 | 1.00 | 0.13 | 1.00 | 0.67 | 0.47 | 0.08 |
| Google workplaces, 12 countries | 12 | 0.33 | 0.50 | 0.07 | 0.25 | 0.57 | 0.24 | -0.48 |
| Google workplaces, factor | 1 | 0.39 | 1.00 | 0.08 | 0.00 | 0.61 | 0.30 | -0.34 |


Country detail (congestion): Brazil ac(52) 0.68, Fourier p 0.27; Egypt ac(52) 0.14, Fourier p 0.04; India ac(52) 0.08, Fourier p 0.00; Indonesia ac(52) -0.06, Fourier p 0.05; Malaysia ac(52) -0.07, Fourier p 0.00; Mexico ac(52) 0.57, Fourier p 0.01; Philippines ac(52) 0.40, Fourier p 0.18; Poland ac(52) 0.59, Fourier p 0.13; Saudi Arabia ac(52) 0.24, Fourier p 0.39; South Africa ac(52) 0.74, Fourier p 0.00; Thailand ac(52) 0.46, Fourier p 0.10; Turkey ac(52) 0.01, Fourier p 0.21.


**Table 3. Correlation of weekly innovations in congestion and Google workplaces mobility, by country.**
Weekly innovations constructed identically for both series; overlap is February 2020 to October 2022.

| Country | Full overlap | Excluding March-June 2020 | After June 2021 |
|---|---|---|---|
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


**Table 4. Pseudo-real-time nowcasts of monthly industrial-production growth, 17 countries, lockdown months excluded from training.**
RMSE relative to the AR(1) benchmark; directional accuracy is the share of correctly signed nowcasts. The Diebold-Mariano test on monthly-average loss differentials (effective sample 21 and 19 months) gives t = 1.35 (p = 0.19) and t = 1.75 (p = 0.10) for the pooled bridge; the pooled country-month version gives p = 0.08 and overstates precision.

| Evaluation window | Model | Country-months | Relative RMSE | Directional accuracy |
|---|---|---|---|---|
| 2021-01 to 2023-01 | AR(1) benchmark | 357 | 1.000 | 0.515 |
| 2021-01 to 2023-01 | Country bridge (monthly congestion change) | 357 | 1.024 | 0.513 |
| 2021-01 to 2023-01 | Almon MIDAS (60 daily lags) | 357 | 1.193 | 0.518 |
| 2021-01 to 2023-01 | Pooled bridge, country fixed effects | 357 | 0.860 | 0.566 |
| 2021-07 to 2023-01 | AR(1) benchmark | 323 | 1.000 | 0.533 |
| 2021-07 to 2023-01 | Country bridge (monthly congestion change) | 323 | 1.019 | 0.520 |
| 2021-07 to 2023-01 | Almon MIDAS (60 daily lags) | 323 | 1.282 | 0.514 |
| 2021-07 to 2023-01 | Pooled bridge, country fixed effects | 323 | 0.919 | 0.570 |


**Table 5. Country-by-country regressions of next-week return (percent) on the country's congestion innovation, ex-lockdown.**
Controls: own same-week return, MSCI EM return, change in log VIX, Brent return, change in log DXY, change in US ten-year yield; HAC(4) t-statistics. Three signal versions: actual, lagged 52 weeks, and the real-time seasonal difference. No coefficient is significant at 5 percent for local indices; one of eleven is, a different country each time, for US-dollar funds.

| Country | Return | Actual b | t | Lag-52 b | t | Seasonal-diff b | t |
|---|---|---|---|---|---|---|---|
| Brazil | local index | 0.12 | 0.39 | -0.19 | -1.10 | 0.39 | 1.35 |
| India | local index | -0.01 | -0.07 | 0.14 | 0.83 | -0.15 | -0.83 |
| Indonesia | local index | 0.09 | 0.54 | -0.03 | -0.16 | 0.05 | 0.31 |
| Malaysia | local index | 0.06 | 0.39 | 0.13 | 1.22 | -0.15 | -1.23 |
| Mexico | local index | -0.25 | -0.82 | -0.30 | -1.08 | 0.25 | 1.94 |
| South Africa | local index | -0.45 | -1.86 | -0.29 | -1.64 | -0.08 | -0.56 |
| Turkey | local index | -0.39 | -1.33 | 0.11 | 0.34 | -0.17 | -0.68 |
| Brazil | USD ETF | 0.40 | 0.88 | -0.34 | -1.19 | 0.72 | 1.54 |
| India | USD ETF | -0.07 | -0.30 | 0.28 | 1.98 | -0.32 | -1.96 |
| Indonesia | USD ETF | 0.27 | 0.85 | -0.16 | -0.52 | 0.31 | 0.99 |
| Malaysia | USD ETF | 0.04 | 0.26 | 0.12 | 1.12 | -0.15 | -1.15 |
| Mexico | USD ETF | -0.20 | -0.51 | -0.46 | -1.37 | 0.42 | 2.25 |
| Philippines | USD ETF | -0.54 | -2.28 | -0.02 | -0.11 | -0.28 | -1.52 |
| Poland | USD ETF | -0.26 | -0.60 | -0.47 | -1.20 | 0.31 | 0.69 |
| Saudi Arabia | USD ETF | -0.21 | -0.77 | -0.23 | -1.25 | -0.03 | -0.11 |
| South Africa | USD ETF | -0.51 | -1.33 | -0.40 | -1.27 | -0.25 | -0.93 |
| Thailand | USD ETF | -0.15 | -0.66 | 0.05 | 0.32 | -0.03 | -0.16 |
| Turkey | USD ETF | -0.44 | -1.14 | 0.41 | 1.03 | -0.36 | -0.92 |


**Table 6. The state-dependent specification: fixed-effects ladder, placebo versions and calendar decomposition.**
Dependent variable: next-week US-dollar fund return (SD units); x = congestion innovation (SD units); S = 1[VIX > 25]; ex-lockdown sample. Panel A adds controls cumulatively on top of country-by-calendar-month effects; equation (1), reported in Panel B, replaces the country-by-month effects with country-by-year and state-by-month effects. Standard errors clustered by week; L7 uses Driscoll-Kraay(4).

Panel A. Fixed-effects ladder

| Specification | N | x, calm | t | x × S | t | x, stress |
|---|---|---|---|---|---|---|
| L1 country x month FE | 1518 | -0.107 | -2.90 | 0.307 | 3.26 | 0.200 |
| L2 + state x month FE | 1518 | -0.101 | -2.68 | 0.292 | 3.44 | 0.191 |
| L3 + year FE | 1518 | -0.101 | -2.63 | 0.291 | 3.35 | 0.189 |
| L4 country x year FE | 1518 | -0.104 | -2.63 | 0.297 | 3.35 | 0.193 |
| L5 + holiday dummies | 1518 | -0.065 | -1.87 | 0.243 | 2.94 | 0.178 |
| L6 + S x controls, log VIX | 1518 | -0.072 | -2.06 | 0.274 | 3.35 | 0.202 |
| L7 everything, Driscoll-Kraay(4) | 1518 | -0.072 | -2.48 | 0.274 | 4.00 | 0.202 |

Panel B. Signal versions, equation (1); with the stringency and fuel controls added, the interactions are 0.273 (t 3.76), 0.078 (t 1.16) and 0.037 (t 0.54) for the actual, lagged and differenced signals

| Version | N | x, calm | t | x × S | t |
|---|---|---|---|---|---|
| Actual signal | 1518 | -0.054 | -1.83 | 0.259 | 3.69 |
| Actual signal, placebo sample | 1098 | -0.028 | -0.81 | 0.189 | 2.57 |
| Signal lagged 52 weeks | 1098 | 0.025 | 0.74 | 0.082 | 1.22 |
| Real-time seasonal difference | 1098 | -0.036 | -1.09 | 0.049 | 0.67 |

Panel C. Calendar decomposition, equation (1); the circular-shift placebo is benchmarked against the 0.259 (t 3.69) estimate

| Regressor | N | calm | t | × S | t |
|---|---|---|---|---|---|
| Own in-sample week-of-year profile (seasonal component only) | 1617 | -0.041 | -1.64 | 0.156 | 2.86 |
| Another country's week-of-year profile | 1617 | -0.001 | -0.03 | 0.007 | 0.13 |
| Signal minus own profile (non-seasonal residual) | 1518 | -0.024 | -0.94 | 0.102 | 2.00 |
| Circular block shift of the panel, 300 draws | 1518 | | | placebo t: mean 0.18, SD 1.02; 0 of 300 ≥ 3.69 | |
| Within 2021 only (L6 without country-by-year effects) | 583 | -0.004 | -0.09 | -0.181 | -1.22 |
| Within 2022 only | 572 | -0.124 | -2.00 | 0.315 | 3.45 |


**Table 7. Next-week log realized variance of US-dollar fund returns on the congestion innovation.**
Heterogeneous-autoregressive controls (own log variance, four- and thirteen-week means), log VIX, MSCI EM return, change in log VIX, country-by-year and calendar-month fixed effects, moving-holiday dummies; week-clustered t unless stated.

| Specification | N | Coefficient | t |
|---|---|---|---|
| Baseline without holiday dummies | 1507 | -0.075 | -2.61 |
| With holiday dummies (reference) | 1507 | -0.065 | -2.27 |
| Per-trading-day variance target | 1507 | -0.065 | -2.25 |
| Driscoll-Kraay(4) errors | 1507 | -0.065 | -2.60 |
| Moving-block bootstrap, 500 draws | 1507 | -0.065 (SE 0.024; CI -0.104 to -0.013) | -2.70 |
| With stringency change and fuel proxy | 1507 | -0.065 | -2.21 |
| Absolute innovation | 1507 | 0.055 | 1.27 |
| Positive part / negative part | 1507 | -0.031 / -0.087 | -0.56 / -1.83 |
| Within 2020 H2 / 2021 / 2022 | 286 / 583 / 572 | -0.081 / -0.029 / -0.019 | -1.51 / -0.73 / -0.37 |
| Circular block shift placebo, 300 draws | | placebo t mean 0.02, SD 1.08 | 1.0% of draws ≤ actual |
| Local index target | 724 | -0.047 | -0.79 |
| Cross-country factor / country residual | 1507 | -0.130 / -0.054 | -1.11 / -1.94 |
| Signal lagged 52 weeks | 1087 | 0.025 | 0.88 |
| Real-time seasonal difference | 1087 | -0.053 | -1.84 |

R² without and with the innovation: 0.422 and 0.424. One standard deviation of the innovation moves next-week variance by -6.3 percent and volatility by -3.2 percent.


**Table 8. The 2022 pattern on the seasonally differenced cross-country factor: basket time series.**
Next-week return (percent) of the equal-weight basket of eleven US-dollar country funds on the real-time seasonally differenced factor (SD units), its interaction with S, S, global controls, holiday shares, and, in the second row of each block, the country-average stringency change and lagged local-currency oil price with their state interactions; HAC(4).

| Sample | Controls | N | F, calm | t | F × S | t |
|---|---|---|---|---|---|---|
| 2022 | holidays | 52 | -0.63 | -0.84 | 2.00 | 2.44 |
| 2022 | + stringency, fuel | 52 | -0.41 | -0.57 | 1.69 | 2.28 |
| July 2020 to February 2023 | holidays | 100 | -0.06 | -0.39 | 0.98 | 2.19 |
| July 2020 to February 2023 | + stringency, fuel | 100 | -0.02 | -0.15 | 1.00 | 2.23 |
| 2021 | holidays | 41 | 0.01 | 0.05 | -1.26 | -0.35 |
| 2021 | + stringency, fuel | 41 | 0.20 | 1.08 | -7.90 | -1.89 |

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
A5 Weighting and inclusion robustness: results/tables/appendix_A5_weights_inclusion.md. With equal city weights, the largest city only, or Taiwan, the UAE and Greece added, the Table 6 interaction is 0.21-0.28 (t 3.5-4.3) on the actual signal and 0.04-0.07 (t 0.6-0.9) on the seasonally differenced signal; the volatility coefficient, in the specification without holiday dummies, is -0.06 to -0.08 (t -2.5 to -2.6); in single-city countries alone it is -0.05 (t -1.2).
A6 Simulation of placebo attenuation under a news-only null: results/tables/round2_stats.md, Section 2.
B Pre-registration: paper/PREREGISTRATION.md.

## References

Beyer, R. C. M., Franco-Bedoya, S., & Galdo, V. (2021). Examining the economic impact of COVID-19 in India through daily electricity consumption and nighttime light intensity. *World Development, 140*, 105287. https://doi.org/10.1016/j.worlddev.2020.105287

Białkowski, J., Etebari, A., & Wisniewski, T. P. (2012). Fast profits: Investor sentiment and stock returns during Ramadan. *Journal of Banking and Finance, 36*(3), 835-845. https://doi.org/10.1016/j.jbankfin.2011.09.014

Boyd, J. H., Hu, J., & Jagannathan, R. (2005). The stock market's reaction to unemployment news: Why bad news is usually good for stocks. *Journal of Finance, 60*(2), 649-672. https://doi.org/10.1111/j.1540-6261.2005.00742.x

Cao, T., Qian, X., & Zhang, L. (2024). The price of the slow lane: Traffic congestion and stock block trading premium. *International Review of Finance, 24*(1), 30-52. https://doi.org/10.1111/irfi.12432

Düz Tan, S., & Taş, O. (2019). Investor attention and stock returns: Evidence from Borsa Istanbul. *Borsa Istanbul Review, 19*(2), 106-116. https://doi.org/10.1016/j.bir.2018.10.003

Eraslan, S., & Götz, T. (2020). *An unconventional weekly economic activity index for Germany* (Technical Paper 02/2020). Deutsche Bundesbank.

Ferson, W. E., Sarkissian, S., & Simin, T. T. (2003). Spurious regressions in financial economics? *Journal of Finance, 58*(4), 1393-1413. https://doi.org/10.1111/1540-6261.00571

Froot, K., Kang, N., Ozik, G., & Sadka, R. (2017). What do measures of real-time corporate sales say about earnings surprises and post-announcement returns? *Journal of Financial Economics, 125*(1), 143-162. https://doi.org/10.1016/j.jfineco.2017.04.008

Gamtkitsulashvili, T., & Plekhanov, A. (2023). Mobility and economic activity around the world during the Covid-19 crisis. *Applied Economics Letters, 30*(5), 608-614. https://doi.org/10.1080/13504851.2021.2001419

Hale, T., Angrist, N., Goldszmidt, R., Kira, B., Petherick, A., Phillips, T., Webster, S., Cameron-Blake, E., Hallas, L., Majumdar, S., & Tatlow, H. (2021). A global panel database of pandemic policies (Oxford COVID-19 Government Response Tracker). *Nature Human Behaviour, 5*(4), 529-538. https://doi.org/10.1038/s41562-021-01079-8

Harvey, C. R. (2017). Presidential address: The scientific outlook in financial economics. *Journal of Finance, 72*(4), 1399-1440. https://doi.org/10.1111/jofi.12530

Harvey, C. R., Liu, Y., & Zhu, H. (2016). ... and the cross-section of expected returns. *Review of Financial Studies, 29*(1), 5-68. https://doi.org/10.1093/rfs/hhv059

Heston, S. L., & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics, 87*(2), 418-445. https://doi.org/10.1016/j.jfineco.2007.02.003

Hirshleifer, D., Jiang, D., & DiGiovanni, Y. M. (2020). Mood beta and seasonalities in stock returns. *Journal of Financial Economics, 137*(1), 272-295. https://doi.org/10.1016/j.jfineco.2020.02.003

Katona, Z., Painter, M. O., Patatoukas, P. N., & Zeng, J. (2025). On the capital market consequences of big data: Evidence from outer space. *Journal of Financial and Quantitative Analysis, 60*(2), 551-579. https://doi.org/10.1017/S0022109023001448

Keloharju, M., Linnainmaa, J. T., & Nyberg, P. (2016). Return seasonalities. *Journal of Finance, 71*(4), 1557-1590. https://doi.org/10.1111/jofi.12398

Khanthavit, A. (2021). Bangkok traffic congestion, stressed investors, and Thai stock-market returns. *ABAC Journal, 41*(4), 1-23. https://doi.org/10.14456/abacj.2021.1

Khanthavit, A. (2022). The relationship between traffic congestion and stock market returns. *ABAC Journal, 42*(1), 1-15. https://doi.org/10.14456/abacj.2022.33

Lazer, D., Kennedy, R., King, G., & Vespignani, A. (2014). The parable of Google Flu: Traps in big data analysis. *Science, 343*(6176), 1203-1205. https://doi.org/10.1126/science.1248506

Lewis, D. J., Mertens, K., Stock, J. H., & Trivedi, M. (2022). Measuring real activity using a weekly economic index. *Journal of Applied Econometrics, 37*(4), 667-687. https://doi.org/10.1002/jae.2873

McQueen, G., & Roley, V. V. (1993). Stock prices, news, and business conditions. *Review of Financial Studies, 6*(3), 683-707. https://doi.org/10.1093/rfs/5.3.683

Novy-Marx, R. (2014). Predicting anomaly performance with politics, the weather, global warming, sunspots, and the stars. *Journal of Financial Economics, 112*(2), 137-146. https://doi.org/10.1016/j.jfineco.2014.02.002

Sampi, J., & Jooste, C. (2020). *Nowcasting economic activity in times of COVID-19: An approximation from the Google Community Mobility Report* (Policy Research Working Paper 9247). World Bank. https://doi.org/10.1596/1813-9450-9247

Seyyed, F. J., Abraham, A., & Al-Hajji, M. (2005). Seasonality in stock returns and volatility: The Ramadan effect. *Research in International Business and Finance, 19*(3), 374-383. https://doi.org/10.1016/j.ribaf.2004.12.010

Stambaugh, R. F. (1999). Predictive regressions. *Journal of Financial Economics, 54*(3), 375-421. https://doi.org/10.1016/S0304-405X(99)00041-0

Tang, T. C. (2008). Do vehicles on highways help to predict the Malaysian stock market? *IUP Journal of Applied Economics, 7*(2), 25-30.

Thaker, H. M. T. (2022). COVID-19, mobility, and stock markets performance: Evidence from ASEAN-5. *Asian Economics Letters, 3*(4). https://doi.org/10.46557/001c.37963

Woloszko, N. (2024). Nowcasting with panels and alternative data: The OECD weekly tracker. *International Journal of Forecasting, 40*(4), 1302-1335. https://doi.org/10.1016/j.ijforecast.2023.11.005

Zhu, C. (2019). Big data as a governance mechanism. *Review of Financial Studies, 32*(5), 2021-2061. https://doi.org/10.1093/rfs/hhy081

### Data sources

ActiveConclusion. (2023). *COVID19_mobility: tomtom_reports/tomtom_trafic_index.csv* [Data set, archived daily TomTom Traffic Index values, 2019-12-30 to 2023-02-14; data remain the property of TomTom International BV]. GitHub.

Google LLC. (2022). *COVID-19 Community Mobility Reports* [Data set]. https://www.google.com/covid19/mobility/

International Monetary Fund. (2026). *International Financial Statistics* [Data set, via DBnomics].

World Bank. (2026). *Global Economic Monitor* [Data set, via DBnomics].
