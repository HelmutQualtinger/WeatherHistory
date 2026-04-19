from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="NewYork",
        latitude=40.7128,
        longitude=-74.0060,
        timezone="America/New_York",
    )
