from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=-33.4489,
        longitude=-70.6693,
        timezone="America/Santiago",
        filename="santiago_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
