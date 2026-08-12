---
title: FFmpeg Video Filters
name: ffmpeg-video-filters
namespace: stringhub
type: app
version: 0.2.0
description: Apply video filters - scale, crop, watermark, speed, blur, and visual effects
tags: [ffmpeg, filters, scale, crop, overlay]
---

# FFmpeg Video Filters

Apply one video filter per action — the daemon runs `ffmpeg -vf`/`-filter_complex`,
so you pass paths and a few parameters instead of writing filter strings. Use `-2`
for a scale dimension to keep the aspect ratio. **Each action's flags are listed below**
(required unless shown in `[...]`, which marks an optional flag and its default). The
flags here are complete — you shouldn't need `/act.<name> --help`.

## Filters
- **`/act.scale`** `--input <path>` `--output <path>` `[--width <px|-2>]` (default `-2`) `[--height <px|-2>]` (default `-2`) `[--flags <algo>]` — resize; use `-2` on one dimension to preserve aspect ratio; `flags` e.g. `lanczos`.
- **`/act.crop`** `--input <path>` `--output <path>` `--width <px>` `--height <px>` `[--x <px>]` `[--y <px>]` — crop to width x height, from offset `x`,`y` (omit for centered).
- **`/act.watermark`** `--input <path>` `--output <path>` `--overlay <img>` `[--position <expr>]` (default `10:10`) — overlay an image; `position` is an overlay expr like `10:10`, `W-w-10:H-h-10`, or `(W-w)/2:(H-h)/2`.
- **`/act.speed`** `--input <path>` `--output <path>` `--factor <n>` `[--noaudio 1]` — change playback speed (`2.0` = 2x faster, `0.5` = half); applies `setpts` + `atempo`, or drops audio with `--noaudio 1`.
- **`/act.blur`** `--input <path>` `--output <path>` `[--kind box|gaussian]` (default `box`) `[--param <p>]` — `box` (boxblur, `param` = `radius:power` e.g. `10:5`) or `gaussian` (gblur, `param` = sigma).
- **`/act.eq`** `--input <path>` `--output <path>` `[--brightness <n>]` `[--contrast <n>]` `[--saturation <n>]` — adjust any of brightness / contrast / saturation (leave others blank).
- **`/act.rotate`** `--input <path>` `--output <path>` `--degrees <90cw|90ccw|180>` — rotate via transpose.
- **`/act.fade`** `--input <path>` `--output <path>` `[--type in|out|both]` (default `in`) `[--start <sec>]` (default `0`) `[--duration <sec>]` (default `2`) — fade in/out (`start` = the OUT start for `both`).

```act.scale
CLI python3 ./scripts/vfilter.py scale "{input}" "{output}" "{width}" "{height}" "{flags}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the scaled video"
  width: string (optional) "Target width, or -2 to keep aspect ratio" = "-2"
  height: string (optional) "Target height, or -2 to keep aspect ratio" = "-2"
  flags: string (optional) "Scaling algorithm, e.g. lanczos" = ""
```

```act.crop
CLI python3 ./scripts/vfilter.py crop "{input}" "{output}" "{width}" "{height}" "{x}" "{y}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the cropped video"
  width: string (required) "Crop width"
  height: string (required) "Crop height"
  x: string (optional) "X offset (omit for centered)" = ""
  y: string (optional) "Y offset (omit for centered)" = ""
```

```act.watermark
CLI python3 ./scripts/vfilter.py watermark "{input}" "{output}" "{overlay}" "{position}"
  input: string (required) "Path to the base video"
  output: string (required) "Path to write the watermarked video"
  overlay: string (required) "Path to the overlay image (e.g. logo.png)"
  position: string (optional) "Overlay position expression" = "10:10"
```

```act.speed
CLI python3 ./scripts/vfilter.py speed "{input}" "{output}" "{factor}" "{noaudio}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the speed-adjusted video"
  factor: string (required) "Speed factor: 2.0 = 2x faster, 0.5 = half speed"
  noaudio: string (optional) "Set to 1 to change video speed only (drop audio)" = ""
```

```act.blur
CLI python3 ./scripts/vfilter.py blur "{input}" "{output}" "{kind}" "{param}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the blurred video"
  kind: string (optional) "'box' (default) or 'gaussian'" = "box"
  param: string (optional) "box: 'radius:power' e.g. 10:5; gaussian: sigma e.g. 5" = ""
```

```act.eq
CLI python3 ./scripts/vfilter.py eq "{input}" "{output}" "{brightness}" "{contrast}" "{saturation}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the adjusted video"
  brightness: string (optional) "Brightness delta, e.g. 0.1" = ""
  contrast: string (optional) "Contrast factor, e.g. 1.2" = ""
  saturation: string (optional) "Saturation factor, e.g. 1.5" = ""
```

```act.rotate
CLI python3 ./scripts/vfilter.py rotate "{input}" "{output}" "{degrees}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the rotated video"
  degrees: string (required) "One of: 90cw, 90ccw, 180"
```

```act.fade
CLI python3 ./scripts/vfilter.py fade "{input}" "{output}" "{type}" "{start}" "{duration}"
  input: string (required) "Path to the input video"
  output: string (required) "Path to write the faded video"
  type: string (optional) "in, out, or both" = "in"
  start: string (optional) "Fade start time in seconds (the OUT start for 'both')" = "0"
  duration: string (optional) "Fade duration in seconds" = "2"
```
