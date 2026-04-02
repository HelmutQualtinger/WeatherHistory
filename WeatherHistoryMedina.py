from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=24.5247,
        longitude=39.5692,
        timezone="Asia/Riyadh",
        filename="medina_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
