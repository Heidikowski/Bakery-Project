import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

umsatz = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/umsatzdaten_gekuerzt.csv')
umsatz.head()



### Merging data frames to complete data frame with all the data

#Zuordnung von Warengruppen zu Kategorien
kategorie_mapping = {
    1: 'Brot',
    2: 'Broetchen',
    3: 'Croissant',
    4: 'Konditorei',
    5: 'Kuchen',
    6: 'Saisonbrot'
}
#Neue Spalte 'Kategorie' hinzufügen, basierend auf der Spalte 'Warengruppe'
umsatz['Kategorie'] = umsatz['Warengruppe'].map(kategorie_mapping)
#Überprüfen, ob die Zuordnung korrekt durchgeführt wurde
print(umsatz.head())

# Convert the 'Datum' column to datetime format to work with dates
umsatz['Datum'] = pd.to_datetime(umsatz['Datum'])

# Extract the weekday name and add it as a new column
umsatz['Weekday'] = umsatz['Datum'].dt.day_name()

# Calculate the mean and standard error for each weekday
weekday_stats = umsatz.groupby('Weekday')['Umsatz'].agg(['mean', 'count', 'std'])

# Calculate the 95% confidence interval
confidence_level = 0.95
z_score = stats.norm.ppf((1 + confidence_level) / 2)  # z-score for 95% confidence
weekday_stats['ci'] = z_score * (weekday_stats['std'] / np.sqrt(weekday_stats['count']))

# Sort weekdays in calendar order
ordered_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_stats = weekday_stats.reindex(ordered_weekdays)

# Implement Kieler Woche data
kieler_woche_data = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/kiwo.csv')

# Convert the 'Datum' column to datetime for consistency
kieler_woche_data['Datum'] = pd.to_datetime(kieler_woche_data['Datum'])

# Merge Kieler Woche data with main DataFrame
umsatz = umsatz.merge(kieler_woche_data, on='Datum', how='left')

# Add the 'Kieler Woche' column
umsatz['Kieler Woche'] = umsatz['KielerWoche'].apply(lambda x: 'yes' if x == 1 else 'no')

# Drop the temporary 'KielerWoche' column
umsatz.drop(columns=['KielerWoche'], inplace=True)

# Check the updated DataFrame
print(umsatz.head())

# Implement Wetter data
wetter_data = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/wetter.csv')

# Convert the 'Datum' column to datetime for consistency
wetter_data['Datum'] = pd.to_datetime(wetter_data['Datum'])

# MergeWetter data with main DataFrame
umsatz = umsatz.merge(wetter_data, on='Datum', how='left')

# Check the updated DataFrame
print(umsatz.head())

# Save the final DataFrame to a CSV file
umsatz.to_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/final_umsatz.csv', index=False)




### One hot encoding with weather codes
pd.get_dummies(umsatz, columns=['Wettercode'], prefix='Wetter')

counts = umsatz['Wettercode'].value_counts()
print(counts)