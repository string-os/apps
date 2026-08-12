---
title: Pause Detector
name: pause-detector
namespace: stringhub
type: app
version: 0.2.0
description: "Detect pauses and silence in audio using local dynamic thresholds. Use when you need to find natural pauses in lectures, board-writing silences, or breaks between sections. Uses local context comparison to avoid false positives from volume variation."
tags: [audio, pauses, silence, threshold, scipy]
---

# Pause Detector

Find pauses / low-energy segments in an energy profile (from energy-calculator) using a
*local* dynamic threshold: each second is compared to a sliding-window local average, so
the detector adapts to changing speaker volume instead of using one global cutoff. Output
is a JSON list of `{start, end, duration}` segments. The action runs the numpy/scipy code.

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action writes JSON to `--output`; you should not
need `/act.detect --help`.

## Detect
- **`/act.detect`** `--energies <path.json>` `--output <path.json>` `[--start_time <s>]` (default `0`)
  `[--threshold_ratio <r>]` (default `0.5`) `[--min_duration <s>]` (default `2`)
  `[--window_size <s>]` (default `30`) — detect pause segments from an energies JSON
  (output of energy-calculator).

Tuning knobs (sensible defaults): lower `--threshold_ratio` = more aggressive; higher
`--min_duration` = only longer pauses; `--window_size` sets how much local context the
threshold averages over. Use `--start_time` to skip a known opening so it isn't reported
as one giant pause.

```act.detect
CLI python3 ./scripts/detect_pauses.py --energies "{energies}" --output "{output}" --start-time {start_time} --threshold-ratio {threshold_ratio} --min-duration {min_duration} --window-size {window_size}
  energies: string (required) "Path to energy JSON file (from energy-calculator)"
  output: string (required) "Path to output JSON file"
  start_time: number (optional) "Start analyzing from this second" = "0"
  threshold_ratio: number (optional) "Ratio of local average for low energy" = "0.5"
  min_duration: number (optional) "Minimum pause duration in seconds" = "2"
  window_size: number (optional) "Local average window size" = "30"
```
