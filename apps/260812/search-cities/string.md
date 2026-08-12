---
title: Search Cities
name: search-cities
namespace: stringhub
type: app
version: 0.2.0
description: "List cities for a given state using the bundled background data. Use this skill to validate state inputs or expand destination choices before flight/restaurant/attraction/driving/accommodation lookups."
tags: [travel, cities, states, dataset, search]
---

# Search Cities

List the cities in a given state — the daemon runs the search script, so you call
the action with a state instead of parsing the file yourself.

- **`/act.search`** `--state <name>` — list the cities in that state.

Searches the bundled city/state background data (`citySet_with_states.txt`).

```act.search
CLI python3 ./scripts/search_cities.py --state {state}
  state: string (required) "State to list cities for"
```
