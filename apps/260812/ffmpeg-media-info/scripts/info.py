#!/usr/bin/env python3
"""Wrapper for the ffmpeg-media-info skill.

Each subcommand runs exactly the ffprobe command the SKILL.md documents and
returns its output as JSON {"ok":true,"<field>":...} or {"ok":false,"error":...}.
ffprobe/ffmpeg are expected on PATH in the benchmark image.
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
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    if len(sys.argv) < 3:
        emit({"ok": False, "error": "usage: info.py <op> <input> [stream]"})
    op = sys.argv[1]
    inp = clean(sys.argv[2])
    stream = clean(sys.argv[3]) if len(sys.argv) > 3 else ""
    if not inp or not os.path.exists(inp):
        emit({"ok": False, "error": f"input not found: {inp!r}"})

    # ffprobe -v error base
    base = ["ffprobe", "-v", "error"]
    try:
        if op == "info":
            # ffprobe -v quiet -print_format json -show_format -show_streams input
            rc, out, err = run(["ffprobe", "-v", "quiet", "-print_format", "json",
                                "-show_format", "-show_streams", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "info": json.loads(out)})
        elif op == "duration":
            rc, out, err = run(base + ["-show_entries", "format=duration",
                                       "-of", "default=noprint_wrappers=1:nokey=1", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "duration": out.strip()})
        elif op == "resolution":
            rc, out, err = run(base + ["-select_streams", "v:0", "-show_entries",
                                       "stream=width,height", "-of", "csv=s=x:p=0", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "resolution": out.strip()})
        elif op == "bitrate":
            sel = stream or "format"
            if sel == "video":
                rc, out, err = run(base + ["-select_streams", "v:0", "-show_entries",
                                           "stream=bit_rate", "-of",
                                           "default=noprint_wrappers=1:nokey=1", inp])
            else:
                rc, out, err = run(base + ["-show_entries", "format=bit_rate", "-of",
                                           "default=noprint_wrappers=1:nokey=1", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "bitrate": out.strip()})
        elif op == "codec":
            sel = "a:0" if stream == "audio" else "v:0"
            rc, out, err = run(base + ["-select_streams", sel, "-show_entries",
                                       "stream=codec_name,codec_long_name", "-of",
                                       "default=noprint_wrappers=1", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "codec": out.strip()})
        elif op == "sample_rate":
            rc, out, err = run(base + ["-select_streams", "a:0", "-show_entries",
                                       "stream=sample_rate", "-of",
                                       "default=noprint_wrappers=1:nokey=1", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "sample_rate": out.strip()})
        elif op == "channels":
            rc, out, err = run(base + ["-select_streams", "a:0", "-show_entries",
                                       "stream=channels", "-of",
                                       "default=noprint_wrappers=1:nokey=1", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "channels": out.strip()})
        elif op == "framerate":
            rc, out, err = run(base + ["-select_streams", "v:0", "-show_entries",
                                       "stream=r_frame_rate", "-of",
                                       "default=noprint_wrappers=1:nokey=1", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            emit({"ok": True, "framerate": out.strip()})
        elif op == "stream_count":
            sel = "a" if stream == "audio" else "v"
            rc, out, err = run(base + ["-select_streams", sel, "-show_entries",
                                       "stream=index", "-of", "csv=p=0", inp])
            if rc != 0:
                emit({"ok": False, "error": err.strip() or "ffprobe failed"})
            count = len([x for x in out.splitlines() if x.strip()])
            emit({"ok": True, "stream_count": count, "type": sel})
        else:
            emit({"ok": False, "error": f"unknown op: {op}"})
    except FileNotFoundError:
        emit({"ok": False, "error": "ffprobe not found on PATH. Install ffmpeg (apt install ffmpeg / conda install -c conda-forge ffmpeg)."})
    except json.JSONDecodeError as e:
        emit({"ok": False, "error": f"could not parse ffprobe JSON: {e}"})


if __name__ == "__main__":
    main()
