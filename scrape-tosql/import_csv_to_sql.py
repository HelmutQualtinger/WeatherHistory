import os
import csv
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

CITIES = {
    "Wien":         {"country": "Austria",       "continent": "Europa",       "lat": 48.2082,  "lon": 16.3738,   "csv": "wien_wetter_vollständig_03_2026.csv"},
    "Lagos":        {"country": "Nigeria",        "continent": "Afrika",       "lat": 6.5244,   "lon": 3.3792,    "csv": "lagos_wetter_vollständig_03_2026.csv"},
    "Nairobi":      {"country": "Kenya",          "continent": "Afrika",       "lat": -1.2921,  "lon": 36.8219,   "csv": "nairobi_wetter_vollständig_03_2026.csv"},
    "Casablanca":   {"country": "Morocco",        "continent": "Afrika",       "lat": 33.5731,  "lon": -7.5898,   "csv": "casablanca_wetter_vollständig_03_2026.csv"},
    "Medina":       {"country": "Saudi Arabia",   "continent": "Asien",        "lat": 24.5247,  "lon": 39.5692,   "csv": "medina_wetter_vollständig_03_2026.csv"},
    "Rom":          {"country": "Italy",          "continent": "Europa",       "lat": 41.9028,  "lon": 12.4964,   "csv": "rome_wetter_vollständig_03_2026.csv"},
    "Lissabon":     {"country": "Portugal",       "continent": "Europa",       "lat": 38.7223,  "lon": -9.1393,   "csv": "lisbon_wetter_vollständig_03_2026.csv"},
    "Santiago":     {"country": "Chile",          "continent": "Südamerika",   "lat": -33.4489, "lon": -70.6693,  "csv": "santiago_wetter_vollständig_03_2026.csv"},
    "Las Vegas":    {"country": "USA",            "continent": "Nordamerika",  "lat": 36.1699,  "lon": -115.1398, "csv": "lasvegas_wetter_vollständig_03_2026.csv"},
    "Los Angeles":  {"country": "USA",            "continent": "Nordamerika",  "lat": 34.0522,  "lon": -118.2437, "csv": "losangeles_wetter_vollständig_03_2026.csv"},
    "New York":     {"country": "USA",            "continent": "Nordamerika",  "lat": 40.7128,  "lon": -74.0060,  "csv": "newyork_wetter_vollständig_03_2026.csv"},
    "Oslo":         {"country": "Norway",         "continent": "Europa",       "lat": 59.9139,  "lon": 10.7522,   "csv": "oslo_wetter_vollständig_03_2026.csv"},
    "Yakutsk":      {"country": "Russia",         "continent": "Asien",        "lat": 62.0355,  "lon": 129.6755,  "csv": "yakutsk_wetter_vollständig_03_2026.csv"},
    "Tokyo":        {"country": "Japan",          "continent": "Asien",        "lat": 35.6762,  "lon": 139.6503,  "csv": "tokyo_wetter_vollständig_03_2026.csv"},
    "Shanghai":     {"country": "China",          "continent": "Asien",        "lat": 31.2304,  "lon": 121.4737,  "csv": "shanghai_wetter_vollständig_03_2026.csv"},
    "Mumbai":       {"country": "India",          "continent": "Asien",        "lat": 19.0760,  "lon": 72.8777,   "csv": "mumbai_wetter_vollständig_03_2026.csv"},
    "Dublin":       {"country": "Ireland",        "continent": "Europa",       "lat": 53.3498,  "lon": -6.2603,   "csv": "dublin_wetter_vollständig_03_2026.csv"},
    "Canberra":     {"country": "Australia",      "continent": "Ozeanien",     "lat": -35.2809, "lon": 149.1300,  "csv": "canberra_wetter_vollständig_03_2026.csv"},
    "Wellington":   {"country": "New Zealand",    "continent": "Ozeanien",     "lat": -41.2866, "lon": 174.7756,  "csv": "wellington_wetter_vollständig_03_2026.csv"},
    "Kapstadt":     {"country": "South Africa",   "continent": "Afrika",       "lat": -33.9249, "lon": 18.4241,   "csv": "kapstadt_wetter_vollständig_03_2026.csv"},
    "Rio":          {"country": "Brazil",         "continent": "Südamerika",   "lat": -22.9068, "lon": -43.1729,  "csv": "rio_wetter_vollständig_03_2026.csv"},
    "Kuala Lumpur": {"country": "Malaysia",       "continent": "Asien",        "lat": 3.1390,   "lon": 101.6869,  "csv": "kualalumpur_wetter_vollständig_03_2026.csv"},
    "London":       {"country": "UK",             "continent": "Europa",       "lat": 51.5074,  "lon": -0.1278,   "csv": "london_wetter_vollständig_03_2026.csv"},
    "Paris":        {"country": "France",         "continent": "Europa",       "lat": 48.8566,  "lon": 2.3522,    "csv": "paris_wetter_vollständig_03_2026.csv"},
    "Moskau":       {"country": "Russia",         "continent": "Europa",       "lat": 55.7558,  "lon": 37.6176,   "csv": "moscow_wetter_vollständig_03_2026.csv"},
    "Wladiwostok":  {"country": "Russia",         "continent": "Asien",        "lat": 43.1155,  "lon": 131.8855,  "csv": "wladiwostok_wetter_vollständig_03_2026.csv"},
}

