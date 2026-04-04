from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=53.3498,
        longitude=-6.2603,
        timezone="Europe/Dublin",
        filename="dublin_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
