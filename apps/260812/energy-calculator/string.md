---
title: Energy Calculator
name: energy-calculator
namespace: stringhub
type: app
version: 0.2.0
description: "Calculate per-second RMS energy from audio files. Use when you need to analyze audio volume patterns, prepare data for silence/pause detection, or create an energy profile for audio analysis tasks."
tags: [audio, rms, energy, numpy, analysis]
---

# Energy Calculator

Turn a WAV file into a per-window RMS energy profile (JSON: per-window `energies` plus
min/max/mean/std stats). RMS tracks perceived loudness, so the output feeds
silence-detector and pause-detector. The action runs the numpy code for you. Needs numpy.

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action writes JSON to `--output`; you should not
need `/act.calc --help`.

## Calculate
- **`/act.calc`** `--audio <path.wav>` `--output <path.json>` `[--window_seconds <s>]` (default `1`)
  — compute RMS energy per window over a WAV and write the profile JSON. Lower
  `--window_seconds` (e.g. `0.5`) for finer time resolution.

```act.calc
CLI python3 ./scripts/calc_energy.py --audio "{audio}" --output "{output}" --window-seconds {window_seconds}
  audio: string (required) "Path to input WAV file"
  output: string (required) "Path to output JSON file"
  window_seconds: number (optional) "Window size for energy calculation (seconds)" = "1"
```
