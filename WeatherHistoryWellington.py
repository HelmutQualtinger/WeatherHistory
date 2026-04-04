from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=-41.2866,
        longitude=174.7756,
        timezone="Pacific/Auckland",
        filename="wellington_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
