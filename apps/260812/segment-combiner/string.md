---
title: Segment Combiner
name: segment-combiner
namespace: stringhub
type: app
version: 0.2.0
description: "Combine multiple segment detection results into a unified list. Use when you need to merge segments from different detectors, prepare removal lists for video processing, or consolidate detection outputs."
tags: [segments, merge, video, json]
---

# Segment Combiner

Merge several segment JSON files (each with a `segments` array, e.g. one from
silence-detector and one from pause-detector) into a single sorted list ready for
video-processor's removal input. The action runs the merge. Output is sorted by start
time with totals.

All flags are listed inline below (all required). The action writes JSON to `--output`;
you should not need `/act.combine --help`.

## Combine
- **`/act.combine`** `--segments "<a.json b.json ...>"` `--output <path.json>` — merge two
  or more segment JSONs into one sorted list. `--segments` is ONE space-separated quoted
  string of input files (e.g. `--segments "silence.json pauses.json"`), split inside the
  action.

```act.combine
CLI sh -c 'python3 ./scripts/combine_segments.py --segments $1 --output "$2"' _ {segments} "{output}"
  segments: string (required) "One or more segment JSON files as a single space-separated quoted string, e.g. a.json b.json"
  output: string (required) "Path to output combined segments JSON"
```
