from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="LasVegas",
        latitude=36.1699,
        longitude=-115.1398,
        timezone="America/Los_Angeles",
    )
