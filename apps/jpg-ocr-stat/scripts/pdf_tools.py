#!/usr/bin/env python3
"""PDF helpers built on poppler CLIs (pdftotext / pdftoppm) -> JSON.

  text    PDF -> plain text (stdout-embedded or written to a file)
  images  PDF pages -> image files (for OCR of scanned PDFs)

Poppler ships both binaries; install with `conda install -c conda-forge poppler`.
"""

import argparse
import json
import os
import subprocess
import sys


def have(binary):
    return subprocess.run(["which", binary], capture_output=True).returncode == 0


def cmd_text(args):
    if not have("pdftotext"):
        return {"success": False, "error": "pdftotext not found. "
                "Install: conda install -c conda-forge poppler"}
    out = args.out or "-"
    try:
        r = subprocess.run(["pdftotext", "-layout", args.pdf, out],
                           capture_output=True, text=True)
    except Exception as e:
        return {"success": False, "error": f"pdftotext failed: {e}"}
    if r.returncode != 0:
        return {"success": False, "error": r.stderr.strip() or "pdftotext failed"}
    if out == "-":
        text = r.stdout
        return {"success": True, "pdf": args.pdf, "chars": len(text),
                "text": text[:8000] + ("\n...[truncated]" if len(text) > 8000 else "")}
    return {"success": True, "pdf": args.pdf, "output": out}


def cmd_images(args):
    if not have("pdftoppm"):
        return {"success": False, "error": "pdftoppm not found. "
                "Install: conda install -c conda-forge poppler"}
    os.makedirs(args.outdir, exist_ok=True)
    prefix = os.path.join(args.outdir, "page")
    fmt_flag = {"png": "-png", "jpeg": "-jpeg", "jpg": "-jpeg", "tiff": "-tiff"}.get(args.format, "-png")
    try:
        r = subprocess.run(["pdftoppm", fmt_flag, "-r", str(args.dpi), args.pdf, prefix],
                           capture_output=True, text=True)
    except Exception as e:
        return {"success": False, "error": f"pdftoppm failed: {e}"}
    if r.returncode != 0:
        return {"success": False, "error": r.stderr.strip() or "pdftoppm failed"}
    files = sorted(f for f in os.listdir(args.outdir) if f.startswith("page"))
    return {"success": True, "pdf": args.pdf, "outdir": args.outdir,
            "dpi": args.dpi, "format": args.format, "pages": len(files), "files": files}


def main():
    ap = argparse.ArgumentParser(description="PDF text/image extraction via poppler.")
    sub = ap.add_subparsers(dest="mode", required=True)

    t = sub.add_parser("text", help="Extract text from a PDF")
    t.add_argument("--pdf", required=True)
    t.add_argument("--out", default=None, help="Output .txt path (omit to embed text in JSON)")

    im = sub.add_parser("images", help="Render PDF pages to images")
    im.add_argument("--pdf", required=True)
    im.add_argument("--outdir", required=True)
    im.add_argument("--dpi", type=int, default=200)
    im.add_argument("--format", default="png", choices=["png", "jpeg", "jpg", "tiff"])

    args = ap.parse_args()
    if not os.path.isfile(args.pdf):
        print(json.dumps({"success": False, "error": f"PDF not found: {args.pdf}"}))
        sys.exit(1)
    result = cmd_text(args) if args.mode == "text" else cmd_images(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
