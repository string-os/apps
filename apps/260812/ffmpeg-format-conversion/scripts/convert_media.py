#!/usr/bin/env python3
"""Wrapper for the ffmpeg-format-conversion skill.

Runs the format/codec conversion commands the SKILL.md documents:
  - convert: re-encode to a target container, optionally choosing video/audio
    codec, CRF, bitrate, and x264/x265 preset (the skill's codec + quality knobs).
  - copy:    stream-copy into a new container with -c copy (fast, no re-encode).
ffmpeg is expected on PATH in the benchmark image.
"""
import sys, os, json, subprocess


def clean(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    return "" if v.startswith("{") and v.endswith("}") else v


def emit(d):
    print(json.dumps(d))
    sys.exit(0 if d.get("ok") else 1)


def run(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True)
    except FileNotFoundError:
        emit({"ok": False, "error": "ffmpeg not found on PATH. Install ffmpeg (apt install ffmpeg / conda install -c conda-forge ffmpeg)."})
    if p.returncode != 0:
        emit({"ok": False, "error": (p.stderr or "ffmpeg failed").strip()[-800:]})


def main():
    if len(sys.argv) < 2:
        emit({"ok": False, "error": "usage: convert_media.py <convert|copy> ..."})
    op = sys.argv[1]
    if op == "copy":
        # ffmpeg -i input -c copy output
        if len(sys.argv) < 4:
            emit({"ok": False, "error": "usage: convert_media.py copy <input> <output>"})
        inp, out = clean(sys.argv[2]), clean(sys.argv[3])
        if not inp or not os.path.exists(inp):
            emit({"ok": False, "error": f"input not found: {inp!r}"})
        run(["ffmpeg", "-y", "-i", inp, "-c", "copy", out])
        emit({"ok": True, "op": "copy", "output": out})
    elif op == "convert":
        # ffmpeg -i input [-c:v VC] [-c:a AC] [-crf N] [-preset P] [-b:v BV] [-b:a BA] output
        if len(sys.argv) < 4:
            emit({"ok": False, "error": "usage: convert_media.py convert <input> <output> [vcodec] [acodec] [crf] [preset] [vbitrate] [abitrate]"})
        args = [clean(x) for x in sys.argv[2:]]
        inp = args[0]
        out = args[1]
        vcodec = args[2] if len(args) > 2 else ""
        acodec = args[3] if len(args) > 3 else ""
        crf = args[4] if len(args) > 4 else ""
        preset = args[5] if len(args) > 5 else ""
        vbitrate = args[6] if len(args) > 6 else ""
        abitrate = args[7] if len(args) > 7 else ""
        if not inp or not os.path.exists(inp):
            emit({"ok": False, "error": f"input not found: {inp!r}"})
        cmd = ["ffmpeg", "-y", "-i", inp]
        if vcodec:
            cmd += ["-c:v", vcodec]
        if acodec:
            cmd += ["-c:a", acodec]
        if crf:
            cmd += ["-crf", crf]
        if preset:
            cmd += ["-preset", preset]
        if vbitrate:
            cmd += ["-b:v", vbitrate]
        if abitrate:
            cmd += ["-b:a", abitrate]
        cmd.append(out)
        run(cmd)
        emit({"ok": True, "op": "convert", "output": out,
              "vcodec": vcodec, "acodec": acodec, "crf": crf, "preset": preset})
    else:
        emit({"ok": False, "error": f"unknown op: {op}"})


if __name__ == "__main__":
    main()
