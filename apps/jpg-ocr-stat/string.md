---
title: JPG OCR Stat
name: jpg-ocr-stat
namespace: stringhub
type: app
version: 0.1.0
default: home
description: |
  Receipt-image OCR → spreadsheet stats, plus a media-to-text toolkit.
  Home turns a folder of scanned receipts into an xlsx of filename/date/total.
  Sub-pages: Tesseract OCR, OpenAI vision OCR, PDF→text/images, video→frames, xlsx read/write.
tags: [ocr, tesseract, receipts, xlsx, pdf, vision, video, extraction]
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# JPG OCR Stat

Turn a folder of **scanned receipt images** into a clean spreadsheet of
`filename`, `date`, and `total_amount` — one row per image, ordered by filename.
Built on Tesseract OCR with multi-pass preprocessing and keyword-priority total
detection (`GRAND TOTAL` > `TOTAL RM` > `TOTAL AMOUNT` > `TOTAL`/`AMOUNT`, with
`SUBTOTAL`/`TAX`/`GST`/`CHANGE` excluded).

This page is the end-to-end pipeline. The other pages expose the building blocks
on their own — use them when you need raw OCR text, PDF/video inputs, or to
inspect the xlsx.

## Pages

- `@imageocr` — OCR a single image to text (Tesseract)
- `@vision` — OCR/analyze an image with OpenAI vision (handwriting, hard layouts)
- `@pdf` — PDF → text, or PDF pages → images (then OCR them)
- `@video` — video → frames (then OCR them)
- `@xlsx` — inspect or build .xlsx files

## Run the stats pipeline

OCR is slow (~1–1.5s/image) and a folder can hold hundreds of receipts, so the
job runs **detached in the background** — the action returns immediately. Poll
`/act.status` until `state` is `done`, then `/act.preview` to see the sheet.

```act.stat
CLI setsid bash -c 'python3 ./scripts/receipt_stat.py --input "{input}" --output "{output}" --status "{output}.status" >/dev/null 2>&1' </dev/null >/dev/null 2>&1 & echo "Started OCR job (pid $!). Output -> {output}. Poll: /act.status   (then /act.preview when state=done)"
  input: string (required) "Directory of receipt images (.jpg/.png/...)"
  output: string (optional) "Output .xlsx path" = "./stat_ocr.xlsx"
```

## Check job progress

```act.status
CLI cat "{output}.status" 2>/dev/null || echo '{"state":"unknown","hint":"no status file yet — run /act.stat first, or check the --output path matches"}'
  output: string (optional) "Output .xlsx whose .status to read" = "./stat_ocr.xlsx"
```

`state` is `running` (with `processed`/`images`), `done` (with `fully_extracted`),
or `error`.

## Verify the result

```act.preview
CLI python3 ./scripts/xlsx_tools.py read --file "{file}" --rows {rows}
  file: string (optional) "xlsx to preview" = "./stat_ocr.xlsx"
  rows: number (optional) "Max preview rows" = "15"
```

next: `/act.stat --input <dir>` · `/act.status` until done · `/act.preview` · raw OCR → `@imageocr`
