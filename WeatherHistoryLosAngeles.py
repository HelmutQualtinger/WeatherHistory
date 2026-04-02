from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=34.0522,
        longitude=-118.2437,
        timezone="America/Los_Angeles",
        filename="losangeles_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
