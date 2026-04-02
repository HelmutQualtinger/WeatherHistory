# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the scripts

```bash
# Fetch weather data for a city
python3 WeatherHistoryWien.py
python3 WeatherHistoryCasablanca.py
python3 WeatherHistoryMedina.py

# Start a dashboard (each on its own port)
python3 StrahlungDashWien.py        # http://localhost:8050
python3 StrahlungDashCasablanca.py  # http://localhost:8051
python3 StrahlungDashMedina.py      # http://localhost:8052
```

## Architecture

Two shared libraries power all city-specific scripts:

**`weather_fetch.py`** – single function `fetch_weather_data(latitude, longitude, timezone, filename, start_date, end_date)`. Calls the Open-Meteo archive API, aggregates hourly data into daily min/max/avg rows, and writes a CSV.

**`weather_dash_lib.py`** – `load_data(filename)` loads a CSV and computes all aggregations (monthly/yearly kWh, monthly temp averages, monthly precip totals). `create_app(cfg)` builds and returns a fully configured Dash app with six tabs: Strahlung Monatsmittel, Strahlung nach Jahr, Strahlung Zeitreihe, Strahlung Jahressummen, Temperaturen, Niederschlag. All callbacks are registered inside `create_app`.

**City scripts** are thin wrappers — `WeatherHistory*.py` call `fetch_weather_data(...)` with city-specific coordinates/timezone/filename, and `StrahlungDash*.py` call `create_app(cfg)` with a config dict of colors, thresholds, and port.

## Adding a new city

1. Create `WeatherHistoryXxx.py` calling `fetch_weather_data(...)` with the city's coordinates and timezone.
2. Create `StrahlungDashXxx.py` calling `create_app(cfg)` — pick an unused port and set colors/thresholds in the config dict.
3. Run the fetch script to generate the CSV, then start the dashboard.

## CSV format

Each CSV has daily rows with columns: `Datum`, then for each of the six fields (Strahlung, Temp, Feuchte, Druck, Bedeckung, Niederschlag): `_Min`, `_Max`, `_Avg`. Strahlung is in W/m²; the dashboards convert to kWh/m² via `Strahlung_Avg × 24 / 1000`. Niederschlag daily total = `Niederschlag_Avg × 24` mm.

## Dependencies

Managed via `pyproject.toml` with a `.venv`. Use `python3` (not `python`). Dash and Plotly are used for dashboards but not listed in `pyproject.toml` — install manually if needed: `pip install dash plotly pandas`.
