#!/usr/bin/env python3
"""Tesseract OCR for a single image -> JSON {text, confidence, ...}.

Multi-pass when --multipass is set (tries several preprocess + PSM combos and
concatenates), otherwise a single clean pass with per-word confidence.
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageOps, ImageFilter
    import pytesseract
except ImportError as e:
    print(json.dumps({"success": False, "error": f"Missing dependency: {e.name}. "
                      "Install: conda install -c conda-forge tesseract pytesseract pillow"}))
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tess import ensure_tessdata  # noqa: E402


def single_pass(img, lang, psm):
    cfg = f"--psm {psm}"
    data = pytesseract.image_to_data(img, lang=lang, config=cfg,
                                     output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(img, lang=lang, config=cfg)
    confs = [c for c in data["conf"] if isinstance(c, (int, float)) and c > 0]
    avg = sum(confs) / len(confs) if confs else 0
    regions = len({b for b in data["block_num"] if b > 0})
    level = "high" if avg >= 80 else "medium" if avg >= 50 else "low"
    return text.strip(), avg, level, regions


def multi_pass(img, lang):
    gray = ImageOps.grayscale(img)
    variants = [ImageOps.autocontrast(gray),
                ImageOps.invert(ImageOps.autocontrast(gray)),
                gray.filter(ImageFilter.SHARPEN)]
    out = []
    for v in variants:
        for psm in ("6", "4", "11"):
            try:
                t = pytesseract.image_to_string(v, lang=lang, config=f"--psm {psm}")
                if t.strip():
                    out.append(t.strip())
            except Exception:
                pass
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="OCR a single image with Tesseract.")
    ap.add_argument("--image", required=True, help="Path to image (jpg/png/webp/...)")
    ap.add_argument("--lang", default="eng", help="Tesseract language(s), e.g. eng or eng+fra")
    ap.add_argument("--psm", default="3", help="Page segmentation mode (single pass)")
    ap.add_argument("--multipass", action="store_true", help="Run multiple preprocess+PSM passes")
    args = ap.parse_args()

    if not os.path.isfile(args.image):
        print(json.dumps({"success": False, "error": f"Image not found: {args.image}"}))
        sys.exit(1)
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        print(json.dumps({"success": False, "error": "Tesseract binary not found. "
                          "Install: conda install -c conda-forge tesseract"}))
        sys.exit(1)
    if not ensure_tessdata(args.lang):
        print(json.dumps({"success": False, "error": f"Tesseract language data for '{args.lang}' not found. "
                          "Install the language pack or set TESSDATA_PREFIX to a dir with "
                          f"{args.lang.split('+')[0]}.traineddata."}))
        sys.exit(1)

    try:
        img = Image.open(args.image)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Cannot open image: {e}"}))
        sys.exit(1)

    filename = os.path.basename(args.image)
    if args.multipass:
        text = multi_pass(img, args.lang)
        result = {"success": True, "filename": filename, "mode": "multipass",
                  "extracted_text": text, "confidence": "n/a (combined passes)"}
    else:
        text, avg, level, regions = single_pass(img, args.lang, args.psm)
        result = {"success": True, "filename": filename, "mode": f"single psm={args.psm}",
                  "extracted_text": text, "confidence": level,
                  "avg_confidence": round(avg, 1), "text_regions": regions}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
