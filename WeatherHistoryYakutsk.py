from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=62.0355,
        longitude=129.6755,
        timezone="Asia/Yakutsk",
        filename="yakutsk_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
