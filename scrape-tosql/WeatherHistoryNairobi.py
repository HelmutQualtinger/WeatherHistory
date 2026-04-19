from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Nairobi",
        latitude=-1.2921,
        longitude=36.8219,
        timezone="Africa/Nairobi",
    )
