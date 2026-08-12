---
title: Marker PDF To Markdown
name: marker
namespace: stringhub
type: app
version: 0.2.0
description: Convert PDF documents to Markdown using marker_single. Use when Claude needs to extract text content from PDFs while preserving LaTeX formulas, equations, and document structure. Ideal for academic papers and technical documents containing mathematical notation.
tags: [pdf, markdown, latex, marker]
---

# Marker

Convert a PDF to Markdown while preserving LaTeX formulas, equations, and document
structure — best for academic papers and technical docs with math notation. The action
runs the bundled marker pipeline (via `marker_single`) so you just point it at a PDF.

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action prints the Markdown to stdout; you should not
need `/act.to_markdown --help`.

## Convert
- **`/act.to_markdown`** `--pdf <path>` `[--timeout <seconds>]` (default `120`) — convert a
  PDF to Markdown via `marker_single`, printed to stdout. Preserves LaTeX formulas and
  structure. Use when you need the text content of a math-heavy PDF. Raise `--timeout` for
  large PDFs (model load + inference can be slow on first run).

```act.to_markdown
CLI python3 ./scripts/marker_to_markdown.py "{pdf}" --timeout "{timeout}"
  pdf: string (required) "Path to the PDF file to convert"
  timeout: string (optional) "Timeout in seconds for marker_single" = "120"
```
