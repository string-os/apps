---
title: FFmpeg Media Info
name: ffmpeg-media-info
namespace: stringhub
type: app
version: 0.2.0
description: Analyze media file properties - duration, resolution, bitrate, codecs, and stream information
tags: [ffmpeg, ffprobe, media, metadata]
---

# FFmpeg Media Info

Inspect media files through actions — the daemon runs the underlying `ffprobe`
command, so you call an action with a file path instead of writing probe flags.
All actions print JSON; values come straight from `ffprobe`. **Each action's flags
are listed below** (required unless shown in `[...]`, which marks an optional flag and
its default). The flags here are complete — you shouldn't need `/act.<name> --help`.

## Inspect
- **`/act.info`** `--input <path>` — full `-show_format -show_streams` dump as structured JSON (everything).
- **`/act.duration`** `--input <path>` — total duration in seconds.
- **`/act.resolution`** `--input <path>` — first video stream `WIDTHxHEIGHT`.
- **`/act.bitrate`** `--input <path>` `[--stream video]` — overall bitrate, or `--stream video` for the video stream's bitrate.
- **`/act.codec`** `--input <path>` `[--stream video|audio]` (default `video`) — codec name + long name.
- **`/act.sample_rate`** `--input <path>` — first audio stream sample rate.
- **`/act.channels`** `--input <path>` — first audio stream channel count.
- **`/act.framerate`** `--input <path>` — first video stream frame rate (`r_frame_rate`).
- **`/act.stream_count`** `--input <path>` `[--stream video|audio]` (default `video`) — number of video (or audio) streams.

```act.info
CLI python3 ./scripts/info.py info "{input}"
  input: string (required) "Path to the media file"
```

```act.duration
CLI python3 ./scripts/info.py duration "{input}"
  input: string (required) "Path to the media file"
```

```act.resolution
CLI python3 ./scripts/info.py resolution "{input}"
  input: string (required) "Path to the media file"
```

```act.bitrate
CLI python3 ./scripts/info.py bitrate "{input}" "{stream}"
  input: string (required) "Path to the media file"
  stream: string (optional) "'video' for the video stream bitrate; omit for overall" = ""
```

```act.codec
CLI python3 ./scripts/info.py codec "{input}" "{stream}"
  input: string (required) "Path to the media file"
  stream: string (optional) "'video' (default) or 'audio'" = "video"
```

```act.sample_rate
CLI python3 ./scripts/info.py sample_rate "{input}"
  input: string (required) "Path to the media file"
```

```act.channels
CLI python3 ./scripts/info.py channels "{input}"
  input: string (required) "Path to the media file"
```

```act.framerate
CLI python3 ./scripts/info.py framerate "{input}"
  input: string (required) "Path to the media file"
```

```act.stream_count
CLI python3 ./scripts/info.py stream_count "{input}" "{stream}"
  input: string (required) "Path to the media file"
  stream: string (optional) "'video' (default) or 'audio'" = "video"
```
