import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'MANUSCRIPT_v4.md'); s = open(p, encoding='utf-8').read()
refs = """## References

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
"""
s = s[:s.index('## References')] + refs
s = s.replace("Katona et al., 2024", "Katona et al., 2025").replace("Katona et al. (2024)", "Katona et al. (2025)")
s = s.replace("Duz Tan & Tas, 2019", "Düz Tan & Taş, 2019").replace("Duz Tan and Tas, 2019", "Düz Tan & Taş, 2019").replace("Bialkowski et al.", "Białkowski et al.")
open(p, 'w', encoding='utf-8').write(s)
body = s[:s.index('## Tables')]
cited = set(re.findall(r"([A-Z][\w'\-]+(?: et al\.)?(?: & [A-Z][\w'\-]+)?),? \(?(\d{4})", body))
print("leftover verify tags:", s.count("[verify"), "| 'in this journal' mentions:", body.count("this journal"))
