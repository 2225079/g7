# GDP: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
# Population: https://ourworldindata.org/grapher/population

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

G7 = ["United States", "Germany", "Japan", "United Kingdom", "France", "Italy", "Canada"]

_gdp, _pop = pd.read_csv("data/gdp.csv"), pd.read_csv("data/population.csv")
gdp, pop = _gdp[["year"] + G7], _pop[["year"] + G7]

pop[G7] = pop[G7].astype(float)

gdp.loc[:, G7] = gdp.loc[:, G7].apply(lambda v: v / 1e12)
pop.loc[:, G7] = pop.loc[:, G7].apply(lambda v: v / 1e6)

fig = plt.figure(figsize=(16, 9))

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

print("GDP-Population corr:")
for country in G7:
    ax1.plot(gdp["year"], gdp[country], label=country)
    ax2.plot(pop["year"], pop[country], label=country)
    print(f"{country.rjust(max([len(w) for w in G7]))}: {round(np.corrcoef(gdp[country], pop[country])[0][1], 3):.3f}")

ax1.set_title("GDP")
ax1.set_xlim([gdp["year"][0], gdp["year"].iat[-1]])
ax1.set_xlabel("A.D.")
ax1.set_ylabel("Trillion USD")
ax1.grid()
ax1.legend()
ax1.set_yscale("log")

ax2.set_title("Populations")
ax2.set_xlim([pop["year"][0], pop["year"].iat[-1]])
ax2.set_xlabel("A.D.")
ax2.set_ylabel("Million people")
ax2.grid()
ax2.legend()

fig.suptitle("Historical GDP and Populations of G7", fontsize=12)
fig.tight_layout()

plt.savefig("out/out.png", dpi=350)
