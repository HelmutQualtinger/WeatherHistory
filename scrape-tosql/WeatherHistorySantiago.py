from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Santiago",
        latitude=-33.4489,
        longitude=-70.6693,
        timezone="America/Santiago",
    )
