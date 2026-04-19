import requests
import statistics
import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

START_DATE = "1980-01-01"
END_DATE = "2026-03-31"

HOURLY_FIELDS = [
    "shortwave_radiation", "temperature_2m", "relative_humidity_2m",
    "surface_pressure", "cloud_cover", "precipitation"
]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ClimateHistory (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    City VARCHAR(100) NOT NULL,
    Datum DATE NOT NULL,
    Latitude FLOAT,
    Longitude FLOAT,
    Strahlung_Min FLOAT,
    Strahlung_Max FLOAT,
    Strahlung_Avg FLOAT,
    Temp_Min FLOAT,
    Temp_Max FLOAT,
    Temp_Avg FLOAT,
    Feuchte_Min FLOAT,
    Feuchte_Max FLOAT,
    Feuchte_Avg FLOAT,
    Druck_Min FLOAT,
    Druck_Max FLOAT,
    Druck_Avg FLOAT,
    Bedeckung_Min FLOAT,
    Bedeckung_Max FLOAT,
    Bedeckung_Avg FLOAT,
    Niederschlag_Min FLOAT,
    Niederschlag_Max FLOAT,
    Niederschlag_Avg FLOAT,
    UNIQUE KEY uq_city_datum (City, Datum),
    INDEX idx_datum (Datum),
    INDEX idx_geo_datum (Longitude, Latitude, Datum)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

INSERT_SQL = """
INSERT INTO ClimateHistory (
    City, Datum, Latitude, Longitude,
    Strahlung_Min, Strahlung_Max, Strahlung_Avg,
    Temp_Min, Temp_Max, Temp_Avg,
    Feuchte_Min, Feuchte_Max, Feuchte_Avg,
    Druck_Min, Druck_Max, Druck_Avg,
    Bedeckung_Min, Bedeckung_Max, Bedeckung_Avg,
    Niederschlag_Min, Niederschlag_Max, Niederschlag_Avg
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    Strahlung_Min=VALUES(Strahlung_Min), Strahlung_Max=VALUES(Strahlung_Max), Strahlung_Avg=VALUES(Strahlung_Avg),
    Temp_Min=VALUES(Temp_Min), Temp_Max=VALUES(Temp_Max), Temp_Avg=VALUES(Temp_Avg),
    Feuchte_Min=VALUES(Feuchte_Min), Feuchte_Max=VALUES(Feuchte_Max), Feuchte_Avg=VALUES(Feuchte_Avg),
    Druck_Min=VALUES(Druck_Min), Druck_Max=VALUES(Druck_Max), Druck_Avg=VALUES(Druck_Avg),
    Bedeckung_Min=VALUES(Bedeckung_Min), Bedeckung_Max=VALUES(Bedeckung_Max), Bedeckung_Avg=VALUES(Bedeckung_Avg),
    Niederschlag_Min=VALUES(Niederschlag_Min), Niederschlag_Max=VALUES(Niederschlag_Max), Niederschlag_Avg=VALUES(Niederschlag_Avg)
"""


def fetch_weather_data(city, latitude, longitude, timezone,
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

        rows = []
        for i in range(0, len(times), 24):
            day_slice = {key: data[key][i:i+24] for key in data if key != "time"}
            date_str = times[i].split("T")[0]
            row = [city, date_str, latitude, longitude]
            for field in HOURLY_FIELDS:
                vals = day_slice[field]
                row.extend([round(min(vals), 1), round(max(vals), 1), round(statistics.mean(vals), 1)])
            rows.append(tuple(row))

        conn = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        cursor.executemany(INSERT_SQL, rows)
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Erfolg! {len(rows)} Zeilen für '{city}' in ClimateHistory gespeichert.")

    except Exception as e:
        print(f"Fehler: {e}")
