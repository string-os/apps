---
title: OpenAI Vision OCR
name: jpg-ocr-stat-openai-vision
type: app
version: 0.1.0
requires:
  - OPENAI_API_KEY
description: OCR or analyze an image with an OpenAI vision model (gpt-4o). Fallback for handwriting, stylized fonts, or layouts Tesseract mishandles.
tags: [ocr, openai, vision, gpt-4o]
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# OpenAI Vision OCR

Send one image to an OpenAI vision model and get text or a description back.
Stronger than Tesseract on **handwriting, stylized fonts, and complex layouts**,
at the cost of an API call (needs `OPENAI_API_KEY`, billed per image/token).

Default prompt extracts all text in reading order. Override `--prompt` to ask
anything ("describe the scene", "list the line items as JSON", ...).

> Needs `OPENAI_API_KEY` in the env. See `@requirements`. Without it the action
> returns an actionable error, not a crash.

```act.vision
CLI OPENAI_API_KEY=$OPENAI_API_KEY python3 ./scripts/openai_vision.py --image "{image}" --prompt "{prompt}" --model {model} --detail {detail}
  image: string (required) "Path to the image file"
  prompt: string (optional) "Instruction for the model" = "Extract ALL text from this image in reading order. Return only the text."
  model: string (optional) "Vision model id" = "gpt-4o"
  detail: string (optional) "low | high | auto (high is best for OCR)" = "high"
```

next: `/act.vision --image <path>` · cheaper local OCR → `@imageocr`
