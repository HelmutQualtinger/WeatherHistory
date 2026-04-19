from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from weather_fetch_tosql import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        city="Shanghai",
        latitude=31.2304,
        longitude=121.4737,
        timezone="Asia/Shanghai",
    )
