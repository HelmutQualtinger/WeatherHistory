from weather_fetch import fetch_weather_data

if __name__ == "__main__":
    fetch_weather_data(
        latitude=31.2304,
        longitude=121.4737,
        timezone="Asia/Shanghai",
        filename="shanghai_wetter_vollständig_03_2026.csv",
        start_date="1980-01-01",
    )
