---
title: Image Editing
name: image-editing
namespace: stringhub
type: app
version: 0.2.0
description: Comprehensive command-line tools for modifying and manipulating images, such as resize, blur, crop, flip, and many more.
tags: [imagemagick, convert, image, resize]
---

# Image Editing

Modify images through actions — the daemon runs ImageMagick's `convert`, so you pass
the input/output paths and a parameter instead of writing operator flags. The output
file extension sets the target format (e.g. write `.jpg` to convert a PNG to JPEG).
All actions print JSON. **Each action's flags are listed below** (required unless shown
in `[...]`, which marks an optional flag and its default). The flags here are complete —
you shouldn't need `/act.<name> --help`.

## Operations
- **`/act.resize`** `--input <path>` `--output <path>` `--geometry <geo>` — resize by a geometry: `50%`, `256x256` (max dimension, aspect kept), etc.
- **`/act.format`** `--input <path>` `--output <path>` — re-save in the format implied by the output extension (e.g. `.png` → `.jpg`).
- **`/act.auto_orient`** `--input <path>` `--output <path>` — read the EXIF Orientation and rotate so the image is upright, then reset the tag.
- **`/act.blur`** `--input <path>` `--output <path>` `--amount <radiusxsigma>` — Gaussian blur; `radiusxsigma` (sigma is what matters), e.g. `0x8`.
- **`/act.border`** `--input <path>` `--output <path>` `--value <pct>` `[--color <c>]` — add a border `value%` of width/height; `color` defaults to ImageMagick gray.
- **`/act.brightness_contrast`** `--input <path>` `--output <path>` `--brightness <n>` `[--contrast <n>]` — adjust brightness (and optional contrast), each -100..+100; 0 = no change.
- **`/act.blue_shift`** `--input <path>` `--output <path>` `[--factor <n>]` (default `1.5`) — moonlight/night simulation; start with factor 1.5.
- **`/act.contrast`** `--input <path>` `--output <path>` `[--direction up|down]` (default `up`) — enhance (`up`) or reduce (`down`) contrast.

```act.resize
CLI python3 ./scripts/img.py resize "{input}" "{output}" "{geometry}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the resized image"
  geometry: string (required) "Resize geometry, e.g. 50% or 256x256"
```

```act.format
CLI python3 ./scripts/img.py format "{input}" "{output}"
  input: string (required) "Path to the input image"
  output: string (required) "Output path; extension sets the target format"
```

```act.auto_orient
CLI python3 ./scripts/img.py auto_orient "{input}" "{output}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the oriented image"
```

```act.blur
CLI python3 ./scripts/img.py blur "{input}" "{output}" "{amount}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the blurred image"
  amount: string (required) "radiusxsigma, e.g. 0x8 (sigma controls the blur)"
```

```act.border
CLI python3 ./scripts/img.py border "{input}" "{output}" "{value}" "{color}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the bordered image"
  value: string (required) "Border size as a percent, e.g. 5%"
  color: string (optional) "Border color, e.g. black or #DFDFDF" = ""
```

```act.brightness_contrast
CLI python3 ./scripts/img.py brightness_contrast "{input}" "{output}" "{brightness}" "{contrast}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the adjusted image"
  brightness: string (required) "Brightness, -100..+100 (0 = no change)"
  contrast: string (optional) "Contrast, -100..+100 (0 = no change)" = ""
```

```act.blue_shift
CLI python3 ./scripts/img.py blue_shift "{input}" "{output}" "{factor}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the night-simulated image"
  factor: string (optional) "Blue-shift factor, start at 1.5" = "1.5"
```

```act.contrast
CLI python3 ./scripts/img.py contrast "{input}" "{output}" "{direction}"
  input: string (required) "Path to the input image"
  output: string (required) "Path to write the contrasted image"
  direction: string (optional) "'up' (enhance, default) or 'down' (reduce)" = "up"
```
