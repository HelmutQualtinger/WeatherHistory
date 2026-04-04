from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=6.5244,
        longitude=3.3792,
        timezone="Africa/Lagos",
        filename="lagos_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
