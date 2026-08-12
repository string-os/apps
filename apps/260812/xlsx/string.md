---
title: Xlsx
name: xlsx
namespace: stringhub
type: app
version: 0.2.0
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
tags: [xlsx, spreadsheet, excel, formulas]
---

[!requirements](./requirements.txt)

# Xlsx

Create, edit, and analyze Excel spreadsheets. **Building the model is your own
openpyxl/pandas code** — this app does not generate it for you. What it offloads are two
mechanical operations: inspecting a workbook (`/act.read`) and recalculating + error-scanning
a workbook you produced (`/act.recalc`). Everything below the actions is the decision
knowledge you MUST apply when building.

## Actions
- **`/act.read`** `--file <path.xlsx>` `[--sheet <name>]` (default: all sheets) — inspect a workbook: sheet names, and per-sheet columns + shape + first ~10 rows (JSON). Use this before building to learn the structure instead of writing read code.
- **`/act.recalc`** `--excel_file <path.xlsx>` `[--timeout_seconds <n>]` (default: recalc.py's own default) — recalculate all formulas via LibreOffice and scan every cell for Excel errors; returns JSON (`status`, `total_errors`, `total_formulas`, `error_summary`). MANDATORY after writing any file that contains formulas.

(Library how-to is intentionally terse — you know the openpyxl/pandas API. The rules below
are the part you must not skip.)

# Requirements for Outputs

## All Excel files

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

# XLSX creation, editing, and analysis

## Choosing a library
- **pandas** — data analysis, bulk reads, simple export (`pd.read_excel`, `df.to_excel`). For inspection, prefer `/act.read` over writing read code.
- **openpyxl** — formulas, formatting, cell-level access, Excel-specific features (`Workbook`/`load_workbook`, `Font`/`PatternFill`/`Alignment`, `wb.save`). Cell indices are 1-based.

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.**
This ensures the spreadsheet remains dynamic and updateable.

- ❌ WRONG: compute in Python and write the result — `sheet['B10'] = df['Sales'].sum()` (hardcodes a number).
- ✅ CORRECT: write the formula — `sheet['B10'] = '=SUM(B2:B9)'`, `sheet['C5'] = '=(C4-C2)/C2'`, `sheet['D20'] = '=AVERAGE(D2:D19)'`.

This applies to ALL calculations — totals, percentages, ratios, differences. The
spreadsheet should recalculate when source data changes.

## Common workflow
1. **Inspect** existing inputs with `/act.read` (sheet names, columns, sample rows).
2. **Choose tool**: pandas for data, openpyxl for formulas/formatting.
3. **Create/Load**, **Modify** (data, formulas, formatting), **Save**.
4. **Recalculate (MANDATORY IF USING FORMULAS)**: run `/act.recalc` on the saved file.
5. **Verify and fix errors**: if `status` is `errors_found`, read `error_summary` for the
   error type + locations, fix, and recalc again. Common: `#REF!` (bad reference),
   `#DIV/0!` (divide by zero), `#VALUE!` (wrong type), `#NAME?` (unknown function).

## Recalculating formulas (`/act.recalc`)
Files written by openpyxl store formulas as strings but not their computed values.
`/act.recalc` opens the file in LibreOffice, recalculates every sheet, scans ALL cells for
Excel errors, and returns JSON:
```json
{
  "status": "success",        // or "errors_found"
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {           // only present if errors found
    "#REF!": { "count": 2, "locations": ["Sheet1!B5", "Sheet1!C10"] }
  }
}
```

## Formula Verification Checklist

### Essential Verification
- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)

### Common Pitfalls
- [ ] **NaN handling**: Check for null values with `pd.notna()`
- [ ] **Far-right columns**: FY data often in columns 50+
- [ ] **Multiple matches**: Search all occurrences, not just first
- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)
- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)
- [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets

### Formula Testing Strategy
- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly
- [ ] **Verify dependencies**: Check all cells referenced in formulas exist
- [ ] **Test edge cases**: Include zero, negative, and very large values

## openpyxl notes
- `data_only=True` reads calculated values, but saving such a workbook **permanently
  replaces formulas with values** — never save a `data_only=True` load over your source.
- Large files: `read_only=True` (read) / `write_only=True` (write).
- Formulas are preserved but not evaluated until you run `/act.recalc`.

## Code style
- For Python: minimal, concise, no unnecessary comments or prints.
- For the Excel file itself: comment cells with complex formulas/assumptions, document
  data sources for hardcodes, and note key calculations and model sections.

```act.read
CLI python3 ./scripts/xlsx_read.py --file "{file}" --sheet "{sheet}"
  file: string (required) "Path to the .xlsx/.xlsm/.csv file to inspect"
  sheet: string (optional) "Inspect only this sheet (default: all sheets)" = ""
```

```act.recalc
CLI python3 ./scripts/xlsx_recalc.py "{excel_file}" "{timeout_seconds}"
  excel_file: string (required) "Path to the .xlsx file to recalculate"
  timeout_seconds: string (optional) "Timeout in seconds for the LibreOffice recalculation" = ""
```
