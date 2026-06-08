---
title: Image OCR (Tesseract)
name: jpg-ocr-stat-image-ocr
type: app
version: 0.1.0
description: Extract text from a single image with Tesseract OCR. Single-pass (with confidence) or multi-pass for hard images.
tags: [ocr, tesseract, image]
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# Image OCR — Tesseract

Read text out of one image (`.jpg/.jpeg/.png/.webp/.tif/.bmp`) using Tesseract.
Returns JSON: `extracted_text`, plus a `confidence` band (single-pass).

- **Single pass** (default): one clean read with per-word confidence. Fast.
- **Multi-pass** (`--multipass`): several preprocess variants × PSM modes, text
  concatenated. Slower but recovers more from faded/low-contrast scans.

For batch receipt → xlsx, use `@home` instead. For handwriting or stylized
fonts where Tesseract fails, try `@vision`.

```act.ocr
CLI python3 ./scripts/image_ocr.py --image "{image}" --lang {lang} --psm {psm}
  image: string (required) "Path to the image file"
  lang: string (optional) "Tesseract language(s), e.g. eng or eng+fra" = "eng"
  psm: string (optional) "Page segmentation mode (3=auto, 6=block, 4=column, 11=sparse)" = "3"
```

```act.ocr_multipass
CLI python3 ./scripts/image_ocr.py --image "{image}" --lang {lang} --multipass
  image: string (required) "Path to the image file"
  lang: string (optional) "Tesseract language(s)" = "eng"
```

next: `/act.ocr --image <path>` · hard image → `/act.ocr_multipass` · vision → `@vision`
