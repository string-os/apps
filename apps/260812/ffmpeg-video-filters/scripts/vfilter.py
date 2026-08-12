#!/usr/bin/env python3
"""Wrapper for the ffmpeg-video-filters skill.

Each subcommand applies one of the filters the SKILL.md documents:
  scale, crop, watermark (overlay), speed (setpts+atempo), blur (boxblur/gblur),
  eq (brightness/contrast/saturation), rotate (transpose), fade.
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


def vf(inp, out, filt, extra=None):
    cmd = ["ffmpeg", "-y", "-i", inp, "-vf", filt]
    if extra:
        cmd += extra
    cmd.append(out)
    run(cmd)


def main():
    if len(sys.argv) < 4:
        emit({"ok": False, "error": "usage: vfilter.py <op> <input> <output> ..."})
    op = sys.argv[1]
    args = [clean(x) for x in sys.argv[2:]]
    inp, out = args[0], args[1]
    rest = args[2:]
    if not inp or not os.path.exists(inp):
        emit({"ok": False, "error": f"input not found: {inp!r}"})

    if op == "scale":
        # width height [flags]   (use -2 to keep aspect ratio)
        w = rest[0] if len(rest) > 0 and rest[0] else "-2"
        h = rest[1] if len(rest) > 1 and rest[1] else "-2"
        flags = rest[2] if len(rest) > 2 else ""
        filt = f"scale={w}:{h}"
        if flags:
            filt += f":flags={flags}"
        vf(inp, out, filt)
        emit({"ok": True, "op": "scale", "filter": filt, "output": out})

    elif op == "crop":
        # width height [x] [y]
        if len(rest) < 2:
            emit({"ok": False, "error": "crop needs width and height"})
        w, h = rest[0], rest[1]
        x = rest[2] if len(rest) > 2 else ""
        y = rest[3] if len(rest) > 3 else ""
        filt = f"crop={w}:{h}"
        if x and y:
            filt += f":{x}:{y}"
        vf(inp, out, filt)
        emit({"ok": True, "op": "crop", "filter": filt, "output": out})

    elif op == "watermark":
        # overlay_image position
        if len(rest) < 1:
            emit({"ok": False, "error": "watermark needs an overlay image path"})
        logo = rest[0]
        pos = rest[1] if len(rest) > 1 and rest[1] else "10:10"
        if not os.path.exists(logo):
            emit({"ok": False, "error": f"overlay image not found: {logo!r}"})
        cmd = ["ffmpeg", "-y", "-i", inp, "-i", logo,
               "-filter_complex", f"overlay={pos}", out]
        run(cmd)
        emit({"ok": True, "op": "watermark", "overlay": logo, "position": pos, "output": out})

    elif op == "speed":
        # factor  (>1 faster, <1 slower); applies setpts + atempo, or -an if no audio
        if len(rest) < 1 or not rest[0]:
            emit({"ok": False, "error": "speed needs a factor, e.g. 2.0"})
        try:
            factor = float(rest[0])
        except ValueError:
            emit({"ok": False, "error": f"bad speed factor: {rest[0]!r}"})
        pts = 1.0 / factor
        drop_audio = rest[1].lower() in ("1", "true", "yes", "noaudio") if len(rest) > 1 and rest[1] else False
        if drop_audio:
            cmd = ["ffmpeg", "-y", "-i", inp, "-vf", f"setpts={pts}*PTS", "-an", out]
        else:
            cmd = ["ffmpeg", "-y", "-i", inp, "-vf", f"setpts={pts}*PTS",
                   "-af", f"atempo={factor}", out]
        run(cmd)
        emit({"ok": True, "op": "speed", "factor": factor, "output": out})

    elif op == "blur":
        # kind(box|gaussian) param  (box: "10:5" luma_radius:luma_power; gaussian: sigma)
        kind = rest[0] if len(rest) > 0 and rest[0] else "box"
        param = rest[1] if len(rest) > 1 and rest[1] else ("10:5" if kind == "box" else "5")
        if kind == "gaussian":
            filt = f"gblur=sigma={param}"
        else:
            filt = f"boxblur={param}"
        vf(inp, out, filt)
        emit({"ok": True, "op": "blur", "filter": filt, "output": out})

    elif op == "eq":
        # brightness contrast saturation  (any may be empty)
        b = rest[0] if len(rest) > 0 else ""
        c = rest[1] if len(rest) > 1 else ""
        s = rest[2] if len(rest) > 2 else ""
        parts = []
        if b:
            parts.append(f"brightness={b}")
        if c:
            parts.append(f"contrast={c}")
        if s:
            parts.append(f"saturation={s}")
        if not parts:
            emit({"ok": False, "error": "eq needs at least one of brightness/contrast/saturation"})
        filt = "eq=" + ":".join(parts)
        vf(inp, out, filt)
        emit({"ok": True, "op": "eq", "filter": filt, "output": out})

    elif op == "rotate":
        # degrees: 90cw, 90ccw, 180
        d = (rest[0] if len(rest) > 0 else "").lower()
        mapping = {
            "90cw": "transpose=1", "90": "transpose=1",
            "90ccw": "transpose=2", "-90": "transpose=2",
            "180": "transpose=1,transpose=1",
        }
        if d not in mapping:
            emit({"ok": False, "error": "rotate degrees must be one of: 90cw, 90ccw, 180"})
        filt = mapping[d]
        vf(inp, out, filt)
        emit({"ok": True, "op": "rotate", "filter": filt, "output": out})

    elif op == "fade":
        # type(in|out|both) start duration  (for 'both', start/duration are the OUT params; IN is st=0)
        ftype = rest[0] if len(rest) > 0 and rest[0] else "in"
        start = rest[1] if len(rest) > 1 and rest[1] else "0"
        dur = rest[2] if len(rest) > 2 and rest[2] else "2"
        if ftype == "both":
            filt = f"fade=t=in:st=0:d={dur},fade=t=out:st={start}:d={dur}"
        elif ftype in ("in", "out"):
            filt = f"fade=t={ftype}:st={start}:d={dur}"
        else:
            emit({"ok": False, "error": "fade type must be in, out, or both"})
        vf(inp, out, filt)
        emit({"ok": True, "op": "fade", "filter": filt, "output": out})
    else:
        emit({"ok": False, "error": f"unknown op: {op}"})


if __name__ == "__main__":
    main()
