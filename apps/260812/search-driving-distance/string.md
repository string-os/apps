---
title: Search Driving Distance
name: search-driving-distance
namespace: stringhub
type: app
version: 0.2.0
description: "Estimate driving/taxi duration, distance, and rough cost between two cities using the bundled distance matrix CSV. Use this skill when comparing ground travel options or validating itinerary legs."
tags: [travel, driving, distance, routing, dataset]
---

# Search Driving Distance

Estimate distance, duration, and rough cost between two cities — the daemon runs the
search script, so you call the action with an origin and destination instead of
loading the CSV yourself.

- **`/act.search`** `--origin <city>` `--destination <city>` `[--mode driving|taxi]`
  (default `driving`) — distance/duration/cost for that leg.

Searches the bundled distance matrix (`distance.csv`).

```act.search
CLI python3 ./scripts/search_driving_distance.py --origin {origin} --destination {destination} --mode {mode}
  origin: string (required) "Origin city"
  destination: string (required) "Destination city"
  mode: string (optional) "Travel mode: driving (default) or taxi" = "driving"
```
