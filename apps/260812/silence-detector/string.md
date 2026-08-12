---
title: Silence Detector
name: silence-detector
namespace: stringhub
type: app
version: 0.2.0
description: "Detect initial silence segments in audio/video using energy-based analysis. Use when you need to find low-energy periods at the start of recordings (title slides, setup time, pre-roll silence)."
tags: [audio, silence, energy, numpy]
---

# Silence Detector

Find the initial silence (pre-roll / title-card / setup) in an energy profile from
energy-calculator. It builds a baseline from the first N seconds, smooths the energy, and
marks the transition where smoothed energy exceeds baseline × multiplier. Output is a
segment-combiner-compatible JSON (empty `segments` if no clear transition). The action
runs the numpy code.

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action writes JSON to `--output`; you should not
need `/act.detect --help`.

## Detect
- **`/act.detect`** `--energies <path.json>` `--output <path.json>`
  `[--threshold_multiplier <m>]` (default `1.5`) `[--initial_window <s>]` (default `60`)
  `[--smoothing_window <s>]` (default `30`) — detect the initial silence segment from an
  energies JSON (output of energy-calculator).

Tuning: lower `--threshold_multiplier` = more sensitive; `--initial_window` sets how many
seconds form the baseline; `--smoothing_window` controls smoothing.

```act.detect
CLI python3 ./scripts/detect_silence.py --energies "{energies}" --output "{output}" --threshold-multiplier {threshold_multiplier} --initial-window {initial_window} --smoothing-window {smoothing_window}
  energies: string (required) "Path to energy JSON file (from energy-calculator)"
  output: string (required) "Path to output JSON file"
  threshold_multiplier: number (optional) "Energy threshold multiplier" = "1.5"
  initial_window: number (optional) "Seconds for baseline calculation" = "60"
  smoothing_window: number (optional) "Moving average window" = "30"
```
