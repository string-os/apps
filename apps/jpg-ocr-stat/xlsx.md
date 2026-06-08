---
title: XLSX read / write
name: jpg-ocr-stat-xlsx
type: app
version: 0.1.0
description: Inspect an .xlsx (sheets, dimensions, preview rows) or build a single-sheet workbook from JSON rows. Uses openpyxl.
tags: [xlsx, spreadsheet, openpyxl]
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# XLSX read / write

Work with spreadsheet files via openpyxl.

- **`/act.read`** — list sheets, show dimensions, and preview the first rows of a
  sheet. Use it to verify what `@home`'s stat pipeline produced.
- **`/act.write`** — build a single-sheet `.xlsx` from a JSON file of rows
  (array of arrays). Lets you assemble a workbook from data you extracted
  yourself (OCR + your own parsing).

```act.read
CLI python3 ./scripts/xlsx_tools.py read --file "{file}" --rows {rows}
  file: string (required) "Path to the .xlsx file"
  rows: number (optional) "Max preview rows" = "20"
```

```act.write
CLI python3 ./scripts/xlsx_tools.py write --rows "{rows}" --out "{out}" --sheet {sheet}
  rows: string (required) "Path to a JSON file: array of rows, each an array of cells"
  out: string (required) "Output .xlsx path"
  sheet: string (optional) "Sheet name" = "results"
```

Rows JSON example: `[["filename","date","total_amount"],["000.jpg","2018-10-19","47.70"]]`

next: `/act.read --file ./stat_ocr.xlsx` · build one → `/act.write --rows rows.json --out out.xlsx`
