---
title: PDF
name: pdf
namespace: stringhub
type: app
version: 0.2.0
description: "Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale."
tags: [pdf, forms, extraction, documents]
---

[!requirements](./requirements.txt)

# PDF

Inspect, extract, transform, and fill PDFs through actions — the daemon runs the
underlying pypdf / pdfplumber / poppler code, so you call an action with file paths
instead of writing it. **Each action's flags are listed below** (required unless shown
in `[...]`, which marks an optional flag and its default). All actions print JSON;
file-producing actions report the output path. The flags here are complete — you should
not need `/act.<name> --help`.

## Extract / inspect
- **`/act.extract_text`** `--pdf <path>` `[--out <file>]` `[--layout layout]` — page text;
  omit `--out` to get it inline, pass `--layout layout` to preserve column layout.
- **`/act.extract_tables`** `--pdf <path>` `[--out <file>]` `[--format json|csv]` (default `json`)
  — detected tables, inline or written to `--out`.
- **`/act.metadata`** `--pdf <path>` — title / author / subject / creator / page count.
- **`/act.ocr`** `--pdf <path>` `[--out <file>]` — OCR a scanned (image-only) PDF to text.
- **`/act.extract_images`** `--pdf <path>` `[--out_prefix <prefix>]` (default `image`) — dump embedded images.

## Transform
- **`/act.merge`** `--inputs "<a.pdf b.pdf ...>"` `--out <file>` — concatenate PDFs (`--inputs` is ONE
  space-separated quoted string).
- **`/act.split`** `--pdf <path>` `[--out_dir <dir>]` (default `.`) — write one `page_N.pdf` per page.
- **`/act.rotate`** `--pdf <path>` `--out <file>` `[--degrees <n>]` (default `90`) `[--pages "<1 3>" | all]`
  (default `all`) — rotate all or the listed pages.
- **`/act.encrypt`** `--pdf <path>` `--out <file>` `--user_password <pw>` `[--owner_password <pw>]` — add a password.
- **`/act.decrypt`** `--pdf <path>` `--out <file>` `[--password <pw>]` — remove a password.

## Fill a PDF form  (the main workflow for a form-filling task)
First check which kind of form it is, then follow that branch:

1. **`/act.check_fillable_fields`** `--pdf <path>` — does the PDF have real AcroForm fillable fields?
2a. **Fillable** →
   - **`/act.extract_form_field_info`** `--input_pdf <path>` `--output_json <path>` — write the field
     list; each entry has `field_id`, `page`, `type`, and (for checkboxes) `checked_value`.
   - Build a `field_values.json` that is a **JSON list of objects** — one per field you fill —
     each `{"field_id": <id>, "page": <n>, "value": <val>}`. The `field_id` and `page` MUST match
     `/act.extract_form_field_info`'s output. **It is a list, NOT a `{id: value}` map** (a map makes
     `fill_fillable_fields` raise `TypeError: string indices must be integers`). For a checkbox set
     `value` to that field's exact `checked_value` (e.g. `/2`), not `/1` or `true`. Omit clerk/optional fields.
     Example:
     `[{"field_id": "SC-100[0].Page2[0]...PlaintiffName1[0]", "page": 2, "value": "Joyce He"}]`
   - **`/act.fill_fillable_fields`** `--input_pdf <path>` `--field_values_json <path>` `--output_pdf <path>`
     — validates the field ids / pages / values and prints any errors to fix, then writes the filled PDF.
2b. **Flat / scanned (no AcroForm fields)** →
   - **`/act.convert_pdf_to_images`** `--pdf <path>` `--output_dir <dir>` — one PNG per page.
   - Locate each field's bounding box and write a `fields.json`, then
   - **`/act.check_bounding_boxes`** `--fields_json <path>` — validate boxes (no overlap / too-small).
   - **`/act.create_validation_image`** `--page_number <n>` `--fields_json <path>` `--input_image <png>` `--output_image <png>` — optional visual check.
   - **`/act.fill_pdf_form_with_annotations`** `--input_pdf <path>` `--fields_json <path>` `--output_pdf <path>` — stamp the text onto the page.

`forms.md` is bundled — for the **flat/scanned annotation path (2b)** read it for the
bounding-box determination details (the visual analysis is involved). `reference.md` covers
pdf-lib / troubleshooting. The **fillable path (2a)** above is complete on its own.

```act.extract_text
CLI python3 ./scripts/pdf_ops.py extract_text "{pdf}" "{out}" "{layout}"
  pdf: string (required) "Path to the PDF"
  out: string (optional) "Write text here; omit to return text inline" = ""
  layout: string (optional) "Set to 'layout' to preserve column layout" = ""
```

