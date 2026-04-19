from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Wien",
        latitude=48.2085,
        longitude=16.3725,
        timezone="Europe/Berlin",
    )
