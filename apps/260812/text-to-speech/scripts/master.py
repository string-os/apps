#!/usr/bin/env python3
"""Wrapper for the text-to-speech (TTS Audio Mastering) skill.

The skill ships no TTS engine command — engine choice is a decision the agent makes.
What it DOES document are concrete FFmpeg mastering steps, exposed here as actions:
  - cleanup:   high-pass ~20Hz (+ optional low-pass ~16kHz) + short boundary fades
  - measure:   ITU-R BS.1770 loudness via ebur128
  - normalize: loudnorm I=-23 TP=-1.5 LRA=11 (final step)
  - pad:       pad a segment with trailing silence to match a target window
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
        emit({"ok": False, "error": (p.stderr or "ffmpeg failed").strip()[-1200:]})
    return p


def need(inp):
    if not inp or not os.path.exists(inp):
        emit({"ok": False, "error": f"input not found: {inp!r}"})


def main():
    if len(sys.argv) < 2:
        emit({"ok": False, "error": "usage: master.py <cleanup|measure|normalize|pad> ..."})
    op = sys.argv[1]
    a = [clean(x) for x in sys.argv[2:]]

    if op == "cleanup":
        # input output [hp_hz=20] [lp_hz(optional)] [fade_ms=50]
        if len(a) < 2:
            emit({"ok": False, "error": "usage: master.py cleanup <input> <output> [hp_hz] [lp_hz] [fade_ms]"})
        inp, out = a[0], a[1]
        hp = a[2] if len(a) > 2 and a[2] else "20"
        lp = a[3] if len(a) > 3 and a[3] else ""
        fade_ms = a[4] if len(a) > 4 and a[4] else "50"
        need(inp)
        # duration to place the out-fade at end-(fade)
        p = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", inp])
        try:
            dur = float((p.stdout or "0").strip())
        except ValueError:
            dur = 0.0
        d = max(float(fade_ms) / 1000.0, 0.0)
        chain = [f"highpass=f={hp}"]
        if lp:
            chain.append(f"lowpass=f={lp}")
        chain.append(f"afade=t=in:st=0:d={d}")
        out_st = max(dur - d, 0.0)
        chain.append(f"afade=t=out:st={out_st:.3f}:d={d}")
        af = ",".join(chain)
        run(["ffmpeg", "-y", "-i", inp, "-af", af, out])
        emit({"ok": True, "op": "cleanup", "filter": af, "output": out})

    elif op == "measure":
        # input  -> ebur128 loudness measurement (stderr)
        if len(a) < 1:
            emit({"ok": False, "error": "usage: master.py measure <input>"})
        inp = a[0]
        need(inp)
        p = run(["ffmpeg", "-i", inp, "-af", "ebur128=peak=true", "-f", "null", "-"])
        emit({"ok": True, "op": "measure", "measurement": (p.stderr or "").strip()[-3000:]})

    elif op == "normalize":
        # input output [target_I=-23]
        if len(a) < 2:
            emit({"ok": False, "error": "usage: master.py normalize <input> <output> [target_I]"})
        inp, out = a[0], a[1]
        ti = a[2] if len(a) > 2 and a[2] else "-23"
        need(inp)
        af = f"loudnorm=I={ti}:TP=-1.5:LRA=11"
        run(["ffmpeg", "-y", "-i", inp, "-af", af, out])
        emit({"ok": True, "op": "normalize", "filter": af, "output": out})

    elif op == "pad":
        # input output target_seconds  -> pad trailing silence to reach the window
        if len(a) < 3:
            emit({"ok": False, "error": "usage: master.py pad <input> <output> <target_seconds>"})
        inp, out, target = a[0], a[1], a[2]
        need(inp)
        try:
            tgt = float(target)
        except ValueError:
            emit({"ok": False, "error": f"bad target_seconds: {target!r}"})
        # apad to whole_dur=target pads the END with silence to reach target length
        af = f"apad=whole_dur={tgt}"
        run(["ffmpeg", "-y", "-i", inp, "-af", af, out])
        emit({"ok": True, "op": "pad", "target_seconds": tgt, "output": out})
    else:
        emit({"ok": False, "error": f"unknown op: {op}"})


if __name__ == "__main__":
    main()
