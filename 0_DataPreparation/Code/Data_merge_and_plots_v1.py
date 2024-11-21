import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

umsatz = pd.read_csv('/workspaces/Intro_data_science/data/umsatzdaten_gekuerzt.csv')
umsatz.head()


# Merging data frames

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
kieler_woche_data = pd.read_csv('/workspaces/Intro_data_science/data/kiwo.csv')

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
wetter_data = pd.read_csv('/workspaces/Intro_data_science/data/wetter.csv')

# Convert the 'Datum' column to datetime for consistency
wetter_data['Datum'] = pd.to_datetime(wetter_data['Datum'])

# MergeWetter data with main DataFrame
umsatz = umsatz.merge(wetter_data, on='Datum', how='left')

# Check the updated DataFrame
print(umsatz.head())




# Average Umsatz by weekday

# Plotting with confidence intervals
plt.figure(figsize=(10, 6))
plt.bar(weekday_stats.index, weekday_stats['mean'], yerr=weekday_stats['ci'], 
        color='skyblue', edgecolor='black', capsize=5, alpha=0.7)

# Add labels and title
plt.title('Average Umsatz by Weekday with 95% Confidence Intervals')
plt.xlabel('Weekday')
plt.ylabel('Average Umsatz')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# Average Umsatz during and outside Kieler Woche

# Calculate the mean, count, and standard deviation for Umsatz grouped by 'Kieler Woche'
kieler_stats = umsatz.groupby('Kieler Woche')['Umsatz'].agg(['mean', 'count', 'std'])

# Calculate the 95% confidence interval
kieler_stats['ci'] = z_score * (kieler_stats['std'] / np.sqrt(kieler_stats['count']))

# Plotting with confidence intervals
plt.figure(figsize=(8, 5))
plt.bar(
    kieler_stats.index, kieler_stats['mean'], yerr=kieler_stats['ci'], 
    color=['skyblue', 'salmon'], edgecolor='black', capsize=5, alpha=0.7
)

# Add labels and title
plt.title('Average Umsatz During and Outside Kieler Woche with 95% Confidence Intervals')
plt.xlabel('Kieler Woche')
plt.ylabel('Average Umsatz')
plt.xticks(ticks=[0, 1], labels=['No', 'Yes'], rotation=0)
plt.tight_layout()
plt.show()



# Average Umsatz by weekday during and outside Kieler Woche

# Group by Weekday and 'Kieler Woche' to calculate mean, count, and std
weekday_kieler_stats = (
    umsatz.groupby(['Weekday', 'Kieler Woche'])['Umsatz']
    .agg(['mean', 'count', 'std'])
    .reset_index()
)

# Calculate confidence intervals
weekday_kieler_stats['ci'] = (
    z_score * (weekday_kieler_stats['std'] / np.sqrt(weekday_kieler_stats['count']))
)

# Pivot the data for easier plotting
weekday_kieler_pivot = weekday_kieler_stats.pivot(
    index='Weekday', columns='Kieler Woche', values=['mean', 'ci']
)

# Ensure the weekdays are in calendar order
weekday_kieler_pivot = weekday_kieler_pivot.loc[ordered_weekdays]

# Plotting
plt.figure(figsize=(12, 6))
x = np.arange(len(ordered_weekdays))  # the label locations
width = 0.35  # the width of the bars

# Bars for "No" (Kieler Woche == 'no')
plt.bar(
    x - width/2, 
    weekday_kieler_pivot[('mean', 'no')], 
    yerr=weekday_kieler_pivot[('ci', 'no')], 
    width=width, 
    label='No', 
    color='skyblue', 
    capsize=5, 
    edgecolor='black', 
    alpha=0.7
)

# Bars for "Yes" (Kieler Woche == 'yes')
plt.bar(
    x + width/2, 
    weekday_kieler_pivot[('mean', 'yes')], 
    yerr=weekday_kieler_pivot[('ci', 'yes')], 
    width=width, 
    label='Yes', 
    color='salmon', 
    capsize=5, 
    edgecolor='black', 
    alpha=0.7
)

# Add labels, title, and legend
plt.title('Average Umsatz by Weekday During and Outside Kieler Woche with 95% Confidence Intervals')
plt.xlabel('Weekday')
plt.ylabel('Average Umsatz')
plt.xticks(x, ordered_weekdays)
plt.legend(title='Kieler Woche')
plt.tight_layout()
plt.show()



# Average Umsatz by Kategorie

# Calculate the mean, count, and standard deviation for Umsatz grouped by Kategorie
category_stats = umsatz.groupby('Kategorie')['Umsatz'].agg(['mean', 'count', 'std'])

# Calculate the 95% confidence intervals
category_stats['ci'] = z_score * (category_stats['std'] / np.sqrt(category_stats['count']))

# Plotting with confidence intervals
plt.figure(figsize=(10, 6))
plt.bar(
    category_stats.index, category_stats['mean'], yerr=category_stats['ci'], 
    color='lightgreen', edgecolor='black', capsize=5, alpha=0.8
)

# Add labels and title
plt.title('Average Umsatz by Kategorie with 95% Confidence Intervals')
plt.xlabel('Kategorie')
plt.ylabel('Average Umsatz')
plt.tight_layout()
plt.show()



# Average Umsatz by Kategorie for each weekday

# Calculate statistics grouped by Kategorie and Weekday
category_weekday_stats = (
    umsatz.groupby(['Kategorie', 'Weekday'])['Umsatz']
    .agg(['mean', 'count', 'std'])
    .reset_index()
)

# Calculate the 95% confidence intervals
category_weekday_stats['ci'] = z_score * (category_weekday_stats['std'] / np.sqrt(category_weekday_stats['count']))

# Sort weekdays in calendar order
category_weekday_stats['Weekday'] = pd.Categorical(category_weekday_stats['Weekday'], categories=ordered_weekdays, ordered=True)
category_weekday_stats.sort_values(['Kategorie', 'Weekday'], inplace=True)

# Plotting
plt.figure(figsize=(14, 8))
categories = category_weekday_stats['Kategorie'].unique()
x = np.arange(len(categories))  # label locations
width = 0.1  # width of the bars

# Loop through weekdays to plot separate bars
for i, weekday in enumerate(ordered_weekdays):
    weekday_data = category_weekday_stats[category_weekday_stats['Weekday'] == weekday]
    plt.bar(
        x + i * width, weekday_data['mean'], width, 
        yerr=weekday_data['ci'], label=weekday, capsize=5, alpha=0.8
    )

# Add labels, title, and legend
plt.title('Average Umsatz by Kategorie for Each Weekday with 95% Confidence Intervals')
plt.xlabel('Kategorie')
plt.ylabel('Average Umsatz')
plt.xticks(ticks=x + (width * 3), labels=categories)
plt.legend(title='Weekday', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()