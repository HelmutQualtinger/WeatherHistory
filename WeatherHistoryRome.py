from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=41.9028,
        longitude=12.4964,
        timezone="Europe/Rome",
        filename="rome_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