INSERT_SQL = """
INSERT INTO ClimateHistory (
    City, Country, Continent, Datum, Latitude, Longitude,
    Strahlung_Min, Strahlung_Max, Strahlung_Avg,
    Temp_Min, Temp_Max, Temp_Avg,
    Feuchte_Min, Feuchte_Max, Feuchte_Avg,
    Druck_Min, Druck_Max, Druck_Avg,
    Bedeckung_Min, Bedeckung_Max, Bedeckung_Avg,
    Niederschlag_Min, Niederschlag_Max, Niederschlag_Avg
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
    Country=VALUES(Country), Continent=VALUES(Continent),
    Latitude=VALUES(Latitude), Longitude=VALUES(Longitude),
    Strahlung_Min=VALUES(Strahlung_Min), Strahlung_Max=VALUES(Strahlung_Max), Strahlung_Avg=VALUES(Strahlung_Avg),
    Temp_Min=VALUES(Temp_Min), Temp_Max=VALUES(Temp_Max), Temp_Avg=VALUES(Temp_Avg),
    Feuchte_Min=VALUES(Feuchte_Min), Feuchte_Max=VALUES(Feuchte_Max), Feuchte_Avg=VALUES(Feuchte_Avg),
    Druck_Min=VALUES(Druck_Min), Druck_Max=VALUES(Druck_Max), Druck_Avg=VALUES(Druck_Avg),
    Bedeckung_Min=VALUES(Bedeckung_Min), Bedeckung_Max=VALUES(Bedeckung_Max), Bedeckung_Avg=VALUES(Bedeckung_Avg),
    Niederschlag_Min=VALUES(Niederschlag_Min), Niederschlag_Max=VALUES(Niederschlag_Max), Niederschlag_Avg=VALUES(Niederschlag_Avg)
"""

csv_dir = Path(__file__).parent.parent / "csv"

conn = mysql.connector.connect(
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)
cursor = conn.cursor()

for city, meta in CITIES.items():
    path = csv_dir / meta["csv"]
    if not path.exists():
        print(f"SKIP {city}: {path} not found")
        continue
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append((
                city, meta["country"], meta["continent"], row["Datum"],
                meta["lat"], meta["lon"],
                row["Strahlung_Min"], row["Strahlung_Max"], row["Strahlung_Avg"],
                row["Temp_Min"], row["Temp_Max"], row["Temp_Avg"],
                row["Feuchte_Min"], row["Feuchte_Max"], row["Feuchte_Avg"],
                row["Druck_Min"], row["Druck_Max"], row["Druck_Avg"],
                row["Bedeckung_Min"], row["Bedeckung_Max"], row["Bedeckung_Avg"],
                row["Niederschlag_Min"], row["Niederschlag_Max"], row["Niederschlag_Avg"],
            ))
    cursor.executemany(INSERT_SQL, rows)
    conn.commit()
    print(f"{city}: {len(rows)} rows inserted.")

cursor.close()
conn.close()
