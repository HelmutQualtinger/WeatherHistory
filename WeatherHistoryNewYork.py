from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=40.7128,
        longitude=-74.0060,
        timezone="America/New_York",
        filename="newyork_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
