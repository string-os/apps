---
name: weather
namespace: stringhub
version: 1.0.0
description: Current weather, forecasts, and city lookup via Open-Meteo. No API key required.
tags: [utilities, weather, forecast, open-meteo, geocoding, temperature]
type: app
---

# Weather

Current weather and 7-day forecasts anywhere in the world. Powered by Open-Meteo (free, no API key).

**Quick start:**
1. `/act.find_city --name "Seoul"` to get coordinates
2. `/act.current --latitude 37.57 --longitude 126.98` for current conditions
3. `/act.forecast --latitude 37.57 --longitude 126.98` for 7-day outlook

---

## Find City

```act.find_city
GET https://geocoding-api.open-meteo.com/v1/search?count=3
  name: string (required) "City name (e.g. Seoul, Tokyo, New York)"
```

```act.find_city.response
## Search Results

{Response.body.results.0.name}, {Response.body.results.0.country}
- **Latitude:** {Response.body.results.0.latitude}
- **Longitude:** {Response.body.results.0.longitude}
- **Timezone:** {Response.body.results.0.timezone}
- **Population:** {Response.body.results.0.population}

Next: `/act.current --latitude {Response.body.results.0.latitude} --longitude {Response.body.results.0.longitude}`
```

    /act.find_city --name "Seoul"
    /act.find_city --name "San Francisco"
    /act.find_city --name "London"

---

## Current Weather

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

---

## 7-Day Forecast

```act.forecast
GET https://api.open-meteo.com/v1/forecast?daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto
  latitude: number (required) "Latitude"
  longitude: number (required) "Longitude"
```

```act.forecast.response
## 7-Day Forecast

Timezone: {Response.body.timezone} · Elevation: {Response.body.elevation}m
```

---

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

---

## Tips

- Start with `find_city` if you only know the city name
- All temperatures in Celsius, wind in km/h
- Forecast requires `curl` + `jq` (pre-installed on most systems)
- Open-Meteo is free for non-commercial use, no rate limits
