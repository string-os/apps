---
title: Audio Extractor
name: audio-extractor
namespace: stringhub
type: app
version: 0.2.0
description: "Extract audio from video files to WAV format. Use when you need to analyze audio from video, prepare audio for energy calculation, or convert video audio to standard format for processing."
tags: [audio, video, ffmpeg, wav, extraction]
---

# Audio Extractor

Extract a video's audio to WAV (mono, 16-bit PCM) for downstream analysis. The action
runs the underlying ffmpeg pipeline — call it with paths instead of writing ffmpeg
yourself. Output is mono at 16 kHz by default, which is enough for speech/energy work
and keeps files small. Needs `ffmpeg` on PATH.

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action prints JSON; you should not need
`/act.extract --help`.

## Extract
- **`/act.extract`** `--video <path>` `--output <path.wav>` `[--sample_rate <Hz>]` (default `16000`)
  `[--duration_flag "<--duration N>"]` (default empty = full video) — pull a video's audio
  into a WAV file. `--duration_flag` carries the literal sub-flag as its value: pass
  `--duration_flag "--duration 600"` to keep only the first 600s; omit it for the whole video.

```act.extract
CLI ./scripts/_optshim.sh python3 ./scripts/extract_audio.py --video "{video}" --output "{output}" --sample-rate {sample_rate} -- {duration_flag}
  video: string (required) "Path to input video file"
  output: string (required) "Path to output WAV file"
  sample_rate: number (optional) "Audio sample rate in Hz" = "16000"
  duration_flag: string (optional) "Optional duration limit, e.g. --duration 600 (empty = full video)" = ""
```
