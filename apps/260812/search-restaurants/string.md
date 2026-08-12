---
title: Search Restaurants
name: search-restaurants
namespace: stringhub
type: app
version: 0.2.0
description: "Retrieve restaurants by city from the bundled dataset. Use this skill when recommending places to eat or validating dining options for a destination."
tags: [travel, restaurants, dining, dataset, search]
---

# Search Restaurants

Look up restaurants for a city — the daemon runs the search script, so you call the
action with a city instead of loading the CSV yourself.

- **`/act.search`** `--city <name>` — list restaurants (name, cuisines, average cost,
  rating) in that city.

Searches the bundled restaurants dataset (`clean_restaurant_2022.csv`).

```act.search
CLI python3 ./scripts/search_restaurants.py --city {city}
  city: string (required) "City to search restaurants for"
```
