# Open-Meteo Historical Weather API – Available Variables

Source: https://open-meteo.com/en/docs/historical-weather-api

---

## Hourly Variables

### Temperature & Humidity

| Variable | Unit | Meaning |
|---|---|---|
| `temperature_2m` | °C | Air temperature 2m above ground |
| `relative_humidity_2m` | % | Relative humidity at 2m |
| `dew_point_2m` | °C | Dew point temperature at 2m |
| `apparent_temperature` | °C | Feels-like temperature (wind chill + humidity + radiation) |
| `vapour_pressure_deficit` | kPa | Water vapour pressure deficit |

### Pressure

| Variable | Unit | Meaning |
|---|---|---|
| `surface_pressure` | hPa | Pressure at ground level |
| `pressure_msl` | hPa | Pressure reduced to mean sea level |

### Precipitation

| Variable | Unit | Meaning |
|---|---|---|
| `precipitation` | mm | Total precipitation (preceding hour) |
| `rain` | mm | Liquid rain only |
| `snowfall` | cm | Snowfall amount |
| `snow_depth` | m | Accumulated snow on ground |

### Cloud Cover

| Variable | Unit | Meaning |
|---|---|---|
| `cloud_cover` | % | Total cloud coverage |
| `cloud_cover_low` | % | Low clouds (0–2 km) |
| `cloud_cover_mid` | % | Mid clouds (2–6 km) |
| `cloud_cover_high` | % | High clouds (>6 km) |

### Solar Radiation

| Variable | Unit | Meaning |
|---|---|---|
| `shortwave_radiation` | W/m² | Global horizontal irradiance *(currently fetched)* |
| `direct_radiation` | W/m² | Direct solar radiation on horizontal plane |
| `direct_normal_irradiance` | W/m² | Direct radiation perpendicular to sun |
| `diffuse_radiation` | W/m² | Scattered/diffuse radiation |
| `global_tilted_irradiance` | W/m² | Radiation on a tilted panel |
| `sunshine_duration` | seconds | Sunshine seconds per hour |

### Wind

| Variable | Unit | Meaning |
|---|---|---|
| `wind_speed_10m` | km/h | Wind speed at 10m |
| `wind_speed_100m` | km/h | Wind speed at 100m |
| `wind_direction_10m` | ° | Wind direction at 10m |
| `wind_direction_100m` | ° | Wind direction at 100m |
| `wind_gusts_10m` | km/h | Wind gusts at 10m |

### Soil

| Variable | Unit | Meaning |
|---|---|---|
| `soil_temperature_0_to_7cm` | °C | Soil temperature 0–7 cm depth |
| `soil_temperature_7_to_28cm` | °C | Soil temperature 7–28 cm depth |
| `soil_temperature_28_to_100cm` | °C | Soil temperature 28–100 cm depth |
| `soil_moisture_0_to_7cm` | m³/m³ | Soil water content 0–7 cm |
| `soil_moisture_7_to_28cm` | m³/m³ | Soil water content 7–28 cm |
| `soil_moisture_28_to_100cm` | m³/m³ | Soil water content 28–100 cm |

### Other

| Variable | Unit | Meaning |
|---|---|---|
| `et0_fao_evapotranspiration` | mm | Reference evapotranspiration (well-watered grass) |
| `weather_code` | WMO code | Numeric weather condition code |

---

## Daily Variables (pre-aggregated by the API)

| Variable | Unit | Meaning |
|---|---|---|
| `temperature_2m_max` / `_min` | °C | Daily max/min air temperature |
| `apparent_temperature_max` / `_min` | °C | Daily max/min feels-like temperature |
| `precipitation_sum` | mm | Total daily precipitation |
| `rain_sum` | mm | Total daily rain |
| `snowfall_sum` | cm | Total daily snowfall |
| `precipitation_hours` | h | Hours per day with rain |
| `shortwave_radiation_sum` | MJ/m² | Daily total solar energy |
| `sunshine_duration` | seconds | Daily sunshine duration |
| `daylight_duration` | seconds | Daily daylight duration |
| `sunrise` / `sunset` | ISO8601 | Sunrise/sunset times |
| `wind_speed_10m_max` | km/h | Daily max wind speed |
| `wind_gusts_10m_max` | km/h | Daily max wind gusts |
| `wind_direction_10m_dominant` | ° | Dominant wind direction |
| `et0_fao_evapotranspiration` | mm | Daily evapotranspiration |
| `weather_code` | WMO code | Most severe weather condition of the day |

---

## Currently Fetched in This Project

| Variable | Meaning |
|---|---|
| `shortwave_radiation` | Solar irradiance → converted to kWh/m² (`Avg × 24 / 1000`) |
| `temperature_2m` | Air temperature |
| `relative_humidity_2m` | Relative humidity |
| `surface_pressure` | Atmospheric pressure at ground |
| `cloud_cover` | Total cloud coverage |
| `precipitation` | Precipitation → daily total (`Avg × 24` mm) |

All fetched hourly and aggregated to daily `_Min`, `_Max`, `_Avg` columns in the CSV.

## Potentially Interesting Additions

- `wind_speed_10m` — wind analysis per city
- `apparent_temperature` — how hot/cold it actually feels
- `sunshine_duration` — actual sunshine hours vs. cloud cover
- `snow_depth` — relevant for cold cities (Wien, Oslo, Yakutsk)
- `direct_normal_irradiance` — useful for solar panel yield estimates
