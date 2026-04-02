from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=48.2085,
        longitude=16.3725,
        timezone="Europe/Berlin",
        filename="wien_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
