from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=-35.2809,
        longitude=149.1300,
        timezone="Australia/Sydney",
        filename=str(Path(__file__).parent.parent / "csv" / "canberra_wetter_vollständig_03_2026.csv"),
        start_date="1980-01-01",
    )
