from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=35.6762,
        longitude=139.6503,
        timezone="Asia/Tokyo",
        filename="tokyo_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
