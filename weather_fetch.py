import requests
import csv
import statistics

START_DATE = "2000-01-01"
END_DATE = "2026-03-31"

HOURLY_FIELDS = [
    "shortwave_radiation", "temperature_2m", "relative_humidity_2m",
    "surface_pressure", "cloud_cover", "precipitation"
]

CSV_HEADERS = [
    "Datum",
    "Strahlung_Min", "Strahlung_Max", "Strahlung_Avg",
    "Temp_Min", "Temp_Max", "Temp_Avg",
    "Feuchte_Min", "Feuchte_Max", "Feuchte_Avg",
    "Druck_Min", "Druck_Max", "Druck_Avg",
    "Bedeckung_Min", "Bedeckung_Max", "Bedeckung_Avg",
    "Niederschlag_Min", "Niederschlag_Max", "Niederschlag_Avg",
]


def fetch_weather_data(latitude, longitude, timezone, filename,
                       start_date=START_DATE, end_date=END_DATE):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": HOURLY_FIELDS,
        "timezone": timezone,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["hourly"]
        times = data["time"]

        daily_data = []
        for i in range(0, len(times), 24):
            day_slice = {key: data[key][i:i+24] for key in data if key != "time"}
            row = [times[i].split("T")[0]]
            for field in HOURLY_FIELDS:
                vals = day_slice[field]
                row.extend([round(min(vals), 1), round(max(vals), 1), round(statistics.mean(vals), 1)])
            daily_data.append(row)

        with open(filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
            writer.writerows(daily_data)

        print(f"Erfolg! Die Datei '{filename}' wurde erstellt.")

    except Exception as e:
        print(f"Fehler: {e}")
