---
title: FFmpeg Video Editing
name: ffmpeg-video-editing
namespace: stringhub
type: app
version: 0.2.0
description: Cut, trim, concatenate, and split video files - basic video editing operations
tags: [ffmpeg, video, trim, concat]
---

# FFmpeg Video Editing

Basic cut / trim / concatenate / split operations through actions — the daemon
runs `ffmpeg`, so you pass paths and times instead of writing flags. Times are
`HH:MM:SS` or seconds. `-c copy` is the fast default (keyframe-accurate); set
`reencode` for frame-accurate cuts or to bridge differing codecs. **Each action's
flags are listed below** (required unless shown in `[...]`, which marks an optional flag
and its default). The flags here are complete — you shouldn't need `/act.<name> --help`.

## Edit
- **`/act.cut`** `--input <path>` `--output <path>` `--start <time>` `[--end <time>]` `[--duration <sec>]` `[--reencode 1]` — extract one segment. Give `start` plus either `end` OR `duration`. Stream-copy by default; `--reencode 1` for a precise (re-encoded) cut.
- **`/act.concat`** `--inputs "<a.mp4 b.mp4 ...>"` `--output <path>` `[--reencode 1]` — join clips with the file-list method (the skill's recommended approach). `--inputs` is ONE quoted space-separated string; `-c copy` requires matching codecs, else `--reencode 1`.
- **`/act.split`** `--input <path>` `--out_pattern <pat>` `--segment_seconds <sec>` — chop into fixed-length segments via `-f segment -segment_time`; `out_pattern` carries the counter + ext, e.g. `out_%03d.mp4`.

```act.cut
CLI python3 ./scripts/edit.py cut "{input}" "{output}" "{start}" "{end}" "{duration}" "{reencode}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the cut segment"
  start: string (required) "Start time, HH:MM:SS or seconds"
  end: string (optional) "End time (use this OR duration)" = ""
  duration: string (optional) "Segment length in seconds (use this OR end)" = ""
  reencode: string (optional) "Set to 1 for a re-encoded, frame-accurate cut" = ""
```

```act.concat
CLI python3 ./scripts/edit.py concat "{inputs}" "{output}" "{reencode}"
  inputs: string (required) "Quoted space-separated input paths, e.g. 'a.mp4 b.mp4 c.mp4'"
  output: string (required) "Path to write the concatenated video"
  reencode: string (optional) "Set to 1 to re-encode (needed if codecs differ)" = ""
```

```act.split
CLI python3 ./scripts/edit.py split "{input}" "{out_pattern}" "{segment_seconds}"
  input: string (required) "Path to the input video"
  out_pattern: string (required) "Output pattern with a counter, e.g. out_%03d.mp4"
  segment_seconds: string (required) "Length of each segment in seconds, e.g. 60"
```
