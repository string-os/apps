#!/usr/bin/env python3
"""Receipt OCR -> stats xlsx.

Reads every image under --input, OCRs each with Tesseract (multi-pass), pulls the
date and total amount, and writes a single-sheet xlsx ("results") with columns
filename, date, total_amount ordered by filename. Prints a JSON summary to stdout.

This is the core of the jpg-ocr-stat app. Failure on a single field -> null cell,
never a crash, so the whole batch always produces a file.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageOps, ImageFilter
    import pytesseract
    from openpyxl import Workbook
except ImportError as e:
    print(json.dumps({
        "success": False,
        "error": f"Missing dependency: {e.name}. "
                 "Install: conda install -c conda-forge tesseract pytesseract pillow openpyxl",
    }))
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tess import ensure_tessdata  # noqa: E402


def _parse_date_any_format(date_text: str) -> Optional[datetime]:
    n = date_text.strip().replace("O", "0").replace("o", "0")
    n = n.replace("I", "1").replace("l", "1").replace(" ", "")
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y",
                "%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y", "%m-%d-%y",
                "%Y/%m/%d", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(n, fmt)
            if 2000 <= dt.year <= 2030:
                return dt
        except ValueError:
            continue
    return None


def _two_dp(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def _preprocess(img: "Image.Image") -> List["Image.Image"]:
    gray = ImageOps.grayscale(img)
    auto = ImageOps.autocontrast(gray, cutoff=2)
    out = [auto, ImageOps.invert(auto)]
    w, h = gray.size
    if w < 1000 or h < 1000:
        scale = max(1000 / w, 1000 / h, 2)
        scaled = gray.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        out.append(ImageOps.autocontrast(scaled, cutoff=2))
    out.append(auto.filter(ImageFilter.SHARPEN))
    out.append(auto.point(lambda p: 255 if p > 128 else 0))
    out.append(auto.point(lambda p: 255 if p > 100 else 0))
    return out


def _ocr_text(path: str) -> str:
    img = Image.open(path)
    configs = [
        "--psm 6", "--psm 4", "--psm 3", "--psm 11",
        "--psm 6 -c tessedit_char_whitelist=0123456789/-.:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
    ]
    texts = []
    pre = _preprocess(img)
    for p in pre:
        try:
            t = pytesseract.image_to_string(p, config=configs[0])
            if t.strip():
                texts.append(t)
        except Exception:
            pass
    for cfg in configs[1:3]:
        for p in pre[:2]:
            try:
                t = pytesseract.image_to_string(p, config=cfg)
                if t.strip():
                    texts.append(t)
            except Exception:
                pass
    return "\n".join(texts)


_DATE_PATTERNS: List[Tuple["re.Pattern", bool]] = [
    (re.compile(r"DATE[:\s]*([0-3]?\d[/\-][01]?\d[/\-]\d{2,4})", re.IGNORECASE), True),
    (re.compile(r"TARIKH[:\s]*([0-3]?\d[/\-][01]?\d[/\-]\d{2,4})", re.IGNORECASE), True),
    (re.compile(r"\b([0-3]?\d/[01]?\d/20\d{2})\b"), False),
    (re.compile(r"\b([0-3]?\d-[01]?\d-20\d{2})\b"), False),
    (re.compile(r"\b([0-3]?\d/[01]?\d/\d{2})\b"), False),
    (re.compile(r"\b([0-3]?\d-[01]?\d-\d{2})\b"), False),
    (re.compile(r"(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})"), False),
]


def _extract_date(text: str) -> Optional[datetime]:
    if not text:
        return None
    found: List[Tuple[datetime, bool]] = []
    for pat, ctx in _DATE_PATTERNS:
        for m in pat.findall(text):
            dt = _parse_date_any_format(m)
            if dt:
                found.append((dt, ctx))
    if not found:
        return None
    ctx_dates = [d for d, c in found if c]
    return ctx_dates[0] if ctx_dates else found[0][0]


_MONEY_RE = re.compile(r"(?:RM\s*)?(\d{1,3}(?:[,\s]\d{3})*\.\d{2}|\d+\.\d{2})", re.IGNORECASE)
_TOTAL_KEYWORDS = [r"GRAND\s*TOTAL", r"TOTAL\s*:?\s*RM", r"TOTAL\s*AMOUNT", r"TOTAL\s*DUE",
                   r"AMOUNT\s*DUE", r"BALANCE\s*DUE", r"NETT\s*TOTAL", r"NET\s*TOTAL",
                   r"\bTOTAL\b", r"\bAMOUNT\b"]
_EXCLUDE_KEYWORDS = [r"SUB\s*TOTAL", r"SUBTOTAL", r"TAX", r"GST", r"SST",
                     r"DISCOUNT", r"CHANGE", r"CASH\s*TENDERED"]


def _extract_total(text: str) -> Optional[Decimal]:
    if not text:
        return None
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    total_re = re.compile("|".join(_TOTAL_KEYWORDS), re.IGNORECASE)
    exclude_re = re.compile("|".join(_EXCLUDE_KEYWORDS), re.IGNORECASE)
    candidates: List[Tuple[Decimal, int]] = []
    for i, line in enumerate(lines):
        if exclude_re.search(line):
            continue
        if total_re.search(line):
            nums = _MONEY_RE.findall(line)
            if nums:
                try:
                    val = Decimal(nums[-1].replace(",", "").replace(" ", ""))
                    if re.search(r"GRAND\s*TOTAL", line, re.IGNORECASE):
                        pri = 50
                    elif re.search(r"TOTAL\s*:?\s*RM", line, re.IGNORECASE):
                        pri = 40
                    elif re.search(r"TOTAL\s*AMOUNT", line, re.IGNORECASE):
                        pri = 30
                    else:
                        pri = 20
                    candidates.append((val, pri))
                except Exception:
                    pass
            if not nums and i + 1 < len(lines):
                nxt = _MONEY_RE.findall(lines[i + 1])
                if nxt:
                    try:
                        candidates.append((Decimal(nxt[-1].replace(",", "").replace(" ", "")), 10))
                    except Exception:
                        pass
    if candidates:
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    return None


def _write_status(path: Optional[str], payload: dict) -> None:
    if not path:
        return
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(payload, f)
        os.replace(tmp, path)
    except Exception:
        pass


def _fail(status_path, msg):
    _write_status(status_path, {"state": "error", "error": msg})
    print(json.dumps({"success": False, "error": msg}))
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="OCR receipt images into a stats xlsx.")
    ap.add_argument("--input", required=True, help="Directory of receipt images")
    ap.add_argument("--output", required=True, help="Output .xlsx path")
    ap.add_argument("--status", default=None, help="Optional path to write live job status JSON")
    args = ap.parse_args()
    status_path = args.status

    in_dir = os.path.normpath(args.input)
    if not os.path.isdir(in_dir):
        _fail(status_path, f"Input dir not found: {in_dir}")

    if not ensure_tessdata("eng"):
        _fail(status_path, "Tesseract language data not found. "
              "Install: conda install -c conda-forge tesseract  (or set TESSDATA_PREFIX "
              "to a dir containing eng.traineddata).")

    exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp"}
    files = sorted(f for f in os.listdir(in_dir)
                   if os.path.splitext(f)[1].lower() in exts)
    if not files:
        _fail(status_path, f"No images in {in_dir} (looked for {sorted(exts)})")

    total = len(files)
    _write_status(status_path, {"state": "running", "images": total, "processed": 0,
                                "output": args.output})

    rows: Dict[str, Dict[str, Optional[str]]] = {}
    both_ok = 0
    for i, name in enumerate(files, 1):
        try:
            text = _ocr_text(os.path.join(in_dir, name))
        except Exception:
            text = ""
        dt = _extract_date(text) if text else None
        amt = _extract_total(text) if text else None
        rows[name] = {
            "date": dt.strftime("%Y-%m-%d") if dt else None,
            "total_amount": _two_dp(amt) if amt is not None else None,
        }
        if dt and amt is not None:
            both_ok += 1
        _write_status(status_path, {"state": "running", "images": total, "processed": i,
                                    "last": name, "output": args.output})

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "results"
    ws.append(["filename", "date", "total_amount"])
    for name in sorted(rows):
        ws.append([name, rows[name]["date"], rows[name]["total_amount"]])
    wb.save(args.output)

    summary = {
        "success": True,
        "state": "done",
        "output": args.output,
        "images": total,
        "fully_extracted": both_ok,
        "partial_or_failed": total - both_ok,
    }
    _write_status(status_path, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
