---
name: weather
namespace: stringhub
version: 1.1.0
description: Current weather, forecasts, and city lookup via Open-Meteo. No API key required.
tags: [utilities, weather, forecast, open-meteo, geocoding, temperature]
type: app
---

[!requirements](./requirements.md)

# Weather

Current conditions and 7-day forecasts anywhere on Earth, via [Open-Meteo](https://open-meteo.com) (free, no API key, no signup). All actions are plain HTTP — nothing to install. Resolve a city name to coordinates with `find_city`, then pass them to `current` or `forecast`.

## Actions

- `/act.find_city --name <city>` — resolve a city name to coordinates (lat, lon, timezone)
- `/act.current --latitude <lat> --longitude <lon>` — current temperature, wind, and conditions
- `/act.forecast --latitude <lat> --longitude <lon>` — 7-day min/max temperature and precipitation

Don't know the coordinates? Run `find_city` first, or use the common-cities table at the bottom.

```act.find_city
GET https://geocoding-api.open-meteo.com/v1/search?count=3
  name: string (required) "City name (e.g. Seoul, Tokyo, New York)"
```

```act.find_city.response
## {Response.body.results.0.name}, {Response.body.results.0.country}

- **Latitude:** {Response.body.results.0.latitude}
- **Longitude:** {Response.body.results.0.longitude}
- **Timezone:** {Response.body.results.0.timezone}
- **Population:** {Response.body.results.0.population}

Next: `/act.current --latitude {Response.body.results.0.latitude} --longitude {Response.body.results.0.longitude}`
```

```act.current
GET https://api.open-meteo.com/v1/forecast?current_weather=true&timezone=auto
  latitude: number (required) "Latitude (e.g. 37.57)"
  longitude: number (required) "Longitude (e.g. 126.98)"
```

```act.current.response
## Current Weather

- **Temperature:** {Response.body.current_weather.temperature}°C
- **Wind:** {Response.body.current_weather.windspeed} km/h @ {Response.body.current_weather.winddirection}°
- **Weather code:** {Response.body.current_weather.weathercode}
- **Daylight:** is_day={Response.body.current_weather.is_day}
- **Observed at:** {Response.body.current_weather.time} ({Response.body.timezone_abbreviation})
- **Location:** lat={Response.body.latitude}, lon={Response.body.longitude}, elevation={Response.body.elevation}m

**Codes:** 0=clear · 1-3=cloudy · 45=fog · 51-67=rain · 71-77=snow · 80-82=showers · 95-99=thunder
```

```act.forecast
GET https://api.open-meteo.com/v1/forecast?daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto
  latitude: number (required) "Latitude"
  longitude: number (required) "Longitude"
```

```act.forecast.response
## 7-Day Forecast

Timezone: {Response.body.timezone} · Elevation: {Response.body.elevation}m

| Date | Min–Max °C | Rain (mm) | Code |
|------|-----------|-----------|------|
| {Response.body.daily.time.0} | {Response.body.daily.temperature_2m_min.0}–{Response.body.daily.temperature_2m_max.0} | {Response.body.daily.precipitation_sum.0} | {Response.body.daily.weathercode.0} |
| {Response.body.daily.time.1} | {Response.body.daily.temperature_2m_min.1}–{Response.body.daily.temperature_2m_max.1} | {Response.body.daily.precipitation_sum.1} | {Response.body.daily.weathercode.1} |
| {Response.body.daily.time.2} | {Response.body.daily.temperature_2m_min.2}–{Response.body.daily.temperature_2m_max.2} | {Response.body.daily.precipitation_sum.2} | {Response.body.daily.weathercode.2} |
| {Response.body.daily.time.3} | {Response.body.daily.temperature_2m_min.3}–{Response.body.daily.temperature_2m_max.3} | {Response.body.daily.precipitation_sum.3} | {Response.body.daily.weathercode.3} |
| {Response.body.daily.time.4} | {Response.body.daily.temperature_2m_min.4}–{Response.body.daily.temperature_2m_max.4} | {Response.body.daily.precipitation_sum.4} | {Response.body.daily.weathercode.4} |
| {Response.body.daily.time.5} | {Response.body.daily.temperature_2m_min.5}–{Response.body.daily.temperature_2m_max.5} | {Response.body.daily.precipitation_sum.5} | {Response.body.daily.weathercode.5} |
| {Response.body.daily.time.6} | {Response.body.daily.temperature_2m_min.6}–{Response.body.daily.temperature_2m_max.6} | {Response.body.daily.precipitation_sum.6} | {Response.body.daily.weathercode.6} |

**Codes:** 0=clear · 1-3=cloudy · 45=fog · 51-67=rain · 71-77=snow · 80-82=showers · 95-99=thunder
```

## Common Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| Seoul | 37.57 | 126.98 |
| Tokyo | 35.68 | 139.76 |
| New York | 40.71 | -74.01 |
| London | 51.51 | -0.13 |
| San Francisco | 37.77 | -122.42 |
| Paris | 48.86 | 2.35 |
| Sydney | -33.87 | 151.21 |

## Tips

- Start with `find_city` if you only know the city name
- All temperatures in Celsius, wind in km/h
- Open-Meteo is free for non-commercial use, no rate limits
