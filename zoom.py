import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

G7 = ["U.S.", "Germany", "Japan", "U.K.", "France", "Italy", "Canada"] # removed "China"
COLORS = ['r', 'b', 'c', 'm', 'y', 'k', "#234512"] # removed 'g'

_gdp, _pop, _wap = pd.read_csv("data/gdp.csv"), pd.read_csv("data/population.csv"), pd.read_csv("data/working_age_population.csv")
gdp, pop, wap = _gdp[["year"] + G7], _pop[["year"] + G7], _wap[["year"] + G7]

gdp_per_wap = wap.copy()
gdp_per_wap[G7] = gdp[G7] / gdp_per_wap[G7]

pop[G7], wap[G7] = pop[G7].astype(float), wap[G7].astype(float)

gdp.loc[:, G7] = gdp.loc[:, G7].apply(lambda v: v / 1e12)
pop.loc[:, G7] = pop.loc[:, G7].apply(lambda v: v / 1e6)
wap.loc[:, G7] = wap.loc[:, G7].apply(lambda v: v / 1e6)
gdp_per_wap.loc[:, G7] = gdp_per_wap.loc[:, G7].apply(lambda v: v / 1e3)

fig = plt.figure(figsize=(16, 9))

ax = fig.add_subplot(1, 1, 1)

for i, country in enumerate(G7):
    ax.plot(gdp_per_wap["year"], gdp_per_wap[country], color=COLORS[i], label=country)

ax.set_ylabel("Thousand USD (GDP per working ages)")
ax.set_xlim([2005, 2023])
ax.set_ylim([20, 90])
ax.legend(loc='upper left')
ax.grid()

plt.savefig("out/zoom.png", dpi=350)
