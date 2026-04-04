from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=31.2304,
        longitude=121.4737,
        timezone="Asia/Shanghai",
        filename=str(Path(__file__).parent.parent / "csv" / "shanghai_wetter_vollständig_03_2026.csv"),
        start_date="1980-01-01",
    )
