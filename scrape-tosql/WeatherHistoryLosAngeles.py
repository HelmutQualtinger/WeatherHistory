from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="LosAngeles",
        latitude=34.0522,
        longitude=-118.2437,
        timezone="America/Los_Angeles",
    )
