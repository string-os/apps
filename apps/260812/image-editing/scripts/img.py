#!/usr/bin/env python3
"""Wrapper for the image-editing skill (ImageMagick `convert`).

Each subcommand runs the `convert` operation the SKILL.md documents:
  resize, format, auto_orient, blur, border, brightness_contrast, blue_shift, contrast.
These map 1:1 to the operators the guide lists (-resize, -format, -auto-orient, -blur,
-border/-bordercolor, -brightness-contrast, -blue-shift, -contrast).
`convert` (ImageMagick) is expected on PATH in the benchmark image.
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
        emit({"ok": False, "error": "convert (ImageMagick) not found on PATH. Install it (apt install imagemagick / conda install -c conda-forge imagemagick)."})
    if p.returncode != 0:
        emit({"ok": False, "error": (p.stderr or "convert failed").strip()[-800:]})


def need(inp):
    if not inp or not os.path.exists(inp):
        emit({"ok": False, "error": f"input not found: {inp!r}"})


def main():
    if len(sys.argv) < 2:
        emit({"ok": False, "error": "usage: img.py <op> ..."})
    op = sys.argv[1]
    a = [clean(x) for x in sys.argv[2:]]

    if op == "resize":
        # input output geometry (e.g. 50%, 256x256)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: img.py resize <input> <output> <geometry>"})
        inp, out, geom = a[0], a[1], a[2]
        need(inp)
        run(["convert", inp, "-resize", geom, out])
        emit({"ok": True, "op": "resize", "geometry": geom, "output": out})

    elif op == "format":
        # input output  (target format = output extension; uses -format/implicit convert)
        if len(a) < 2:
            emit({"ok": False, "error": "usage: img.py format <input> <output>"})
        inp, out = a[0], a[1]
        need(inp)
        run(["convert", inp, out])
        emit({"ok": True, "op": "format", "output": out})

    elif op == "auto_orient":
        if len(a) < 2:
            emit({"ok": False, "error": "usage: img.py auto_orient <input> <output>"})
        inp, out = a[0], a[1]
        need(inp)
        run(["convert", inp, "-auto-orient", out])
        emit({"ok": True, "op": "auto_orient", "output": out})

    elif op == "blur":
        # input output radius_sigma (e.g. 0x8)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: img.py blur <input> <output> <radiusxsigma>"})
        inp, out, rs = a[0], a[1], a[2]
        need(inp)
        run(["convert", inp, "-blur", rs, out])
        emit({"ok": True, "op": "blur", "blur": rs, "output": out})

    elif op == "border":
        # input output value [color]   (value% per the skill; color via -bordercolor)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: img.py border <input> <output> <value> [color]"})
        inp, out, val = a[0], a[1], a[2]
        color = a[3] if len(a) > 3 and a[3] else ""
        need(inp)
        cmd = ["convert", inp]
        if color:
            cmd += ["-bordercolor", color]
        cmd += ["-border", val, out]
        run(cmd)
        emit({"ok": True, "op": "border", "border": val, "color": color, "output": out})

    elif op == "brightness_contrast":
        # input output brightness [contrast]  (-100..+100 each)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: img.py brightness_contrast <input> <output> <brightness> [contrast]"})
        inp, out, b = a[0], a[1], a[2]
        c = a[3] if len(a) > 3 and a[3] else ""
        need(inp)
        spec = b if not c else f"{b}x{c}"
        run(["convert", inp, "-brightness-contrast", spec, out])
        emit({"ok": True, "op": "brightness_contrast", "spec": spec, "output": out})

    elif op == "blue_shift":
        # input output [factor=1.5]
        if len(a) < 2:
            emit({"ok": False, "error": "usage: img.py blue_shift <input> <output> [factor]"})
        inp, out = a[0], a[1]
        factor = a[2] if len(a) > 2 and a[2] else "1.5"
        need(inp)
        run(["convert", inp, "-blue-shift", factor, out])
        emit({"ok": True, "op": "blue_shift", "factor": factor, "output": out})

    elif op == "contrast":
        # input output [direction: up|down]  (-contrast enhances, +contrast reduces)
        if len(a) < 2:
            emit({"ok": False, "error": "usage: img.py contrast <input> <output> [up|down]"})
        inp, out = a[0], a[1]
        direction = (a[2] if len(a) > 2 and a[2] else "up").lower()
        need(inp)
        op_flag = "+contrast" if direction == "down" else "-contrast"
        run(["convert", inp, op_flag, out])
        emit({"ok": True, "op": "contrast", "direction": direction, "output": out})
    else:
        emit({"ok": False, "error": f"unknown op: {op}"})


if __name__ == "__main__":
    main()
