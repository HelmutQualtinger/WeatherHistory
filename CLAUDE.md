# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the scripts

```bash
# Fetch weather data for a city
python3 WeatherHistoryWien.py
python3 WeatherHistoryCasablanca.py
python3 WeatherHistoryMedina.py
python3 WeatherHistoryRome.py
python3 WeatherHistoryLisbon.py
python3 WeatherHistorySantiago.py
python3 WeatherHistoryLosAngeles.py
python3 WeatherHistoryOslo.py

# Start the combined dashboard
python3 StrahlungDashAlle.py        # http://localhost:8055
```

## Architecture

Two shared libraries power all city-specific scripts:

**`weather_fetch.py`** – single function `fetch_weather_data(latitude, longitude, timezone, filename, start_date, end_date)`. Calls the Open-Meteo archive API, aggregates hourly data into daily min/max/avg rows, and writes a CSV.

**`weather_dash_lib.py`** – `load_data(filename)` loads a CSV and computes all aggregations (monthly/yearly kWh, monthly temp averages, monthly precip totals, yearly trend data). Used by `StrahlungDashAlle.py` at startup for every configured city.

**`StrahlungDashAlle.py`** – combined dashboard on port 8055. Preloads all city data at startup, city selected via dropdown. Includes light/dark theme toggle (CSS in `assets/theme.css`, toggled via clientside callback on `<body>`).

**City scripts** are thin wrappers — `WeatherHistory*.py` call `fetch_weather_data(...)` with city-specific coordinates/timezone/filename.

## Adding a new city

1. Create `WeatherHistoryXxx.py` calling `fetch_weather_data(...)` with the city's coordinates and timezone.
2. Add an entry to the `STAEDTE` dict in `StrahlungDashAlle.py` with colors, thresholds, and the CSV filename.
3. Run the fetch script to generate the CSV, then restart the dashboard.

## CSV format

Each CSV has daily rows with columns: `Datum`, then for each of the six fields (Strahlung, Temp, Feuchte, Druck, Bedeckung, Niederschlag): `_Min`, `_Max`, `_Avg`. Strahlung is in W/m²; the dashboards convert to kWh/m² via `Strahlung_Avg × 24 / 1000`. Niederschlag daily total = `Niederschlag_Avg × 24` mm.

## Dependencies

Managed via `pyproject.toml` with a `.venv`. Use `python3` (not `python`). Dash and Plotly are used for dashboards but not listed in `pyproject.toml` — install manually if needed: `pip install dash plotly pandas numpy`.
