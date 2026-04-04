from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=36.1699,
        longitude=-115.1398,
        timezone="America/Los_Angeles",
        filename="lasvegas_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
