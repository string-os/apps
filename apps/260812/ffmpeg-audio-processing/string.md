---
title: FFmpeg Audio Processing
name: ffmpeg-audio-processing
namespace: stringhub
type: app
version: 0.2.0
description: Extract, normalize, mix, and process audio tracks - audio manipulation and analysis
tags: [ffmpeg, audio, normalize, mix]
---

# FFmpeg Audio Processing

Extract and process audio through actions — the daemon runs `ffmpeg`/`ffprobe`, so
you pass paths and a few parameters instead of writing filter strings. **Each action's
flags are listed below** (required unless shown in `[...]`, which marks an optional flag
and its default). All actions print JSON; analysis returns the meter's raw measurement
text. The flags here are complete — you shouldn't need `/act.<name> --help`.

## Extract / convert
- **`/act.extract`** `--input <path>` `--output <path>` `[--format <fmt>]` (default infer from output ext) — pull the audio out of a video (`-vn`); `format` = `mp3`, `aac` (stream-copy), or `wav` (pcm).
- **`/act.resample`** `--input <path>` `--output <path>` `--rate <Hz>` — change sample rate (e.g. 48000) via `aresample` + `-ar`.
- **`/act.channels`** `--input <path>` `--output <path>` `--mode <left|right|mono|stereo>` — extract one channel (`left`/`right`) or set channel count (`mono`/`stereo`).
- **`/act.concat`** `--inputs "<a.mp3 b.mp3 ...>"` `--output <path>` — join several audio files (`-f concat -c copy`); `--inputs` is ONE quoted, space-separated string.

## Levels
- **`/act.normalize`** `--input <path>` `--output <path>` `[--mode loudnorm|volume]` (default `loudnorm`) `[--value <n>]` — `loudnorm` (ITU-R BS.1770: I=-23, TP=-1.5, LRA=11; `value` overrides target I) or simple `volume` (value = factor).
- **`/act.volume`** `--input <path>` `--output <path>` `--value <adj>` — apply a `volume=` adjustment (`6dB`, `-3dB`, `0.5`, …).
- **`/act.analyze`** `--input <path>` `[--mode volumedetect|ebur128|stats]` (default `volumedetect`) — measure levels: `volumedetect`, `ebur128` (LUFS), or `stats` (sample rate/channels/bitrate JSON).

## Mix / timing / filter
- **`/act.mix`** `--video <path>` `--audio <path>` `--output <path>` `[--voice_vol <v>]` `[--music_vol <v>]` — replace a video's audio track, or (with both vols set) `amix` two tracks under volume control.
- **`/act.delay`** `--input <path>` `--output <path>` `--milliseconds <ms>` — delay audio by N milliseconds (`adelay`).
- **`/act.filter`** `--input <path>` `--output <path>` `--kind <highpass|lowpass|bandpass|fadeinout>` `[--freq <Hz>]` `[--width <n>]` — `highpass`/`lowpass` (cutoff via `freq`), `bandpass` (`freq` center + `width`), or `fadeinout` (afade; `freq` = fade-out start, `width` = fade duration).

```act.extract
CLI python3 ./scripts/audio.py extract "{input}" "{output}" "{format}"
  input: string (required) "Path to the video/media file"
  output: string (required) "Path to write the audio"
  format: string (optional) "mp3, aac, wav, or omit to infer from extension" = ""
```

```act.resample
CLI python3 ./scripts/audio.py resample "{input}" "{output}" "{rate}"
  input: string (required) "Path to the input media"
  output: string (required) "Path to write the resampled audio"
  rate: string (required) "Sample rate in Hz, e.g. 48000"
```

```act.channels
CLI python3 ./scripts/audio.py channels "{input}" "{output}" "{mode}"
  input: string (required) "Path to the input media"
  output: string (required) "Path to write the result"
  mode: string (required) "left, right, mono, or stereo"
```

```act.concat
CLI python3 ./scripts/audio.py concat "{inputs}" "{output}"
  inputs: string (required) "Quoted space-separated audio paths, e.g. 'a.mp3 b.mp3'"
  output: string (required) "Path to write the concatenated audio"
```

```act.normalize
CLI python3 ./scripts/audio.py normalize "{input}" "{output}" "{mode}" "{value}"
  input: string (required) "Path to the input media"
  output: string (required) "Path to write the normalized output"
  mode: string (optional) "'loudnorm' (default) or 'volume'" = "loudnorm"
  value: string (optional) "loudnorm: target integrated LUFS (default -23); volume: factor" = ""
```

```act.volume
CLI python3 ./scripts/audio.py volume "{input}" "{output}" "{value}"
  input: string (required) "Path to the input media"
  output: string (required) "Path to write the output"
  value: string (required) "Volume adjustment, e.g. 6dB, -3dB, 0.5"
```

```act.analyze
CLI python3 ./scripts/audio.py analyze "{input}" "{mode}"
  input: string (required) "Path to the input media"
  mode: string (optional) "volumedetect (default), ebur128, or stats" = "volumedetect"
```

```act.mix
CLI python3 ./scripts/audio.py mix "{video}" "{audio}" "{output}" "{voice_vol}" "{music_vol}"
  video: string (required) "Path to the video providing the visual track"
  audio: string (required) "Path to the audio to add/replace"
  output: string (required) "Path to write the muxed output"
  voice_vol: string (optional) "Original-track volume for amix (omit to just replace)" = ""
  music_vol: string (optional) "Added-track volume for amix" = ""
```

```act.delay
CLI python3 ./scripts/audio.py delay "{input}" "{output}" "{milliseconds}"
  input: string (required) "Path to the input media"
  output: string (required) "Path to write the delayed output"
  milliseconds: string (required) "Delay in milliseconds, e.g. 500"
```

```act.filter
CLI python3 ./scripts/audio.py filter "{input}" "{output}" "{kind}" "{freq}" "{width}"
  input: string (required) "Path to the input media"
  output: string (required) "Path to write the filtered output"
  kind: string (required) "highpass, lowpass, bandpass, or fadeinout"
  freq: string (optional) "Cutoff/center frequency (or fade-out start for fadeinout)" = ""
  width: string (optional) "bandpass width, or fade duration for fadeinout" = ""
```
