---
title: 13f Analyzer
name: 13f-analyzer
namespace: stringhub
type: app
version: 0.1.0
description: Perform various data analysis on SEC 13-F and obtain some insights of fund activities such as number of holdings, AUM, and change of holdings between two quarters.
tags: [sec, 13f, finance, analysis]
---

# 13F Analyzer

Analyze SEC 13-F holdings data through actions. The daemon runs the underlying analysis;
identify funds by accession number + quarter (e.g. `2025-q2`), stocks by CUSIP.

## Actions
- **`/act.one_fund_analysis`** `--accession_number <accn>` `--quarter <YYYY-qN>`
  `[--baseline_quarter <YYYY-qN>]` `[--baseline_accession_number <accn>]` — summarize one fund's
  holdings for a quarter (total holdings, AUM, stock count, etc.). **Decision:** to instead get the
  **change** of holdings between two quarters (newly bought / sold stocks ranked by notional value),
  ALSO pass both `--baseline_quarter` and `--baseline_accession_number` (the same fund's accession in
  the baseline quarter). Omit both for a single-quarter summary.
- **`/act.holding_analysis`** `--cusip <cusip>` `--quarter <YYYY-qN>` `[--topk <n>]` (default `10`) —
  for a given stock CUSIP + quarter, list the top-`topk` funds holding it by notional value.

Identify funds by accession number + quarter (e.g. `2025-q2`), stocks by CUSIP. Need an accession
number or CUSIP from a name? Use the `fuzzy-name-search` app first.

```act.one_fund_analysis
CLI python3 "./scripts/one_fund_analysis.py" --accession_number "{accession_number}" --quarter "{quarter}" --baseline_quarter "{baseline_quarter}" --baseline_accession_number "{baseline_accession_number}"
  accession_number: string (required) "The accession number of the fund to analyze"
  quarter: string (required) "The quarter of the fund to analyze (e.g. 2025-q2)"
  baseline_quarter: string (optional) "Baseline quarter for change-of-holdings comparison" = ""
  baseline_accession_number: string (optional) "Baseline accession number for comparison" = ""
```

```act.holding_analysis
CLI python3 "./scripts/holding_analysis.py" --cusip "{cusip}" --quarter "{quarter}" --topk "{topk}"
  cusip: string (required) "The CUSIP of the stock to analyze"
  quarter: string (required) "The quarter to analyze (e.g. 2025-q3)"
  topk: string (optional) "Max number of funds to return" = "10"
```
