# WeatherHistory

Historische Wetterdaten abrufen und interaktiv visualisieren – powered by [Open-Meteo](https://open-meteo.com/) und [Dash/Plotly](https://dash.plotly.com/).

## Überblick

Dieses Projekt lädt stündliche Wetterdaten der Open-Meteo Archiv-API für beliebige Standorte herunter, aggregiert sie zu Tageswerten und stellt sie in einem interaktiven Web-Dashboard dar. Aktuell konfiguriert für **Wien**, **Casablanca**, **Medina**, **Rom**, **Lissabon**, **Santiago de Chile**, **Los Angeles** und **Oslo**.

## Voraussetzungen

- Python 3.13+
- Abhängigkeiten installieren:

```bash
pip install requests dash plotly pandas numpy
```

## Verwendung

### 1. Wetterdaten abrufen

```bash
python3 WeatherHistoryWien.py
python3 WeatherHistoryCasablanca.py
python3 WeatherHistoryMedina.py
python3 WeatherHistoryRome.py
python3 WeatherHistoryLisbon.py
python3 WeatherHistorySantiago.py
python3 WeatherHistoryLosAngeles.py
python3 WeatherHistoryOslo.py
```

Erzeugt jeweils eine CSV-Datei mit täglichen Min/Max/Durchschnittswerten für Strahlung, Temperatur, Luftfeuchtigkeit, Luftdruck, Bewölkung und Niederschlag.

### 2. Dashboard starten

```bash
python3 StrahlungDashAlle.py        # http://localhost:8055
```

## Screenshot

![Wetterdaten Medina – Strahlung Monatsmittel](screenshot_medina.png)

## Dashboard-Inhalte

Stadt per Dropdown auswählen, Light/Dark-Theme per Schaltfläche umschalten. Acht Tabs:

| Tab | Inhalt |
| --- | --- |
| Strahlung Monatsmittel | Ø kWh/m² pro Kalendermonat über alle Jahre |
| Strahlung nach Jahr | Monatliche kWh/m² für ein wählbares Jahr |
| Strahlung Zeitreihe | Alle Monate als Balkendiagramm mit Range-Slider |
| Strahlung Jahressummen | Jährliche Gesamtstrahlung mit Durchschnittslinie |
| Temperaturen | Monatliche Ø-Temperatur, gesamt oder nach Jahr |
| Niederschlag | Monatlicher Niederschlag in mm mit Jahressumme |
| Temp. Jahrestrend | Jährliche Ø-Temperatur mit linearem Fit (°C/Dekade) |
| Niederschlag Jahrestrend | Jährlicher Gesamtniederschlag mit linearem Fit (mm/Dekade) |

## Neue Stadt hinzufügen

1. `WeatherHistoryXxx.py` anlegen:

```python
from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=...,
        longitude=...,
        timezone="Continent/City",
        filename="xxx_wetter.csv",
        start_date="1980-01-01",
    )
```

2. Eintrag in `STAEDTE`-Dict in `StrahlungDashAlle.py` hinzufügen (Farben, Temperaturschwellen, Dateiname).
3. Fetch-Script ausführen, dann Dashboard neu starten.

## Projektstruktur

```text
weather_fetch.py          # Library: Datenabruf via Open-Meteo API
weather_dash_lib.py       # Library: Datenaggregation (load_data)
StrahlungDashAlle.py      # Kombiniertes Dashboard (Port 8055)
assets/theme.css          # CSS für Light/Dark-Theme
WeatherHistoryWien.py        # Wien (48.2°N, 16.4°E)
WeatherHistoryCasablanca.py  # Casablanca (33.6°N, 7.6°W)
WeatherHistoryMedina.py      # Medina (24.5°N, 39.6°E)
WeatherHistoryRome.py        # Rom (41.9°N, 12.5°E)
WeatherHistoryLisbon.py      # Lissabon (38.7°N, 9.1°W)
WeatherHistorySantiago.py    # Santiago de Chile (33.4°S, 70.7°W)
WeatherHistoryLosAngeles.py  # Los Angeles (34.1°N, 118.2°W)
WeatherHistoryOslo.py        # Oslo (59.9°N, 10.8°E)
```

## Datenquelle

[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) – kostenlos, keine Registrierung erforderlich. Daten ab 1940 verfügbar.
