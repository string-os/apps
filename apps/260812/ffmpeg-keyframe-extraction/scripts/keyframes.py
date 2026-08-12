#!/usr/bin/env python3
"""Wrapper for the ffmpeg-keyframe-extraction skill.

Extracts I-frames (keyframes) with the two methods the SKILL.md documents:
  - select (Method 1): ffmpeg -i in -vf "select='eq(pict_type,I)'" -vsync vfr out_%03d.ext
  - skip   (Method 2): ffmpeg -skip_frame nokey -i in -vsync vfr out_%03d.ext
plus the documented options: -q:v <n> (JPEG quality) and -frame_pts 1 (timestamp filenames).
ffmpeg is expected on PATH in the benchmark image.
"""
import sys, os, json, glob, subprocess


def clean(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    return "" if v.startswith("{") and v.endswith("}") else v


def emit(d):
    print(json.dumps(d))
    sys.exit(0 if d.get("ok") else 1)


def main():
    a = [clean(x) for x in sys.argv[1:]]
    if len(a) < 2:
        emit({"ok": False, "error": "usage: keyframes.py <input> <out_pattern> [method] [quality] [frame_pts]"})
    inp, pattern = a[0], a[1]
    method = (a[2] if len(a) > 2 and a[2] else "select").lower()
    quality = a[3] if len(a) > 3 and a[3] else ""
    frame_pts = a[4] if len(a) > 4 and a[4] else ""
    if not inp or not os.path.exists(inp):
        emit({"ok": False, "error": f"input not found: {inp!r}"})
    outdir = os.path.dirname(pattern)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    if method == "skip":
        cmd = ["ffmpeg", "-y", "-skip_frame", "nokey", "-i", inp, "-vsync", "vfr"]
    else:  # select (default, more filtering control)
        cmd = ["ffmpeg", "-y", "-i", inp, "-vf", "select='eq(pict_type,I)'", "-vsync", "vfr"]
    if quality:
        cmd += ["-q:v", quality]
    if frame_pts.lower() in ("1", "true", "yes"):
        cmd += ["-frame_pts", "1"]
    cmd.append(pattern)

    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        emit({"ok": False, "error": "ffmpeg not found on PATH. Install ffmpeg (apt install ffmpeg / conda install -c conda-forge ffmpeg)."})
    if p.returncode != 0:
        emit({"ok": False, "error": (p.stderr or "ffmpeg failed").strip()[-800:]})

    # count produced frames (glob the pattern's directory + extension)
    ext = os.path.splitext(pattern)[1]
    produced = sorted(glob.glob(os.path.join(outdir or ".", "*" + ext)))
    emit({"ok": True, "method": method, "pattern": pattern, "count": len(produced)})


if __name__ == "__main__":
    main()
