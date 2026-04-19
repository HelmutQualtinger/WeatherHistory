import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

DB_NAME = os.environ["DB_NAME"]

CREATE_DB_SQL = f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS `{DB_NAME}`.ClimateHistory (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    City VARCHAR(100) NOT NULL,
    Country VARCHAR(100),
    Continent VARCHAR(100),
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

conn = mysql.connector.connect(
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)
cursor = conn.cursor()
cursor.execute(CREATE_DB_SQL)
print(f"Database '{DB_NAME}' ready.")
cursor.execute(CREATE_TABLE_SQL)
conn.commit()
print(f"Table 'ClimateHistory' ready.")
cursor.close()
conn.close()
