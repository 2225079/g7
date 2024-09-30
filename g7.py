import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

g7 = ["United States", "Germany", "Japan", "United Kingdom", "France", "Italy", "Canada"]

_gdp, _pop = pd.read_csv("data/gdp.csv"), pd.read_csv("data/population.csv")
gdp, pop = _gdp[["year"] + g7], _pop[["year"] + g7]

gdp.loc[:, g7] = gdp.loc[:, g7].apply(lambda v: v / 10**9)
pop.loc[:, g7] = pop.loc[:, g7].apply(lambda v: v / 10**6)

fig = plt.figure(figsize=(16, 9))

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

for country in g7:
    ax1.plot(gdp["year"], gdp[country], label=country)
    ax2.plot(pop["year"], pop[country], label=country)

ax1.set_title("G7 GDP")
ax1.set_xlim([gdp["year"][0], gdp["year"].iat[-1]])
ax1.set_xlabel("Years")
ax1.set_ylabel("Billion USD")
ax1.grid()
ax1.legend()
ax1.set_yscale("log")

ax2.set_title("G7 Populations")
ax2.set_xlim([pop["year"][0], pop["year"].iat[-1]])
ax2.set_xlabel("Years")
ax2.set_ylabel("Million people")
ax2.grid()
ax2.legend()

fig.tight_layout()

plt.savefig("out/out.png", dpi=350)
