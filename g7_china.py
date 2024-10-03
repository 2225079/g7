# GDP: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
# Population: https://ourworldindata.org/grapher/population
# Working age population: https://fred.stlouisfed.org

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

COUNTRIES = ["U.S.", "China", "Germany", "Japan", "U.K.", "France", "Italy", "Canada"]
COLORS = ['r', 'g', 'b', 'c', 'm', 'y', 'k', "#234512"]

_gdp, _pop, _wap = pd.read_csv("data/gdp.csv"), pd.read_csv("data/population.csv"), pd.read_csv("data/working_age_population.csv")
gdp, pop, wap = _gdp[["year"] + COUNTRIES], _pop[["year"] + COUNTRIES], _wap[["year"] + COUNTRIES]

gdp_per_wap = wap.copy()
gdp_per_wap[COUNTRIES] = gdp[COUNTRIES] / gdp_per_wap[COUNTRIES]

print("corr. between GDP and population:")
for country in COUNTRIES:
    print(f"{country.rjust(max([len(w) for w in COUNTRIES]))}: {round(np.corrcoef(gdp[country], pop[country])[0][1], 3): .3f} -- {gdp['year'][0]}-{gdp['year'].iat[-1]} ({gdp['year'].iat[-1] - gdp['year'][0] + 1} yrs)")

print()
print("corr. between GDP and working age population:")
for country in COUNTRIES:
    bound = wap[["year", country]].dropna(how="any")["year"].min()
    print(f"{country.rjust(max([len(w) for w in COUNTRIES]))}: {round(np.corrcoef(gdp[gdp['year'] >= bound][country], wap[wap['year'] >= bound][country])[0][1], 3): .3f} -- {bound}-{wap['year'].iat[-1]} ({wap['year'].iat[-1] - bound + 1} yrs)")

pop[COUNTRIES], wap[COUNTRIES] = pop[COUNTRIES].astype(float), wap[COUNTRIES].astype(float)

gdp.loc[:, COUNTRIES] = gdp.loc[:, COUNTRIES].apply(lambda v: v / 1e12)
pop.loc[:, COUNTRIES] = pop.loc[:, COUNTRIES].apply(lambda v: v / 1e6)
wap.loc[:, COUNTRIES] = wap.loc[:, COUNTRIES].apply(lambda v: v / 1e6)
gdp_per_wap.loc[:, COUNTRIES] = gdp_per_wap.loc[:, COUNTRIES].apply(lambda v: v / 1e3)

fig1 = plt.figure(figsize=(16, 9))

ax1_1 = fig1.add_subplot(1, 1, 1)
ax1_2 = ax1_1.twinx()

for i, country in enumerate(COUNTRIES):
    ax1_1.plot(gdp["year"], gdp[country], label=country, color=COLORS[i])
    ax1_2.plot(gdp_per_wap["year"], gdp_per_wap[country], "--", color=COLORS[i])

ax1_1.set_title("GDP and GDP Per Working Ages (Note: Semilog Graph)")
ax1_1.set_xlim([gdp["year"][0], gdp["year"].iat[-1]])
ax1_1.set_xlabel("A.D.")
ax1_1.set_ylabel("Trillion USD (GDP)")
ax1_1.grid()
ax1_1.legend()
ax1_1.set_yscale("log")

ax1_2.set_ylabel("Thousand USD (GDP per working ages)")
ax1_2.set_ylim([1e-1, 1e2])
ax1_2.set_yscale("log")

plt.savefig("out/gdp.png", dpi=350)

fig2 = plt.figure(figsize=(16, 9))
ax2_1 = fig2.add_subplot(1, 1, 1)
ax2_2 = ax2_1.twinx()

for i, country in enumerate(COUNTRIES):
    # If you remove the plot of China on ax2_1, "China" will not be listed in the legend.
    ax2_1.plot(pop["year"], pop[country], label=country, color=COLORS[i])
    ax2_1.plot(wap["year"], wap[country], "--", color=COLORS[i])

    if country == "China":
        ax2_2.plot(pop["year"], pop[country], label=country, color=COLORS[i])
        ax2_2.plot(wap["year"], wap[country], "--", color=COLORS[i])

ax2_1.set_title("Population and Working Age Population")
ax2_1.set_xlim([1960, 2023])
ax2_1.set_ylim([0, 300])
ax2_1.set_xlabel("A.D.")
ax2_1.set_ylabel("Million people (G7)")
ax2_1.grid()
ax2_1.legend(loc='upper left')

ax2_2.set_ylim([500, 1500])
ax2_2.yaxis.set_major_locator(ticker.MultipleLocator(250))
ax2_2.set_ylabel("Million people (China)")
ax2_2.grid()

plt.savefig("out/pop.png", dpi=350)
