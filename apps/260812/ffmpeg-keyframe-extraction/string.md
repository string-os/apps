---
title: FFmpeg Keyframe Extraction
name: ffmpeg-keyframe-extraction
namespace: stringhub
type: app
version: 0.2.0
description: Extract key frames (I-frames) from video files using FFmpeg command line tool. Use this skill when the user needs to pull out keyframes, thumbnails, or important frames from MP4, MKV, AVI, or other video formats for analysis, previews, or processing.
tags: [ffmpeg, keyframe, iframe, extract]
---

# FFmpeg Keyframe Extraction

Pull I-frames (keyframes) out of a video through one action — the daemon runs
`ffmpeg`, so you give the input and an output pattern instead of writing the
select/skip filter flags. The output file extension (`.png`, `.jpg`, `.bmp`) sets
the image format; include a counter like `keyframe_%03d.png` in the pattern. **The
action's flags are listed below** (required unless shown in `[...]`, which marks an
optional flag and its default). The flags here are complete — you shouldn't need
`/act.extract --help`.

## Extract
- **`/act.extract`** `--input <path>` `--out_pattern <pat>` `[--method select|skip]` (default `select`) `[--quality <1-31>]` `[--frame_pts 1]` — write one image per keyframe.
  - `method`: `select` uses `select='eq(pict_type,I)'` — more filtering control; `skip` uses `-skip_frame nokey` — faster (skips decoding non-keyframes). Both use `-vsync vfr` to avoid duplicate frames.
  - `quality`: `-q:v` for JPEG output (1–31, lower = better).
  - `frame_pts`: set to 1 to put the presentation timestamp in each filename.

```act.extract
CLI python3 ./scripts/keyframes.py "{input}" "{out_pattern}" "{method}" "{quality}" "{frame_pts}"
  input: string (required) "Path to the input video (MP4, MKV, AVI, MOV, ...)"
  out_pattern: string (required) "Output pattern with a counter + extension, e.g. keyframe_%03d.png"
  method: string (optional) "'select' (default, more control) or 'skip' (faster)" = "select"
  quality: string (optional) "JPEG quality via -q:v, 1-31 (lower = better)" = ""
  frame_pts: string (optional) "Set to 1 to use the presentation timestamp in filenames" = ""
```
