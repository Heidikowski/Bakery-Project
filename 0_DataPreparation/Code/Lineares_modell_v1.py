# Im Terminal vorher eingeben: pip install statsmodels 

import pandas as pd
import statsmodels.formula.api as smf

umsatz = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/umsatz_gesamt.csv')
umsatz.head()

# Fit the linear model zu Temperatur
mod = smf.ols('Umsatz ~ Warengruppe', data=umsatz).fit()
# Print the summary
print(mod.summary())

# Fit the linear model zu Temperatur
mod = smf.ols('Umsatz ~ Temperatur', data=umsatz).fit()
# Print the summary
print(mod.summary())

# Fit the linear model zu Wettercodes
mod = smf.ols('Umsatz ~ wetter_sonnig + wetter_wolken + wetter_regen + wetter_schnee + wetter_gewitter + wetter_dunst + wetter_nebel', data=umsatz).fit()
# Print the summary
print(mod.summary())

# Fit the linear model zu Wochentag
mod = smf.ols('Umsatz ~ Wochentag', data=umsatz).fit()
# Print the summary
print(mod.summary())