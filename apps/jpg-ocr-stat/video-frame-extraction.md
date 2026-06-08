---
title: Video → frames
name: jpg-ocr-stat-video-frame-extraction
type: app
version: 0.1.0
description: Extract frames from a video into an image directory with OpenCV. Sample by frame interval or by seconds, with an optional cap.
tags: [video, frames, opencv, extraction]
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# Video → frames

Pull frames out of a video (`.mp4/.mov/.avi/.mkv/...`) into an image folder, so
you can OCR or analyze them downstream (`@imageocr`, `@vision`). Uses OpenCV.

Sampling:
- `--every N` keeps 1 of every N frames (default every frame).
- `--seconds S` keeps one frame every S seconds (overrides `--every`).
- `--max M` stops after M frames (0 = no cap) — handy to avoid flooding disk.

```act.frames
CLI python3 ./scripts/video_frames.py --video "{video}" --outdir "{outdir}" --every {every} --seconds {seconds} --max {max} --format {format}
  video: string (required) "Path to the video file"
  outdir: string (required) "Directory to write frames into"
  every: number (optional) "Keep 1 of every N frames" = "1"
  seconds: number (optional) "Seconds between frames (0 = use --every)" = "0"
  max: number (optional) "Max frames to save (0 = unlimited)" = "0"
  format: string (optional) "jpg | png" = "jpg"
```

next: `/act.frames --video <path> --outdir frames --seconds 1` then OCR via `@imageocr`
