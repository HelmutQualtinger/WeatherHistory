from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Wladiwostok",
        latitude=43.1155,
        longitude=131.8855,
        timezone="Asia/Vladivostok",
    )
