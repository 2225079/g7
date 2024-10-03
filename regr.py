import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

G7 = ["U.S.", "Germany", "Japan", "U.K.", "France", "Italy", "Canada"] # removed "China"
COLORS = ['r', 'b', 'c', 'm', 'y', 'k', "#234512"] # removed 'g'

_gdp, _wap = pd.read_csv("data/gdp.csv"), pd.read_csv("data/working_age_population.csv")
gdp, wap = _gdp[["year"] + G7], _wap[["year"] + G7]

wap[G7] = wap[G7].astype(float)

gdp.loc[:, G7] = gdp.loc[:, G7].apply(lambda v: v / 1e12)
wap.loc[:, G7] = wap.loc[:, G7].apply(lambda v: v / 1e6)

fig = plt.figure(figsize=(16, 9))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

bound = wap[["year", "Japan"]].dropna(how="any")["year"].min()
x = wap[wap["year"] >= bound]["Japan"]
y = gdp[gdp["year"] >= bound]["Japan"]

lr = LinearRegression()
lr.fit(np.array(x.values).reshape(-1, 1), y.values)

ax1.plot(x, y, '.', label="Japan")
ax1.plot(x, lr.predict(np.array(x.values).reshape(-1, 1)), linestyle="solid")

bound = wap[["year", "Canada"]].dropna(how="any")["year"].min()
x = wap[wap["year"] >= bound]["Canada"]
y = gdp[gdp["year"] >= bound]["Canada"]
lr = LinearRegression()
lr.fit(np.array(x.values).reshape(-1, 1), y.values)

ax2.plot(x, y, '.', label="Canada")
ax2.plot(x, lr.predict(np.array(x.values).reshape(-1, 1)), linestyle="solid")

ax1.set_xlabel("Million people (working age population)")
ax1.set_ylabel("Trillion USD (GDP)")
ax1.legend()
ax1.grid()

ax2.set_xlabel("Million people (working age population)")
ax2.set_ylabel("Trillion USD (GDP)")
ax2.legend()
ax2.grid()

plt.savefig("out/regr.png", dpi=350)
