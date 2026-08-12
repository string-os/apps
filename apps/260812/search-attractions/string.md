---
title: Search Attractions
name: search-attractions
namespace: stringhub
type: app
version: 0.2.0
description: "Retrieve attractions by city from the bundled dataset. Use this skill when surfacing points of interest or building sightseeing suggestions for a destination."
tags: [travel, attractions, sightseeing, dataset, search]
---

# Search Attractions

Look up points of interest for a city — the daemon runs the search script, so you
call the action with a city instead of loading the CSV yourself.

- **`/act.search`** `--city <name>` — list attractions (name, address, phone,
  website) in that city.

Searches the bundled attractions dataset (`attractions.csv`).

```act.search
CLI python3 ./scripts/search_attractions.py --city {city}
  city: string (required) "City to search attractions for"
```
