# WeatherHistory

Historische Wetterdaten abrufen und interaktiv visualisieren – powered by [Open-Meteo](https://open-meteo.com/) und [Dash/Plotly](https://dash.plotly.com/).

## Überblick

Dieses Projekt lädt stündliche Wetterdaten der Open-Meteo Archiv-API für beliebige Standorte herunter, aggregiert sie zu Tageswerten und stellt sie in einem interaktiven Web-Dashboard dar. Aktuell konfiguriert für **19 Städte** auf allen Kontinenten:

| Kontinent | Städte |
| --- | --- |
| Europa | Wien, Rom, Lissabon, Oslo, Dublin |
| Afrika | Casablanca, Lagos, Nairobi |
| Asien | Medina, Tokyo, Shanghai, Mumbai, Yakutsk |
| Amerika | Santiago, Los Angeles, Las Vegas, New York |
| Ozeanien | Canberra, Wellington |

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
python3 WeatherHistoryLasVegas.py
python3 WeatherHistoryNewYork.py
python3 WeatherHistoryOslo.py
python3 WeatherHistoryTokyo.py
python3 WeatherHistoryShanghai.py
python3 WeatherHistoryMumbai.py
python3 WeatherHistoryDublin.py
python3 WeatherHistoryCanberra.py
python3 WeatherHistoryWellington.py
python3 WeatherHistoryYakutsk.py
python3 WeatherHistoryLagos.py
python3 WeatherHistoryNairobi.py
```

Erzeugt jeweils eine CSV-Datei mit täglichen Min/Max/Durchschnittswerten für Strahlung, Temperatur, Luftfeuchtigkeit, Luftdruck, Bewölkung und Niederschlag.

### 2. Dashboard starten

```bash
python3 StrahlungDashAlle.py        # http://localhost:8055
```

## Dashboard-Bedienung

Das Dashboard öffnet sich automatisch im Browser unter `http://localhost:8055`.

Die Steuerelemente befinden sich kompakt oben links, die interaktive Weltkarte oben rechts:

- **Kontinent / Stadt** – Auswahl der anzuzeigenden Stadt (auch per Klick auf die Karte)
- **Ansicht** – Dropdown-Menü zur Auswahl der Darstellung
- **Jahr** – erscheint kontextabhängig für jahresspezifische Ansichten
- **Light/Dark-Theme** – Schaltfläche oben rechts

| Ansicht | Inhalt |
| --- | --- |
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
3. Koordinaten in `KOORDINATEN`-Dict in `StrahlungDashAlle.py` eintragen (für die Weltkarte).
4. Fetch-Script ausführen, dann Dashboard neu starten.

## Projektstruktur

```text
weather_fetch.py              # Library: Datenabruf via Open-Meteo API
weather_dash_lib.py           # Library: Datenaggregation (load_data)
StrahlungDashAlle.py          # Kombiniertes Dashboard (Port 8055)
assets/theme.css              # CSS für Light/Dark-Theme
WeatherHistoryWien.py         # Wien        (48.2°N,  16.4°E)
WeatherHistoryCasablanca.py   # Casablanca  (33.6°N,   7.6°W)
WeatherHistoryMedina.py       # Medina      (24.5°N,  39.6°E)
WeatherHistoryRome.py         # Rom         (41.9°N,  12.5°E)
WeatherHistoryLisbon.py       # Lissabon    (38.7°N,   9.1°W)
WeatherHistorySantiago.py     # Santiago    (33.4°S,  70.7°W)
WeatherHistoryLosAngeles.py   # Los Angeles (34.1°N, 118.2°W)
WeatherHistoryLasVegas.py     # Las Vegas   (36.2°N, 115.1°W)
WeatherHistoryNewYork.py      # New York    (40.7°N,  74.0°W)
WeatherHistoryOslo.py         # Oslo        (59.9°N,  10.8°E)
WeatherHistoryTokyo.py        # Tokyo       (35.7°N, 139.7°E)
WeatherHistoryShanghai.py     # Shanghai    (31.2°N, 121.5°E)
WeatherHistoryMumbai.py       # Mumbai      (19.1°N,  72.9°E)
WeatherHistoryDublin.py       # Dublin      (53.3°N,   6.3°W)
WeatherHistoryCanberra.py     # Canberra    (35.3°S, 149.1°E)
WeatherHistoryWellington.py   # Wellington  (41.3°S, 174.8°E)
WeatherHistoryYakutsk.py      # Yakutsk     (62.0°N, 129.7°E)
WeatherHistoryLagos.py        # Lagos       ( 6.5°N,   3.4°E)
WeatherHistoryNairobi.py      # Nairobi     ( 1.3°S,  36.8°E)
```

## Datenquelle

[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) – kostenlos, keine Registrierung erforderlich. Daten ab 1940 verfügbar.
