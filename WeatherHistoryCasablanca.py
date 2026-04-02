from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=33.5731,
        longitude=-7.5898,
        timezone="Africa/Casablanca",
        filename="casablanca_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
