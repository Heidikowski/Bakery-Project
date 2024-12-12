# Im Terminal vorher eingeben: pip install statsmodels 

import pandas as pd
import statsmodels.formula.api as smf

umsatz = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/umsatz_gesamt_feiertage.csv')
umsatz.head()
print(umsatz)
umsatz.columns

bins = [-10, 10, 20, 35]  
labels = ['Kalt', 'Moderat', 'Warm', ]

# Temperatur-Bins der Spalte hinzufügen
umsatz['Temperatur_Bin'] = pd.cut(umsatz['Temperatur'], bins=bins, labels=labels, include_lowest=True)

# Kontrolle der Verteilung in den Bins
print(umsatz['Temperatur_Bin'].value_counts())

print(umsatz.head())

umsatz.columns


# we want to maximize Adj. R-squared ideal close to 1 because it tells us how much of the variance is explained
# coef tells us how much the value moves if the dependet value increases by 1
# last 2 columns are the 95% confidence interval
# 'Umsatz' is the dependent variable (target) we aim to predict
# 'Wochentag' is the continuous feature
# 'C(condition)' treats the 'Warengruppe' feature as a categorical variable.

# Fit the linear model
mod = smf.ols('Umsatz ~ Wochentag + C(Warengruppe) + C(KielerWoche)', data=umsatz).fit()
# Print the summary
print(mod.summary())

# Everything except Kategorie, Bewoelkung, Temperatur, Windgeschwindigkeit, Wettercode and Temperatur_Bin
mod = smf.ols('Umsatz ~ Wochentag + C(Warengruppe) + C(KielerWoche) + C(Monat) + C(wetter_sonnig) + C(wetter_wolken) + C(wetter_regen) + C(wetter_schnee) + C(wetter_gewitter) + C(wetter_dunst) + C(wetter_nebel) + C(sunday_or_holiday)', data=umsatz).fit()
# Print the summary
print(mod.summary())

# Everything except Kategorie, Bewoelkung, Temperatur, Windgeschwindigkeit, Wettercode
mod = smf.ols('Umsatz ~ Wochentag + C(Warengruppe) + C(KielerWoche) + C(Monat) + C(wetter_sonnig) + C(wetter_wolken) + C(wetter_regen) + C(wetter_schnee) + C(wetter_gewitter) + C(wetter_dunst) + C(wetter_nebel) + C(sunday_or_holiday) + C(Temperatur_Bin)', data=umsatz).fit()
# Print the summary
print(mod.summary())