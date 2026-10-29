import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'MANUSCRIPT_v4.md'); s = open(p, encoding='utf-8').read(); miss = []

def R(old, new):
    global s
    pat = re.escape(old).replace(r'\ ', r'\s+'); s2, n = re.subn(pat, lambda m: new, s, count=1)
    if n == 0: miss.append(old[:60])
    s = s2

R("Draft v4, 2026-10-28. Submission-form draft: tables at the end, figures as separate files.", "")
R("Panel A shows that the interaction is 0.31 (t = 3.3) with country-by-month effects alone and remains between 0.24 and 0.30 (t = 2.9 to 4.0, the last with Driscoll-Kraay errors) as state-by-month effects, year and country-by-year effects, holiday dummies, state-interacted controls and the log VIX level are added; fixed effects do not remove it. In specification (1) the calm-state coefficient is -0.054 (t = -1.8) and the interaction 0.259 (t = 3.7), 0.273 (t = 3.8) with the stringency and fuel controls:",
  "Panel A shows that the interaction is 0.31 (t = 3.3) with country-by-month effects alone and remains between 0.24 and 0.30 (t = 2.9 to 4.0, the last with Driscoll-Kraay errors) as state-by-month effects, year and country-by-year effects, holiday dummies, state-interacted controls and the log VIX level are added on top of the country-by-month effects; fixed effects do not remove it. Specification (1), which replaces the country-by-month effects with country-by-year and state-by-month effects, gives a calm-state coefficient of -0.054 (t = -1.8) and an interaction of 0.259 (t = 3.7), 0.273 (t = 3.8) with the stringency and fuel controls:")
R("Panel A adds controls cumulatively; L6 is equation (1). Standard errors clustered by week; L7 uses Driscoll-Kraay(4).",
  "Panel A adds controls cumulatively on top of country-by-calendar-month effects; equation (1), reported in Panel B, replaces the country-by-month effects with country-by-year and state-by-month effects. Standard errors clustered by week; L7 uses Driscoll-Kraay(4).")
R("Panel B. Signal versions, equation (1) with stringency and fuel controls\n\n| Version | N | x, calm | t | x × S | t |\n|---|---|---|---|---|---|\n| Actual signal | 1518 | -0.057 | -1.90 | 0.273 | 3.76 |\n| Actual signal, placebo sample | 1098 | -0.028 | -0.81 | 0.189 | 2.57 |\n| Signal lagged 52 weeks | 1098 | 0.027 | 0.78 | 0.078 | 1.16 |\n| Real-time seasonal difference | 1098 | -0.043 | -1.35 | 0.037 | 0.54 |",
  "Panel B. Signal versions, equation (1); with the stringency and fuel controls added, the interactions are 0.273 (t 3.76), 0.078 (t 1.16) and 0.037 (t 0.54) for the actual, lagged and differenced signals\n\n| Version | N | x, calm | t | x × S | t |\n|---|---|---|---|---|---|\n| Actual signal | 1518 | -0.054 | -1.83 | 0.259 | 3.69 |\n| Actual signal, placebo sample | 1098 | -0.028 | -0.81 | 0.189 | 2.57 |\n| Signal lagged 52 weeks | 1098 | 0.025 | 0.74 | 0.082 | 1.22 |\n| Real-time seasonal difference | 1098 | -0.036 | -1.09 | 0.049 | 0.67 |")
R("Panel C. Calendar decomposition, equation (1) without stringency and fuel", "Panel C. Calendar decomposition, equation (1); the circular-shift placebo is benchmarked against the 0.259 (t 3.69) estimate")
R("and absent by every test in Turkey, India, Indonesia and Malaysia, where Ramadan and other moving holidays shift by eleven days a year and do not align week to week. For those countries the explicit holiday dummies, not a seasonal filter, are the relevant safeguard.",
  "while in Turkey, India, Indonesia and Malaysia, where Ramadan and other moving holidays shift by eleven days a year and do not align week to week, the 52-week autocorrelation is near zero; a smooth seasonal is nonetheless significant in India, Malaysia and, marginally, Indonesia, and absent only in Turkey. For moving-holiday countries the explicit holiday dummies, not a seasonal filter, are the relevant safeguard.")
R("and are found by neither statistic, as the Turkish and Indian series show.", "and can escape both statistics, as the Turkish series shows.")
R("The 2022 pattern is a pre-registered hypothesis.", "The 2022 pattern is recorded as a hypothesis we pre-register (Appendix B).")
R("(Appendix B; the pre-registration will be deposited with a time stamp before submission).", "(Appendix B).")
R("simulating returns that respond only to the actual signal, with noise calibrated to the observed fit, the ratio of the placebo to the actual coefficient has a median of 0.12 but a 5-95 percent range from -1.5 to 1.7, and 21 percent of such simulations produce a seasonal-difference ratio at or below the observed one.",
  "simulating returns that respond only to the actual signal, with noise calibrated to the observed fit on the 946 country-weeks that have the lagged signal and all controls (where the actual interaction is 0.157, t = 2.0, the lagged placebo 0.109, t = 1.8, and the seasonal difference -0.009), the ratio of the placebo to the actual coefficient has a median of 0.12 but a 5-95 percent range from -1.5 to 1.7, and 21 percent of such simulations produce a seasonal-difference ratio at or below the observed one (Appendix A6).")
