from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=-1.2921,
        longitude=36.8219,
        timezone="Africa/Nairobi",
        filename="nairobi_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
