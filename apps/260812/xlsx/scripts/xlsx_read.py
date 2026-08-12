#!/usr/bin/env python3
"""Inspect an Excel/CSV workbook: sheet names, per-sheet columns, shape, first rows.

Wraps pandas.read_excel (the inspect operation the xlsx skill teaches). Prints JSON
so the agent doesn't have to write the read code itself.
"""
import json
import sys
import warnings

warnings.filterwarnings("ignore")

import pandas as pd


def clean(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    return "" if v.startswith("{") and v.endswith("}") else v


def parse_args(argv):
    """Tiny --flag value parser (no argparse, so we control empty-arg handling)."""
    out = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            key = a[2:]
            val = argv[i + 1] if i + 1 < len(argv) else ""
            out[key] = clean(val)
            i += 2
        else:
            i += 1
    return out


def df_summary(df, max_rows=10):
    df = df.where(pd.notna(df), None)
    head = df.head(max_rows)
    rows = [
        [None if pd.isna(x) else (x.item() if hasattr(x, "item") else x) for x in rec]
        for rec in head.itertuples(index=False, name=None)
    ]
    return {
        "shape": [int(df.shape[0]), int(df.shape[1])],
        "columns": [str(c) for c in df.columns],
        "first_rows": rows,
    }


def main():
    args = parse_args(sys.argv[1:])
    path = args.get("file", "")
    sheet = args.get("sheet", "")

    if not path:
        print(json.dumps({"ok": False, "error": "Missing --file. Usage: xlsx_read.py --file PATH [--sheet NAME]"}))
        sys.exit(1)

    try:
        if path.lower().endswith((".csv", ".tsv")):
            sep = "\t" if path.lower().endswith(".tsv") else ","
            df = pd.read_csv(path, sep=sep)
            out = {"ok": True, "file": path, "sheets": ["(csv)"], "data": {"(csv)": df_summary(df)}}
            print(json.dumps(out, default=str))
            return

        xls = pd.ExcelFile(path)
        sheet_names = list(xls.sheet_names)

        if sheet:
            if sheet not in sheet_names:
                print(json.dumps({
                    "ok": False,
                    "error": f"Sheet '{sheet}' not found. Available: {sheet_names}",
                }))
                sys.exit(1)
            targets = [sheet]
        else:
            targets = sheet_names

        data = {}
        for s in targets:
            df = pd.read_excel(xls, sheet_name=s)
            data[s] = df_summary(df)

        print(json.dumps({"ok": True, "file": path, "sheets": sheet_names, "data": data}, default=str))
    except FileNotFoundError:
        print(json.dumps({"ok": False, "error": f"File not found: {path}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}. Check the file is a valid .xlsx/.csv."}))
        sys.exit(1)


if __name__ == "__main__":
    main()
