from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=-35.2809,
        longitude=149.1300,
        timezone="Australia/Sydney",
        filename="canberra_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
