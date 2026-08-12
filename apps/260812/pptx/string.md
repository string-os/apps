---
title: Pptx
name: pptx
namespace: stringhub
type: app
version: 0.2.0
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks"
tags: [pptx, powerpoint, ooxml, presentations]
---

[!requirements](./requirements.txt)

# PPTX

A .pptx is a ZIP of XML parts. These actions run the bundled OOXML/python tooling so
you edit the raw XML directly instead of writing the code yourself. **Each action's flags
are listed below** (required unless shown in `[...]`, which marks an optional flag and its
default). Each action prints its result (or the path it wrote); the flags here are complete,
so you shouldn't need `/act.<name> --help`. For plain text, run `markitdown` on the file;
to render slides, use `soffice` — those are system tools, not actions here.

## Inspect / render
- **`/act.inventory`** `--pptx_file <path>` `--output_json <path>` — extract every text shape
  (position, placeholder type, paragraph formatting) to JSON. Run before `/act.replace`.
- **`/act.thumbnail`** `--pptx_file <path>` `[--output_prefix <prefix>]` (default `thumbnails`)
  `[--cols <3-6>]` (default `5`) — render a JPEG grid of the slides to eyeball layout/overflow.

## Edit raw XML (unpack → edit → validate → pack)
- **`/act.unpack`** `--office_file <path>` `--output_dir <dir>` — explode a .pptx into its XML
  parts (`ppt/slides/slideN.xml`, theme, notes, comments…).
- **`/act.validate`** `--dir <unpacked_dir>` `--original <path>` — schema-check the unpacked dir
  against the original .pptx. Run after EVERY XML edit; fix all errors before packing.
- **`/act.pack`** `--input_directory <unpacked_dir>` `--office_file <out.pptx>` — repack into a .pptx.

## Template-based authoring
- **`/act.rearrange`** `--template <path>` `--output <out.pptx>` `--order <0,34,34,50>` — duplicate /
  reorder / delete template slides by comma-separated 0-based index list.
- **`/act.replace`** `--input_pptx <path>` `--replacement_json <path>` `--output_pptx <out.pptx>` —
  apply a per-shape replacement JSON built from `/act.inventory`; shapes you omit are cleared.

Editing flow: `/act.unpack` → edit the slide XML → `/act.validate` (repeat until clean) → `/act.pack`.
Template flow: `/act.rearrange` → `/act.inventory` → write replacement JSON → `/act.replace`.

`ooxml.md` and `html2pptx.md` are bundled as deep OOXML / html2pptx-library reference —
read them only if you need raw schema or library details. `html2pptx.js` is the
creation library you import from your own script (no action).

```act.unpack
CLI python3 ./ooxml/scripts/unpack.py "{office_file}" "{output_dir}"
  office_file: string (required) "Path to the .pptx to unpack"
  output_dir: string (required) "Directory to write the unpacked OOXML parts into"
```

```act.validate
CLI python3 ./ooxml/scripts/validate.py "{dir}" --original "{original}"
  dir: string (required) "Unpacked OOXML directory to validate"
  original: string (required) "Path to the original .pptx the dir was unpacked from"
```

```act.pack
CLI python3 ./ooxml/scripts/pack.py "{input_directory}" "{office_file}"
  input_directory: string (required) "Unpacked OOXML directory to repack"
  office_file: string (required) "Output .pptx path to write"
```

```act.thumbnail
CLI ./scripts/thumb.sh "{pptx_file}" "{output_prefix}" "{cols}"
  pptx_file: string (required) "Path to the .pptx to render thumbnails from"
  output_prefix: string (optional) "Output prefix/path for the grid (default: thumbnails)" = ""
  cols: string (optional) "Columns per grid, 3-6 (default 5)" = ""
```

```act.rearrange
CLI python3 ./scripts/rearrange.py "{template}" "{output}" "{order}"
  template: string (required) "Source template .pptx"
  output: string (required) "Output .pptx to write"
  order: string (required) "Comma-separated 0-based slide indices, e.g. 0,34,34,50,52"
```

```act.inventory
CLI python3 ./scripts/inventory.py "{pptx_file}" "{output_json}"
  pptx_file: string (required) "Path to the .pptx to extract a text inventory from"
  output_json: string (required) "Output JSON path for the text inventory"
```

```act.replace
CLI python3 ./scripts/replace.py "{input_pptx}" "{replacement_json}" "{output_pptx}"
  input_pptx: string (required) "Working .pptx to apply replacements to"
  replacement_json: string (required) "JSON of replacement paragraphs per shape (from inventory)"
  output_pptx: string (required) "Output .pptx to write"
```