R("In-sample deseasonalization, removing full-sample month-of-year means, preserves the result (0.257, t = 3.0) because it leaves most of that structure in place,", "In-sample deseasonalization by full-sample month-of-year means preserves the result (0.257, t = 3.0, with country-by-month effects) because it leaves most of the week-level structure in place,")
R("**Table 1. Sample and descriptive statistics, ex-lockdown weeks (July 2020 to February 2023).**", "**Table 1. Sample and descriptive statistics, January 2020 to February 2023 excluding March-June 2020 (147 weeks per country; regressions that need lagged signals use 138).**")
R("Appendix Table A5 shows that adding all three leaves every result in the paper unchanged.", "Appendix Table A5 shows that adding all three leaves the Table 6 interaction and the volatility coefficient within their ranges.")
R("the usable content is in volatility: activity surprises lower next-week variance,", "the usable content is in volatility: negative activity surprises raise next-week variance,")
R("In the state-dependent specification estimated for Turkey alone the interaction is -0.28 (t = -1.4),", "In the state-dependent specification estimated for Turkey alone, with calendar-month effects and HAC errors, the interaction is -0.28 (t = -1.4),")
R("the stringency change and the fuel-price proxy of Section 3.5 are added", "the stringency change and the fuel-price proxy of Section 2.5 are added")
R("the volatility coefficient is -0.06 to -0.08 (t -2.5 to -2.6); in single-city countries alone it is -0.05 (t -1.2).", "the volatility coefficient, in the specification without holiday dummies, is -0.06 to -0.08 (t -2.5 to -2.6); in single-city countries alone it is -0.05 (t -1.2).")
R("The nowcasting exercise targets month-on-month growth", "The nowcasting exercise, in the spirit of the mobility-based nowcasts of Sampi and Jooste (2020) and the elasticity estimates of Gamtkitsulashvili and Plekhanov (2023), targets month-on-month growth")
R("the weekly change in the Oxford stringency index and the lagged weekly change", "the weekly change in the Oxford stringency index (Hale et al., 2021) and the lagged weekly change")
R("holiday dummies H (the Ramadan month", "holiday dummies H (Appendix Table A2: the Ramadan month")
R("is strongest in the countries with the most cities and the densest road coverage, and is weakest where", "is strongest in Brazil, South Africa, Poland, Egypt and Turkey, and is weakest where")
R("no country is significant at the 5 percent level in any of the three versions,", "no country's local-index coefficient is significant at the 5 percent level in any of the three versions,")
R("we have collected it for all 490 cities since 21 October 2026", "we have collected it for all 490 cities in the current index, more than the 414 in the archive, since 21 October 2026")
R(" Table 6, Panel A reports the ladder from country-by-month effects alone to this specification. We also add,", "\n\nTable 6, Panel A reports the ladder from country-by-month effects alone to this specification. We also add,")
R(" Each design is estimated with the actual signal, the 52-week-lagged placebo and the real-time seasonal difference. The volatility regression", "\n\nEach design is estimated with the actual signal, the 52-week-lagged placebo and the real-time seasonal difference. The volatility regression")
# APA: ampersand in parenthetical two-author citations; et al. for 3+
body_end = s.index('## References')
body, refs = s[:body_end], s[body_end:]
body = re.sub(r"\(([A-Z][\w'-]+) and ([A-Z][\w'-]+), (\d{4})\)", r"(\1 & \2, \3)", body)
body = re.sub(r"([A-Z][\w'-]+) and ([A-Z][\w'-]+), (\d{4})(?=[;)])", r"\1 & \2, \3", body)
for a in ["Lewis, Mertens, Stock and Trivedi", "Beyer, Franco-Bedoya and Galdo", "Froot, Kang, Ozik and Sadka", "Katona, Painter, Patatoukas and Zeng", "Harvey, Liu and Zhu", "Keloharju, Linnainmaa and Nyberg", "Ferson, Sarkissian and Simin", "Hirshleifer, Jiang and DiGiovanni", "Bialkowski, Etebari and Wisniewski", "Seyyed, Abraham and Al-Hajji", "Lazer, Kennedy, King and Vespignani", "Cao, Qian and Zhang", "Boyd, Hu and Jagannathan"]:
    first = a.split(",")[0]
    body = body.replace(a + ",", first + " et al.,").replace(a + " (", first + " et al. (")
body = body.replace("Eraslan & Gotz", "Eraslan & Götz").replace("Eraslan and Gotz", "Eraslan & Götz")
s = body + refs
open(p, 'w', encoding='utf-8').write(s)
print("misses:", miss if miss else "none"); print("body words:", len(re.findall(r"\w+", s[:s.index('## Tables')])))
