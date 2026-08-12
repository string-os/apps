---
title: Search Accommodations
name: search-accommodations
namespace: stringhub
type: app
version: 0.2.0
description: "Lookup accommodations by city from the bundled dataset. Use this skill when you need to recommend places to stay in a given city or filter lodging options before building an itinerary."
tags: [travel, accommodations, lodging, dataset, search]
---

# Search Accommodations

Look up accommodations for a city — the daemon runs the search script, so you call
the action with a city instead of loading the CSV yourself.

- **`/act.search`** `--city <name>` — list accommodations (name, room type, price,
  occupancy, house rules) in that city.

Searches the bundled accommodations dataset (`clean_accommodations_2022.csv`).

```act.search
CLI python3 ./scripts/search_accommodations.py --city {city}
  city: string (required) "City to search accommodations for"
```
