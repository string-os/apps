---
title: Video Processor
name: video-processor
namespace: stringhub
type: app
version: 0.2.0
description: "Process videos by removing segments and concatenating remaining parts. Use when you need to remove detected pauses/openings from videos, create highlight reels, or batch process segment removals using ffmpeg filter_complex."
tags: [video, ffmpeg, segments, concatenation]
---

# Video Processor

Remove a set of time segments from a video and concatenate what's left, in one pass via
ffmpeg's filter_complex (CRF encoding, audio stays in sync). The action runs the ffmpeg
build/encode for you and also emits a stats report (original/output/removed durations,
compression %). Needs ffmpeg with libx264 + aac.

All flags are listed inline below (all required). The action prints a stats report; you
should not need `/act.process --help`.

## Process
- **`/act.process`** `--input <path>` `--output <path>` `--remove_segments "<a.json b.json ...>"`
  — remove segments from a video and write the trimmed output. `--remove_segments` is ONE
  space-separated quoted string of removal-segment JSONs (each with a `segments` array),
  e.g. `--remove_segments "opening.json pauses.json"`, split inside the action.

Note: encoding a long video can exceed a single action's time budget; for big inputs run
on a multi-core box and expect ~0.3× the video duration.

```act.process
CLI sh -c 'python3 ./scripts/process_video.py --input "$1" --output "$2" --remove-segments $3' _ "{input}" "{output}" {remove_segments}
  input: string (required) "Path to input video file"
  output: string (required) "Path to output video file"
  remove_segments: string (required) "One or more segment JSON files to remove, as a single space-separated quoted string, e.g. opening.json pauses.json"
```
