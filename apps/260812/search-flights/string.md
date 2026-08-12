---
title: Search Flights
name: search-flights
namespace: stringhub
type: app
version: 0.2.0
description: "Search flights by origin, destination, and departure date using the bundled flights dataset. Use this skill when proposing flight options or checking whether a route/date combination exists."
tags: [travel, flights, routes, dataset, search]
---

# Search Flights

Find flights for a route and departure date — the daemon runs the search script, so
you call the action with origin, destination, and date instead of filtering the CSV
yourself.

- **`/act.search`** `--origin <city>` `--destination <city>` `--date <YYYY-MM-DD>`
  `[--path <csv>]` (default `/app/data/flights/clean_Flights_2022.csv`) — list matching
  flights (number, price, dep/arr times, distance).

Searches the bundled flights dataset (`clean_Flights_2022.csv`).

```act.search
CLI python3 ./scripts/search_flights.py --origin {origin} --destination {destination} --date {date} --path {path}
  origin: string (required) "Origin city name"
  destination: string (required) "Destination city name"
  date: string (required) "Departure date (YYYY-MM-DD)"
  path: string (optional) "Path to the flights CSV" = "/app/data/flights/clean_Flights_2022.csv"
```
