# WeatherHistory

Historische Wetterdaten abrufen und interaktiv visualisieren – powered by [Open-Meteo](https://open-meteo.com/) und [Dash/Plotly](https://dash.plotly.com/).

## Überblick

Dieses Projekt lädt stündliche Wetterdaten der Open-Meteo Archiv-API für beliebige Standorte herunter, aggregiert sie zu Tageswerten und stellt sie in interaktiven Web-Dashboards dar. Aktuell konfiguriert für **Wien**, **Casablanca**, **Medina**, **Rom** und **Lissabon**.

## Voraussetzungen

- Python 3.13+
- Abhängigkeiten installieren:

```bash
pip install requests dash plotly pandas
```

## Verwendung

### 1. Wetterdaten abrufen

```bash
python3 WeatherHistoryWien.py
python3 WeatherHistoryCasablanca.py
python3 WeatherHistoryMedina.py
python3 WeatherHistoryRome.py
python3 WeatherHistoryLisbon.py
```

Erzeugt jeweils eine CSV-Datei mit täglichen Min/Max/Durchschnittswerten für Strahlung, Temperatur, Luftfeuchtigkeit, Luftdruck, Bewölkung und Niederschlag.

### 2. Dashboard starten

```bash
python3 StrahlungDashWien.py        # http://localhost:8050
python3 StrahlungDashCasablanca.py  # http://localhost:8051
python3 StrahlungDashMedina.py      # http://localhost:8052
python3 StrahlungDashRome.py        # http://localhost:8053
python3 StrahlungDashLisbon.py      # http://localhost:8054
```

Alle Dashboards können gleichzeitig laufen.

## Screenshot

![Wetterdaten Medina – Strahlung Monatsmittel](screenshot_medina.png)

## Dashboard-Inhalte

Jedes Dashboard bietet sechs Tabs:

| Tab | Inhalt |
| --- | --- |
| Strahlung Monatsmittel | Ø kWh/m² pro Kalendermonat über alle Jahre |
| Strahlung nach Jahr | Monatliche kWh/m² für ein wählbares Jahr |
| Strahlung Zeitreihe | Alle Monate als Balkendiagramm mit Range-Slider |
| Strahlung Jahressummen | Jährliche Gesamtstrahlung mit Durchschnittslinie |
| Temperaturen | Monatliche Ø-Temperatur, gesamt oder nach Jahr |
| Niederschlag | Monatlicher Niederschlag in mm mit Jahressumme |

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
    )
```

1. `StrahlungDashXxx.py` anlegen:

```python
from weather_dash_lib import create_app

app = create_app({
    "filename":                "xxx_wetter.csv",
    "title":                   "Wetterdaten Xxx",
    "city":                    "Xxx",
    "h1_color":                "#xxxxxx",
    "strahlung_colorscale":    "YlOrRd",   # Plotly-Farbskala
    "bar_voll_color":          "#xxxxxx",
    "bar_aktuell_color":       "#xxxxxx",
    "precip_color":            "#xxxxxx",
    "precip_annotation_color": "#xxxxxx",
    "precip_annotation_bg":    "#xxxxxx",
    "temp_cold_threshold":     10,          # °C – unter diesem Wert: kalte Farbe
    "temp_hot_threshold":      30,          # °C – über diesem Wert: heiße Farbe
    "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    "port":                    8053,
})

if __name__ == "__main__":
    app.run(debug=True, port=8053)
```

1. Fetch-Script ausführen, dann Dashboard starten.

## Projektstruktur

```text
weather_fetch.py          # Library: Datenabruf via Open-Meteo API
weather_dash_lib.py       # Library: Dash-App-Factory mit allen Tabs & Callbacks
WeatherHistoryWien.py       # Wien: Datenabruf (48.2°N, 16.4°E)
WeatherHistoryCasablanca.py # Casablanca (33.6°N, 7.6°W)
WeatherHistoryMedina.py     # Medina (24.5°N, 39.6°E)
WeatherHistoryRome.py       # Rom (41.9°N, 12.5°E)
WeatherHistoryLisbon.py     # Lissabon (38.7°N, 9.1°W)
StrahlungDashWien.py        # Wien: Dashboard (Port 8050)
StrahlungDashCasablanca.py  # Casablanca (Port 8051)
StrahlungDashMedina.py      # Medina (Port 8052)
StrahlungDashRome.py        # Rom (Port 8053)
StrahlungDashLisbon.py      # Lissabon (Port 8054)
```

## Datenquelle

[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) – kostenlos, keine Registrierung erforderlich. Daten ab 1940 verfügbar.
