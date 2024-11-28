# Datensätze importieren, umformen und zusammenführen

import pandas as pd
from scipy import stats

# Lade die CSV-Datei aus deinem lokalen Verzeichnis
wetter = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/wetter.csv')
umsatz = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/umsatzdaten_gekuerzt.csv')
kiwo = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/kiwo.csv')

# Umwandlung der 'Datum' Spalte in das Datumsformat
wetter['Datum'] = pd.to_datetime(wetter['Datum'])
umsatz['Datum'] = pd.to_datetime(umsatz['Datum'])
kiwo['Datum'] = pd.to_datetime(kiwo['Datum'])

# Den Monat aus der 'Datum' Spalte extrahieren
wetter['Monat'] = wetter['Datum'].dt.month

# Füge die Wochentag-Spalte hinzu
umsatz['Wochentag'] = umsatz['Datum'].dt.day_name()

# Definiere die Wochentagsreihenfolge
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Zuordnung von Warengruppen zu Kategorien
kategorie_mapping = {
    1: 'Brot',
    2: 'Broetchen',
    3: 'Croissant',
    4: 'Konditorei',
    5: 'Kuchen',
    6: 'Saisonbrot'
}

# Neue Spalte 'Kategorie' hinzufügen, basierend auf der Spalte 'Warengruppe'
umsatz['Kategorie'] = umsatz['Warengruppe'].map(kategorie_mapping)

# Schrittweise Zusammenführen der DataFrames mit einem Outer Join
umsatz_gesamt = pd.merge(umsatz, kiwo, on='Datum', how='outer')
umsatz_gesamt = pd.merge(umsatz_gesamt, wetter, on='Datum', how='outer')

# Sortieren nach Datum 
umsatz_gesamt = umsatz_gesamt.sort_values(by='Datum')

#Spalte "KielerWoche" umformen, sodass "1" oder "0" angezeigt wird
umsatz_gesamt['KielerWoche'] = umsatz_gesamt['KielerWoche'].apply(
    lambda x: '1' if x == 1.0 else '0'
)

# Zeilen mit NaN-Werten in der Umsatz-Spalte löschen
umsatz_gesamt = umsatz_gesamt.dropna(subset=['Umsatz'])

# Ausgabe des zusammengeführten DataFrames
print(umsatz_gesamt)

# Speichern als CSV-Datei
umsatz_gesamt.to_csv('umsatz_gesamt.csv', index=False)

# Tabelle mit one-hot-encoding codierten Wetterbeschreibungen an die Tabelle anfügen
import pandas as pd

# Beide CSV-Dateien einlesen, die mit unterschiedlichen Trennzeichen getrennt sind
umsatz_gesamt = pd.read_csv('umsatz_gesamt.csv', sep=',')
wettercodes_one_hot = pd.read_csv('/workspaces/Bakery-Project/0_DataPreparation/Data/wettercodes_one_hot.csv', sep=';')

# Überprüfen, ob die Spalten korrekt sind
print(umsatz_gesamt.head())  # Erste Zeilen des ersten DataFrames
print(wettercodes_one_hot.head())  # Erste Zeilen des zweiten DataFrames

# Entfernen von Leerzeichen in Spaltennamen
umsatz_gesamt.columns = umsatz_gesamt.columns.str.strip()
wettercodes_one_hot.columns = wettercodes_one_hot.columns.str.strip()

# Wettercode in umsatz_gesamt in Ganzzahlen umwandeln
if 'Wettercode' in umsatz_gesamt.columns:
    umsatz_gesamt['Wettercode'] = pd.to_numeric(umsatz_gesamt['Wettercode'], errors='coerce').astype('Int64')
else:
    print("Spalte 'Wettercode' fehlt in umsatz_gesamt!")

if 'Wettercode' in wettercodes_one_hot.columns:
    wettercodes_one_hot['Wettercode'] = pd.to_numeric(wettercodes_one_hot['Wettercode'], errors='coerce').astype('Int64')
else:
    print("Spalte 'Wettercode' fehlt in wettercodes_one_hot!")

# Zusammenführen der DataFrames
    umsatz_gesamt = pd.merge(
        umsatz_gesamt,
        wettercodes_one_hot,
        on='Wettercode',
        how='left'  # Alle Daten aus umsatz_gesamt behalten
    )
    print(umsatz_gesamt.head())  # Zeigt die ersten Zeilen des zusammengeführten DataFrames

# Optional speichern
umsatz_gesamt.to_csv('umsatz_gesamt.csv', sep=';', index=False)  