---
title: TTS Audio Mastering
name: text-to-speech
namespace: stringhub
type: app
version: 0.2.0
description: "Practical mastering steps for TTS audio: cleanup, loudness normalization, alignment, and delivery specs."
tags: [tts, audio, mastering, loudnorm]
---

# TTS Audio Mastering

Produce clean, delivery-ready TTS audio. The skill itself doesn't ship a TTS engine —
**you choose and run the engine**, then use these actions for the mastering steps it
documents. Engine guidance: neural offline (e.g. Kokoro) = stable/high-quality/no network;
cloud TTS (Edge-TTS / OpenAI TTS) = more natural but network-dependent; formant
(espeak-ng) = prototyping only. **Always confirm the generated audio's native sample
rate before resampling for video delivery.**

**Each action's flags are listed below** (required unless shown in `[...]`, which marks
an optional flag and its default). The flags here are complete — you shouldn't need
`/act.<name> --help`.

## Mastering pipeline (per segment, in order)
1. **`/act.cleanup`** `--input <path>` `--output <path>` `[--hp_hz <Hz>]` (default `20`) `[--lp_hz <Hz>]` `[--fade_ms <ms>]` (default `50`) — high-pass ~20 Hz (rumble/DC), optional low-pass ~16 kHz (harshness), and ~50 ms boundary fades (click/pop). Keep these consistent across all segments.
2. **`/act.measure`** `--input <path>` — read loudness with `ebur128` (ITU-R BS.1770). Targets: ≈ -23 LUFS integrated, ≈ -1.5 dBTP true peak, LRA ≈ 11.
3. **`/act.normalize`** `--input <path>` `--output <path>` `[--target_lufs <n>]` (default `-23`) — apply `loudnorm` as the **final** step, after cleanup and timing edits. If you change tempo/duration afterward, re-normalize.

## Timing & boundaries
- **`/act.pad`** `--input <path>` `--output <path>` `--target_seconds <sec>` — pad a segment with trailing silence to hit its target window length. If a segment is too long instead, trim it or apply a gentle speed change (use the ffmpeg-audio-processing skill). Re-apply boundary fades after any pad/trim.
- Sync guideline: keep end-to-end drift small (≤ 0.2 s) unless the task says otherwise.

```act.cleanup
CLI python3 ./scripts/master.py cleanup "{input}" "{output}" "{hp_hz}" "{lp_hz}" "{fade_ms}"
  input: string (required) "Path to the TTS audio segment"
  output: string (required) "Path to write the cleaned segment"
  hp_hz: string (optional) "High-pass cutoff in Hz" = "20"
  lp_hz: string (optional) "Optional low-pass cutoff in Hz, e.g. 16000" = ""
  fade_ms: string (optional) "Boundary fade length in milliseconds" = "50"
```

```act.measure
CLI python3 ./scripts/master.py measure "{input}"
  input: string (required) "Path to the audio to measure (ebur128 loudness)"
```

```act.normalize
CLI python3 ./scripts/master.py normalize "{input}" "{output}" "{target_lufs}"
  input: string (required) "Path to the audio to normalize"
  output: string (required) "Path to write the normalized audio"
  target_lufs: string (optional) "Integrated loudness target (LUFS)" = "-23"
```

```act.pad
CLI python3 ./scripts/master.py pad "{input}" "{output}" "{target_seconds}"
  input: string (required) "Path to the audio segment"
  output: string (required) "Path to write the padded segment"
  target_seconds: string (required) "Target window length in seconds"
```
