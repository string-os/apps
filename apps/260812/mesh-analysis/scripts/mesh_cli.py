#!/usr/bin/env python3
"""CLI wrapper that exposes the bundled MeshAnalyzer operations as String actions.

mesh_tool.py is the skill's tool, kept verbatim; this just gives it a clean
JSON CLI so the agent calls /act.<op> instead of importing the module.
"""
import sys, os, json, io, contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mesh_tool import MeshAnalyzer


def clean(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    return "" if v.startswith("{") and v.endswith("}") else v


def emit(d):
    print(json.dumps(d))
    sys.exit(0 if d.get("ok") else 1)


def main():
    if len(sys.argv) < 3:
        emit({"ok": False, "error": "usage: mesh_cli.py <analyze|components|volume> <file.stl>"})
    op, stl = sys.argv[1], clean(sys.argv[2])
    if not stl or not os.path.exists(stl):
        emit({"ok": False, "error": f"STL not found: {stl!r}"})
    try:
        # mesh_tool prints a notice to stdout on ASCII fallback; keep stdout clean for JSON
        with contextlib.redirect_stdout(io.StringIO()):
            a = MeshAnalyzer(stl)
        if op == "analyze":
            emit({"ok": True, **a.analyze_largest_component()})
        elif op == "volume":
            emit({"ok": True, "volume": a.get_volume(), "triangles": len(a.triangles)})
        elif op == "components":
            comps = sorted(a.get_components(), key=lambda c: a.get_volume(c), reverse=True)
            rows = [{"index": i, "volume": a.get_volume(c),
                     "material_id": c[0][3] if c else None, "triangles": len(c)}
                    for i, c in enumerate(comps)]
            emit({"ok": True, "total_components": len(comps), "components": rows})
        else:
            emit({"ok": False, "error": f"unknown op {op!r} (analyze|components|volume)"})
    except Exception as e:
        emit({"ok": False, "error": f"{type(e).__name__}: {e}"})


if __name__ == "__main__":
    main()
