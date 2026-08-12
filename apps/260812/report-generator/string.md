---
title: Report Generator
name: report-generator
namespace: stringhub
type: app
version: 0.2.0
description: "Generate compression reports for video processing. Use when you need to create structured JSON reports with duration statistics, compression ratios, and segment details after video processing."
tags: [video, report, compression, ffprobe]
---

# Report Generator

Build a JSON compression report comparing an original vs a processed video: original /
compressed / removed durations and the compression percentage (removed ÷ original × 100).
Durations are measured with ffprobe. The action runs it for you. Needs `ffprobe` (ffmpeg).

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action writes JSON to `--output`; you should not
need `/act.report --help`.

## Report
- **`/act.report`** `--original <path>` `--compressed <path>` `--output <path.json>`
  `[--segments_flag "<--segments file.json>"]` (default empty) — generate the compression
  report. `--segments_flag` carries the literal sub-flag as its value: pass
  `--segments_flag "--segments all_segments.json"` to also itemize what was cut.

```act.report
CLI ./scripts/_optshim.sh python3 ./scripts/generate_report.py --original "{original}" --compressed "{compressed}" --output "{output}" -- {segments_flag}
  original: string (required) "Path to original video file"
  compressed: string (required) "Path to compressed video file"
  output: string (required) "Path to output report JSON"
  segments_flag: string (optional) "Optional segments JSON, e.g. --segments all.json (empty = omit)" = ""
```
