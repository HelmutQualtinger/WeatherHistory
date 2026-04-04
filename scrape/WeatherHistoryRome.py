from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=41.9028,
        longitude=12.4964,
        timezone="Europe/Rome",
        filename=str(Path(__file__).parent.parent / "csv" / "rome_wetter_vollständig_03_2026.csv"),
        start_date="1980-01-01",
    )
