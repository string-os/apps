#!/usr/bin/env python3
"""Wrapper for the ffmpeg-audio-processing skill.

Each subcommand runs an audio operation the SKILL.md documents: extract, normalize,
volume, channels, mix, delay, resample, filter, analyze, concat. ffmpeg/ffprobe are
expected on PATH in the benchmark image.
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


def run(args, capture=False):
    try:
        p = subprocess.run(args, capture_output=True, text=True)
    except FileNotFoundError:
        emit({"ok": False, "error": "ffmpeg/ffprobe not found on PATH. Install ffmpeg (apt install ffmpeg / conda install -c conda-forge ffmpeg)."})
    if p.returncode != 0:
        emit({"ok": False, "error": (p.stderr or "ffmpeg failed").strip()[-1200:]})
    return p


def need(inp):
    if not inp or not os.path.exists(inp):
        emit({"ok": False, "error": f"input not found: {inp!r}"})


def main():
    if len(sys.argv) < 2:
        emit({"ok": False, "error": "usage: audio.py <op> ..."})
    op = sys.argv[1]
    a = [clean(x) for x in sys.argv[2:]]

    if op == "extract":
        # input output [format: mp3|aac|wav]  -> -vn, codec per format
        if len(a) < 2:
            emit({"ok": False, "error": "usage: audio.py extract <input> <output> [format]"})
        inp, out = a[0], a[1]
        fmt = (a[2] if len(a) > 2 and a[2] else "").lower()
        need(inp)
        cmd = ["ffmpeg", "-y", "-i", inp, "-vn"]
        if fmt == "mp3":
            cmd += ["-acodec", "libmp3lame", "-q:a", "2"]
        elif fmt == "aac":
            cmd += ["-c:a", "copy"]
        elif fmt == "wav":
            cmd += ["-acodec", "pcm_s16le"]
        # else: let ffmpeg infer from extension
        cmd.append(out)
        run(cmd)
        emit({"ok": True, "op": "extract", "output": out})

    elif op == "normalize":
        # input output [mode: loudnorm|volume] [value]
        if len(a) < 2:
            emit({"ok": False, "error": "usage: audio.py normalize <input> <output> [loudnorm|volume] [value]"})
        inp, out = a[0], a[1]
        mode = (a[2] if len(a) > 2 and a[2] else "loudnorm").lower()
        val = a[3] if len(a) > 3 and a[3] else ""
        need(inp)
        if mode == "loudnorm":
            # ITU-R BS.1770-4: I=-23 TP=-1.5 LRA=11 (val overrides I if given)
            target = val or "-23"
            af = f"loudnorm=I={target}:TP=-1.5:LRA=11"
        else:
            af = f"volume={val or '2.0'}"
        run(["ffmpeg", "-y", "-i", inp, "-af", af, out])
        emit({"ok": True, "op": "normalize", "filter": af, "output": out})

    elif op == "volume":
        # input output value (e.g. 6dB, -3dB, 0.5)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: audio.py volume <input> <output> <value>"})
        inp, out, val = a[0], a[1], a[2]
        need(inp)
        run(["ffmpeg", "-y", "-i", inp, "-af", f"volume={val}", out])
        emit({"ok": True, "op": "volume", "filter": f"volume={val}", "output": out})

    elif op == "channels":
        # input output mode (left|right|mono|stereo)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: audio.py channels <input> <output> <left|right|mono|stereo>"})
        inp, out, mode = a[0], a[1], a[2].lower()
        need(inp)
        if mode == "left":
            cmd = ["ffmpeg", "-y", "-i", inp, "-map_channel", "0.0.0", out]
        elif mode == "right":
            cmd = ["ffmpeg", "-y", "-i", inp, "-map_channel", "0.0.1", out]
        elif mode == "mono":
            cmd = ["ffmpeg", "-y", "-i", inp, "-ac", "1", out]
        elif mode == "stereo":
            cmd = ["ffmpeg", "-y", "-i", inp, "-ac", "2", out]
        else:
            emit({"ok": False, "error": "channels mode must be left, right, mono, or stereo"})
        run(cmd)
        emit({"ok": True, "op": "channels", "mode": mode, "output": out})

    elif op == "mix":
        # video audio output [voice_vol] [music_vol]
        # replace track if no vols; amix with per-input volume if given
        if len(a) < 3:
            emit({"ok": False, "error": "usage: audio.py mix <video> <audio> <output> [voice_vol] [music_vol]"})
        vid, aud, out = a[0], a[1], a[2]
        vvol = a[3] if len(a) > 3 and a[3] else ""
        mvol = a[4] if len(a) > 4 and a[4] else ""
        need(vid); need(aud)
        if not vvol and not mvol:
            # replace the audio track entirely
            cmd = ["ffmpeg", "-y", "-i", vid, "-i", aud, "-c:v", "copy",
                   "-map", "0:v:0", "-map", "1:a:0", out]
        else:
            vv = vvol or "1.0"
            mv = mvol or "0.3"
            fc = (f"[0:a]volume={vv}[voice];[1:a]volume={mv}[music];"
                  f"[voice][music]amix=inputs=2:duration=first")
            cmd = ["ffmpeg", "-y", "-i", vid, "-i", aud, "-filter_complex", fc,
                   "-c:v", "copy", out]
        run(cmd)
        emit({"ok": True, "op": "mix", "output": out})

    elif op == "delay":
        # input output milliseconds  -> adelay=ms|ms
        if len(a) < 3:
            emit({"ok": False, "error": "usage: audio.py delay <input> <output> <milliseconds>"})
        inp, out, ms = a[0], a[1], a[2]
        need(inp)
        run(["ffmpeg", "-y", "-i", inp, "-af", f"adelay={ms}|{ms}", out])
        emit({"ok": True, "op": "delay", "ms": ms, "output": out})

    elif op == "resample":
        # input output rate(Hz)
        if len(a) < 3:
            emit({"ok": False, "error": "usage: audio.py resample <input> <output> <rate_hz>"})
        inp, out, rate = a[0], a[1], a[2]
        need(inp)
        run(["ffmpeg", "-y", "-i", inp, "-af", f"aresample={rate}", "-ar", rate, out])
        emit({"ok": True, "op": "resample", "rate": rate, "output": out})

    elif op == "filter":
        # input output kind freq [width]
        # kind: highpass | lowpass | bandpass | fadeinout
        if len(a) < 3:
            emit({"ok": False, "error": "usage: audio.py filter <input> <output> <highpass|lowpass|bandpass|fadeinout> [freq] [width/dur]"})
        inp, out, kind = a[0], a[1], a[2].lower()
        p1 = a[3] if len(a) > 3 and a[3] else ""
        p2 = a[4] if len(a) > 4 and a[4] else ""
        need(inp)
        if kind == "highpass":
            af = f"highpass=f={p1 or '200'}"
        elif kind == "lowpass":
            af = f"lowpass=f={p1 or '3000'}"
        elif kind == "bandpass":
            af = f"bandpass=f={p1 or '1000'}:width_type=h:w={p2 or '500'}"
        elif kind == "fadeinout":
            # afade in at 0 + out: p1=out_start, p2=dur
            d = p2 or "2"
            af = f"afade=t=in:st=0:d={d},afade=t=out:st={p1 or '8'}:d={d}"
        else:
            emit({"ok": False, "error": "filter kind must be highpass, lowpass, bandpass, or fadeinout"})
        run(["ffmpeg", "-y", "-i", inp, "-af", af, out])
        emit({"ok": True, "op": "filter", "filter": af, "output": out})

    elif op == "analyze":
        # input [mode: volumedetect|ebur128|stats]
        if len(a) < 1:
            emit({"ok": False, "error": "usage: audio.py analyze <input> [volumedetect|ebur128|stats]"})
        inp = a[0]
        mode = (a[1] if len(a) > 1 and a[1] else "volumedetect").lower()
        need(inp)
        if mode == "stats":
            p = run(["ffprobe", "-v", "error", "-select_streams", "a:0",
                     "-show_entries", "stream=sample_rate,channels,bit_rate",
                     "-of", "json", inp])
            emit({"ok": True, "op": "analyze", "mode": "stats", "stats": json.loads(p.stdout)})
        af = "ebur128=peak=true" if mode == "ebur128" else "volumedetect"
        p = run(["ffmpeg", "-i", inp, "-af", af, "-f", "null", "-"])
        # measurements are on stderr
        emit({"ok": True, "op": "analyze", "mode": mode, "measurement": (p.stderr or "").strip()[-3000:]})

    elif op == "concat":
        # inputs(quoted space-separated) output
        if len(a) < 2:
            emit({"ok": False, "error": "usage: audio.py concat <\"a.mp3 b.mp3 ...\"> <output>"})
        inputs = [x for x in a[0].split() if x.strip()]
        out = a[1]
        if len(inputs) < 2:
            emit({"ok": False, "error": "concat needs >= 2 input files in one quoted string"})
        for f in inputs:
            if not os.path.exists(f):
                emit({"ok": False, "error": f"input not found: {f!r}"})
        fd, listpath = tempfile.mkstemp(suffix=".txt", text=True)
        with os.fdopen(fd, "w") as fh:
            for f in inputs:
                fh.write("file '%s'\n" % os.path.abspath(f).replace("'", "'\\''"))
        try:
            run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listpath, "-c", "copy", out])
        finally:
            os.unlink(listpath)
        emit({"ok": True, "op": "concat", "output": out, "inputs": inputs})
    else:
        emit({"ok": False, "error": f"unknown op: {op}"})


if __name__ == "__main__":
    main()
