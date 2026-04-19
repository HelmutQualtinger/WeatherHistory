from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Canberra",
        latitude=-35.2809,
        longitude=149.1300,
        timezone="Australia/Sydney",
    )
