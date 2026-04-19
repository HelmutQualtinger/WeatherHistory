from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Rio",
        latitude=-22.9068,
        longitude=-43.1729,
        timezone="America/Sao_Paulo",
    )
