# Im Terminal vorher eingeben: pip install statsmodels 

import pandas as pd
import statsmodels.formula.api as smf

umsatz = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/final_umsatz.csv')
umsatz.head()

# Fit the linear model
mod = smf.ols('Umsatz ~ Temperatur', data=umsatz).fit()
# Print the summary
print(mod.summary())