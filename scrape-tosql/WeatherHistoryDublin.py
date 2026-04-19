from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Dublin",
        latitude=53.3498,
        longitude=-6.2603,
        timezone="Europe/Dublin",
    )
