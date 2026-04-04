from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=19.0760,
        longitude=72.8777,
        timezone="Asia/Kolkata",
        filename="mumbai_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
