#!/usr/bin/env python3
"""Wrapper for the ffmpeg-video-editing skill.

Runs the cut / concatenate / split commands the SKILL.md documents:
  - cut:    ffmpeg -ss START [-to END | -t DURATION] -i input (-c copy | -c:v libx264 -c:a aac) output
  - concat: file-list method (the skill's recommended Method 1):
            ffmpeg -f concat -safe 0 -i list.txt (-c copy | re-encode) output
  - split:  ffmpeg -i input -c copy -f segment -segment_time N -reset_timestamps 1 out_%03d.ext
ffmpeg is expected on PATH in the benchmark image.
"""
import sys, os, json, tempfile, subprocess


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
        emit({"ok": False, "error": "usage: edit.py <cut|concat|split> ..."})
    op = sys.argv[1]
    args = [clean(x) for x in sys.argv[2:]]

    if op == "cut":
        # input output start [end] [duration] [reencode]
        if len(args) < 3:
            emit({"ok": False, "error": "usage: edit.py cut <input> <output> <start> [end] [duration] [reencode]"})
        inp, out, start = args[0], args[1], args[2]
        end = args[3] if len(args) > 3 else ""
        dur = args[4] if len(args) > 4 else ""
        reencode = args[5] if len(args) > 5 else ""
        if not inp or not os.path.exists(inp):
            emit({"ok": False, "error": f"input not found: {inp!r}"})
        cmd = ["ffmpeg", "-y", "-ss", start]
        if end:
            cmd += ["-to", end]
        cmd += ["-i", inp]
        if dur:
            cmd += ["-t", dur]
        if reencode.lower() in ("1", "true", "yes", "reencode"):
            cmd += ["-c:v", "libx264", "-c:a", "aac"]
        else:
            cmd += ["-c", "copy"]
        cmd.append(out)
        run(cmd)
        emit({"ok": True, "op": "cut", "output": out})

    elif op == "concat":
        # inputs(space-separated, quoted) output [reencode]
        if len(args) < 2:
            emit({"ok": False, "error": "usage: edit.py concat <\"in1.mp4 in2.mp4 ...\"> <output> [reencode]"})
        inputs = [p for p in args[0].split() if p.strip()]
        out = args[1]
        reencode = args[2] if len(args) > 2 else ""
        if len(inputs) < 2:
            emit({"ok": False, "error": "concat needs >= 2 input files in one quoted, space-separated string"})
        for f in inputs:
            if not os.path.exists(f):
                emit({"ok": False, "error": f"input not found: {f!r}"})
        # build the list.txt the skill's recommended method uses
        fd, listpath = tempfile.mkstemp(suffix=".txt", text=True)
        with os.fdopen(fd, "w") as fh:
            for f in inputs:
                fh.write("file '%s'\n" % os.path.abspath(f).replace("'", "'\\''"))
        try:
            cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listpath]
            if reencode.lower() in ("1", "true", "yes", "reencode"):
                cmd += ["-c:v", "libx264", "-c:a", "aac"]
            else:
                cmd += ["-c", "copy"]
            cmd.append(out)
            run(cmd)
        finally:
            os.unlink(listpath)
        emit({"ok": True, "op": "concat", "output": out, "inputs": inputs})

    elif op == "split":
        # input out_pattern segment_time
        if len(args) < 3:
            emit({"ok": False, "error": "usage: edit.py split <input> <out_pattern> <segment_seconds>"})
        inp, pattern, seg = args[0], args[1], args[2]
        if not inp or not os.path.exists(inp):
            emit({"ok": False, "error": f"input not found: {inp!r}"})
        outdir = os.path.dirname(pattern)
        if outdir:
            os.makedirs(outdir, exist_ok=True)
        cmd = ["ffmpeg", "-y", "-i", inp, "-c", "copy", "-f", "segment",
               "-segment_time", seg, "-reset_timestamps", "1", pattern]
        run(cmd)
        emit({"ok": True, "op": "split", "pattern": pattern, "segment_time": seg})
    else:
        emit({"ok": False, "error": f"unknown op: {op}"})


if __name__ == "__main__":
    main()
