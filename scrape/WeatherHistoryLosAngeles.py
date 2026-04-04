from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=34.0522,
        longitude=-118.2437,
        timezone="America/Los_Angeles",
        filename=str(Path(__file__).parent.parent / "csv" / "losangeles_wetter_vollständig_03_2026.csv"),
        start_date="1980-01-01",
    )
