from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=59.9139,
        longitude=10.7522,
        timezone="Europe/Oslo",
        filename="oslo_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
