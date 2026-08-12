#!/usr/bin/env python3
"""Thin wrapper for the bundled recalc.py.

Normalizes the optional timeout arg (String passes an empty string / literal
placeholder when it is omitted) and invokes the byte-identical recalc.py so the
agent gets `python recalc.py <file> [timeout]` behavior without crashing on int('').
"""
import json
import os
import subprocess
import sys


def clean(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    if v.startswith("{") and v.endswith("}"):
        return ""
    return v


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    recalc = os.path.join(os.path.dirname(here), "recalc.py")

    excel_file = clean(sys.argv[1] if len(sys.argv) > 1 else "")
    timeout = clean(sys.argv[2] if len(sys.argv) > 2 else "")

    if not excel_file:
        print(json.dumps({"error": "Missing excel_file. Usage: /act.recalc --excel_file PATH [--timeout_seconds N]"}))
        sys.exit(1)

    cmd = [sys.executable, recalc, excel_file]
    if timeout:
        if not timeout.isdigit():
            print(json.dumps({"error": f"timeout_seconds must be an integer (got {timeout!r})"}))
            sys.exit(1)
        cmd.append(timeout)

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout:
        sys.stdout.write(r.stdout)
    if r.returncode != 0 and not r.stdout:
        sys.stderr.write(r.stderr)
        print(json.dumps({"error": "recalc.py failed. Ensure LibreOffice (soffice) is installed and the file is a valid .xlsx."}))
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
