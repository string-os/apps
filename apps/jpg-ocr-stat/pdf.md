---
title: PDF → text / images
name: jpg-ocr-stat-pdf
type: app
version: 0.1.0
description: Extract text from a PDF, or render PDF pages to images for OCR. Built on poppler (pdftotext / pdftoppm).
tags: [pdf, poppler, text, images, ocr]
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# PDF → text / images

Two ways to get data out of a PDF:

- **`/act.totext`** — pull the embedded text layer (fast, exact). Works only if
  the PDF actually has text (digital PDFs, not pure scans).
- **`/act.toimages`** — render each page to an image, so you can OCR a *scanned*
  PDF: run this, then feed the output dir's images into `@imageocr` or `@vision`.

Both use poppler (`pdftotext`, `pdftoppm`). See `@requirements` to install.

```act.totext
CLI python3 ./scripts/pdf_tools.py text --pdf "{pdf}" --out "{out}"
  pdf: string (required) "Path to the PDF"
  out: string (optional) "Output .txt path (empty = embed text in the JSON response)" = ""
```

```act.toimages
CLI python3 ./scripts/pdf_tools.py images --pdf "{pdf}" --outdir "{outdir}" --dpi {dpi} --format {format}
  pdf: string (required) "Path to the PDF"
  outdir: string (required) "Directory to write page images into"
  dpi: number (optional) "Render resolution (200–300 good for OCR)" = "200"
  format: string (optional) "png | jpeg | tiff" = "png"
```

next: scanned PDF → `/act.toimages` then OCR the dir via `@imageocr`