```act.extract_tables
CLI python3 ./scripts/pdf_ops.py extract_tables "{pdf}" "{out}" "{format}"
  pdf: string (required) "Path to the PDF"
  out: string (optional) "Write tables here; omit to return inline" = ""
  format: string (optional) "json (default) or csv" = "json"
```

```act.metadata
CLI python3 ./scripts/pdf_ops.py metadata "{pdf}"
  pdf: string (required) "Path to the PDF"
```

```act.ocr
CLI python3 ./scripts/pdf_ops.py ocr "{pdf}" "{out}"
  pdf: string (required) "Path to the scanned PDF"
  out: string (optional) "Write OCR text here; omit to return inline" = ""
```

```act.extract_images
CLI python3 ./scripts/pdf_ops.py extract_images "{pdf}" "{out_prefix}"
  pdf: string (required) "Path to the PDF"
  out_prefix: string (optional) "Output path prefix for extracted images" = "image"
```

```act.merge
CLI python3 ./scripts/pdf_ops.py merge "{inputs}" "{out}"
  inputs: string (required) "Space-separated input PDF paths in one quoted string"
  out: string (required) "Path to write the merged PDF"
```

```act.split
CLI python3 ./scripts/pdf_ops.py split "{pdf}" "{out_dir}"
  pdf: string (required) "Path to the PDF to split"
  out_dir: string (optional) "Directory for page_N.pdf files" = "."
```

```act.rotate
CLI python3 ./scripts/pdf_ops.py rotate "{pdf}" "{out}" "{degrees}" "{pages}"
  pdf: string (required) "Path to the PDF"
  out: string (required) "Path to write the rotated PDF"
  degrees: string (optional) "Clockwise degrees (default 90)" = "90"
  pages: string (optional) "1-based pages e.g. '1 3'; omit/all rotates every page" = "all"
```

```act.encrypt
CLI python3 ./scripts/pdf_ops.py encrypt "{pdf}" "{out}" "{user_password}" "{owner_password}"
  pdf: string (required) "Path to the PDF"
  out: string (required) "Path to write the encrypted PDF"
  user_password: string (required) "Password to open the document"
  owner_password: string (optional) "Owner/permissions password (defaults to user password)" = ""
```

```act.decrypt
CLI python3 ./scripts/pdf_ops.py decrypt "{pdf}" "{out}" "{password}"
  pdf: string (required) "Path to the encrypted PDF"
  out: string (required) "Path to write the decrypted PDF"
  password: string (optional) "Password (if the PDF needs one)" = ""
```

```act.check_fillable_fields
CLI python3 ./scripts/check_fillable_fields.py "{pdf}"
  pdf: string (required) "Path to the PDF to inspect for fillable form fields"
```

```act.extract_form_field_info
CLI python3 ./scripts/extract_form_field_info.py "{input_pdf}" "{output_json}"
  input_pdf: string (required) "Path to the input PDF with fillable fields"
  output_json: string (required) "Path to write the field-info JSON"
```

```act.convert_pdf_to_images
CLI python3 ./scripts/convert_pdf_to_images.py "{pdf}" "{output_dir}"
  pdf: string (required) "Path to the input PDF"
  output_dir: string (required) "Directory to write one PNG per page"
```

```act.fill_fillable_fields
CLI python3 ./scripts/fill_fillable_fields.py "{input_pdf}" "{field_values_json}" "{output_pdf}"
  input_pdf: string (required) "Path to the input PDF with fillable fields"
  field_values_json: string (required) "Path to field_values.json with values to enter"
  output_pdf: string (required) "Path to write the filled PDF"
```

```act.create_validation_image
CLI python3 ./scripts/create_validation_image.py "{page_number}" "{fields_json}" "{input_image}" "{output_image}"
  page_number: string (required) "1-based page number to validate"
  fields_json: string (required) "Path to fields.json with bounding boxes"
  input_image: string (required) "Path to the page PNG to draw on"
  output_image: string (required) "Path to write the validation image"
```

```act.check_bounding_boxes
CLI python3 ./scripts/check_bounding_boxes.py "{fields_json}"
  fields_json: string (required) "Path to fields.json to validate for intersecting/too-small boxes"
```

```act.fill_pdf_form_with_annotations
CLI python3 ./scripts/fill_pdf_form_with_annotations.py "{input_pdf}" "{fields_json}" "{output_pdf}"
  input_pdf: string (required) "Path to the input PDF (non-fillable form)"
  fields_json: string (required) "Path to fields.json with bounding boxes and entry text"
  output_pdf: string (required) "Path to write the annotated PDF"
```
