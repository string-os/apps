---
title: Object Counter
name: object-counter
namespace: stringhub
type: app
version: 0.1.0
description: Count occurrences of an object in the image using computer vision algorithm.
tags: [object-counting, computer-vision, opencv]
---

# Object Counter

Count how many times a template object appears in an image through one action — the
daemon runs the bundled OpenCV normalized-correlation matcher, so you pass the two
image paths plus two tuning values instead of writing the CV code. The action prints
the count. **Its flags are listed below** (all required); they're complete, so you
shouldn't need `/act.count --help`.

## Count
- **`/act.count`** `--input_image <path>` `--object_image <path>` `--threshold <0-1>` `--dedup_min_dist <px>` — count occurrences of `object_image` (the template) inside `input_image`.
  - `threshold`: match cutoff; use a high value like `0.9` for high-fidelity counting.
  - `dedup_min_dist`: Non-Maximum Suppression min distance to merge duplicate hits; a good default is `3`.

```act.count
CLI python3 ./scripts/count_objects.py --tool count --input_image "{input_image}" --object_image "{object_image}" --threshold "{threshold}" --dedup_min_dist "{dedup_min_dist}"
  input_image: string (required) "Path to input image containing one or multiple objects"
  object_image: string (required) "Path to the object/template image to count"
  threshold: string (required) "Match threshold (e.g. 0.9 for high fidelity)"
  dedup_min_dist: string (required) "Non-Maximum Suppression min distance (e.g. 3)"
```
