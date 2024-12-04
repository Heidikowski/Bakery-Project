# Im Terminal vorher eingeben: pip install statsmodels 

import pandas as pd
import statsmodels.formula.api as smf

umsatz = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/umsatz_gesamt.csv')
umsatz.head()
print(umsatz)

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

mod = smf.ols('Umsatz ~ Wochentag + C(Warengruppe) + C(KielerWoche) + C(Monat) + C(wetter_sonnig) + C(wetter_wolken) + C(wetter_regen) + C(wetter_schnee) + C(wetter_gewitter) + C(wetter_dunst) + C(wetter_nebel)', data=umsatz).fit()
# Print the summary
print(mod.summary())