---
title: FFmpeg Format Conversion
name: ffmpeg-format-conversion
namespace: stringhub
type: app
version: 0.2.0
description: Convert media files between formats - video containers, audio formats, and codec transcoding
tags: [ffmpeg, conversion, transcode, codec]
---

# FFmpeg Format Conversion

Convert media between containers, codecs, and audio formats through actions —
the daemon runs `ffmpeg`, so you pass the input/output paths and the few codec /
quality knobs instead of writing flags. The output container is chosen by the
output file extension (`.mp4`, `.mkv`, `.webm`, `.mp3`, `.m4a`, `.opus`, `.flac`, …).
**Each action's flags are listed below** (required unless shown in `[...]`, which marks
an optional flag and its default). The flags here are complete — you shouldn't need
`/act.<name> --help`.

## Convert
- **`/act.copy`** `--input <path>` `--output <path>` — remux into a new container with `-c copy` (fast, no re-encode, no quality loss). Use when you only need to change the container and the codecs are already compatible.
- **`/act.convert`** `--input <path>` `--output <path>` `[--vcodec <c>]` `[--acodec <c>]` `[--crf <n>]` `[--preset <p>]` `[--vbitrate <b>]` `[--abitrate <b>]` — re-encode. `vcodec` (`libx264`/`libx265`/`libvpx-vp9`/`libaom-av1`), `acodec` (`aac`/`libmp3lame`/`libopus`/`flac`), quality via `crf` (18–23 good for H.264, lower = better) or explicit `vbitrate`/`abitrate` (e.g. `2M`/`192k`), and the x264/x265 `preset` (ultrafast…veryslow; faster = larger). Omit any knob to let ffmpeg default it.

```act.copy
CLI python3 ./scripts/convert_media.py copy "{input}" "{output}"
  input: string (required) "Path to the input media file"
  output: string (required) "Output path; extension sets the target container"
```

```act.convert
CLI python3 ./scripts/convert_media.py convert "{input}" "{output}" "{vcodec}" "{acodec}" "{crf}" "{preset}" "{vbitrate}" "{abitrate}"
  input: string (required) "Path to the input media file"
  output: string (required) "Output path; extension sets the target container/format"
  vcodec: string (optional) "Video codec e.g. libx264, libx265, libvpx-vp9, libaom-av1" = ""
  acodec: string (optional) "Audio codec e.g. aac, libmp3lame, libopus, flac" = ""
  crf: string (optional) "Constant Rate Factor (lower = better quality, e.g. 23)" = ""
  preset: string (optional) "x264/x265 speed preset e.g. fast, medium, slow" = ""
  vbitrate: string (optional) "Target video bitrate e.g. 2M" = ""
  abitrate: string (optional) "Target audio bitrate e.g. 192k" = ""
```
