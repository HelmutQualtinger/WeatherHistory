# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the scripts

```bash
# Fetch weather data for a city (run from project root)
python3 scrape/WeatherHistoryWien.py
python3 scrape/WeatherHistoryCasablanca.py
python3 scrape/WeatherHistoryMedina.py
python3 scrape/WeatherHistoryRome.py
python3 scrape/WeatherHistoryLisbon.py
python3 scrape/WeatherHistorySantiago.py
python3 scrape/WeatherHistoryLosAngeles.py
python3 scrape/WeatherHistoryLasVegas.py
python3 scrape/WeatherHistoryNewYork.py
python3 scrape/WeatherHistoryOslo.py
python3 scrape/WeatherHistoryTokyo.py
python3 scrape/WeatherHistoryShanghai.py
python3 scrape/WeatherHistoryMumbai.py
python3 scrape/WeatherHistoryDublin.py
python3 scrape/WeatherHistoryCanberra.py
python3 scrape/WeatherHistoryWellington.py
python3 scrape/WeatherHistoryYakutsk.py
python3 scrape/WeatherHistoryLagos.py
python3 scrape/WeatherHistoryNairobi.py
# CSVs are written to csv/

# Start the combined dashboard
python3 StrahlungDashAlle.py        # http://localhost:8055
```

## Architecture

Two shared libraries power all city-specific scripts:

**`weather_fetch.py`** – single function `fetch_weather_data(latitude, longitude, timezone, filename, start_date, end_date)`. Calls the Open-Meteo archive API, aggregates hourly data into daily min/max/avg rows, and writes a CSV.

**`weather_dash_lib.py`** – `load_data(filename)` loads a CSV and computes all aggregations (monthly/yearly kWh, monthly temp averages, monthly precip totals, yearly trend data). Used by `StrahlungDashAlle.py` at startup for every configured city.

**`StrahlungDashAlle.py`** – combined dashboard on port 8055. Preloads all city data at startup. UI: compact top bar with Kontinent/Stadt dropdowns and Ansicht/Jahr dropdowns on the left, interactive world map on the right. View selection via dropdown menu (not tabs). Light/dark theme toggle. Reads CSVs from `csv/`.

**City scripts** live in `scrape/` — `WeatherHistory*.py` call `fetch_weather_data(...)` with city-specific coordinates/timezone/filename. They use `pathlib` to resolve paths relative to their location, so they can be run from any working directory. CSVs are written to `csv/`.

**Key dicts in `StrahlungDashAlle.py`:**
- `STAEDTE` – per-city colors, temperature thresholds, CSV filename
- `KONTINENTE` – continent → list of cities (drives the continent dropdown)
- `KOORDINATEN` – city → (lat, lon) for the world map markers

## Adding a new city

1. Create `scrape/WeatherHistoryXxx.py` calling `fetch_weather_data(...)` with the city's coordinates and timezone. Use `Path(__file__).parent.parent / "csv" / "xxx.csv"` for the filename.
2. Add an entry to `STAEDTE` in `StrahlungDashAlle.py` with colors, thresholds, and `"filename": "csv/xxx.csv"`.
3. Add the city to the appropriate continent in `KONTINENTE`.
4. Add coordinates to `KOORDINATEN` for the world map.
5. Run the fetch script to generate the CSV, then restart the dashboard.

## CSV format

Each CSV has daily rows with columns: `Datum`, then for each of the six fields (Strahlung, Temp, Feuchte, Druck, Bedeckung, Niederschlag): `_Min`, `_Max`, `_Avg`. Strahlung is in W/m²; the dashboards convert to kWh/m² via `Strahlung_Avg × 24 / 1000`. Niederschlag daily total = `Niederschlag_Avg × 24` mm.

## Dependencies

Managed via `pyproject.toml` with a `.venv`. Use `python3` (not `python`). Dash and Plotly are used for dashboards but not listed in `pyproject.toml` — install manually if needed: `pip install dash plotly pandas numpy`.
