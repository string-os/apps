---
title: Fuzzy Name Search
name: fuzzy-name-search
namespace: stringhub
type: app
version: 0.1.0
description: This skill includes search capability in 13F, such as fuzzy search a fund information using possibly inaccurate name, or fuzzy search a stock cusip info using its name.
tags: [sec, 13f, search, fuzzy, cusip]
---

# Fuzzy Name Search

Search 13F fund and stock metadata by name through actions. Fuzzy matching (Levenshtein)
means you don't need the exact name — pass approximate keywords and get ranked results
with similarity scores.

## Actions
- **`/act.search_fund`** `--quarter <YYYY-qN>` `[--keywords <name>]` `[--accession_number <accn>]`
  `[--topk <n>]` (default `10`) — find a fund in a given quarter. **Decision:** pass `--keywords` for a
  fuzzy name search (returns top-`topk` funds with accession numbers, addresses, etc.) **OR**
  `--accession_number` for an exact lookup of a single fund. `--quarter` is always required; give at
  least one of `--keywords` / `--accession_number`.
- **`/act.search_stock_cusip`** `--keywords <name>` `[--topk <n>]` (default `10`) — fuzzy-search a
  stock by name and get its CUSIP (top-`topk` ranked matches with similarity scores).

The accession numbers and CUSIPs returned here feed directly into the `13f-analyzer` app's actions.

```act.search_fund
CLI python3 "./scripts/search_fund.py" --keywords "{keywords}" --accession_number "{accession_number}" --quarter "{quarter}" --topk "{topk}"
  quarter: string (required) "The quarter to search in (e.g. 2025-q2)"
  keywords: string (optional) "Fund name or keywords for fuzzy search" = ""
  accession_number: string (optional) "Exact accession number to look up" = ""
  topk: string (optional) "Max number of results to return" = "10"
```

```act.search_stock_cusip
CLI python3 "./scripts/search_stock_cusip.py" --keywords "{keywords}" --topk "{topk}"
  keywords: string (required) "Stock name or keywords for fuzzy CUSIP search"
  topk: string (optional) "Max number of results to return" = "10"
```
