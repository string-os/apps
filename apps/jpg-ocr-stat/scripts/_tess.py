"""Shared Tesseract bootstrap: ensure TESSDATA_PREFIX points at real language data.

Conda's tesseract often ships traineddata under <prefix>/share/tessdata but does
not export TESSDATA_PREFIX, so OCR silently returns nothing. ensure_tessdata()
locates a tessdata dir containing the requested language and sets the env var
before pytesseract is used. Idempotent and best-effort.
"""

import glob
import os
import shutil


def ensure_tessdata(lang: str = "eng") -> bool:
    """Set TESSDATA_PREFIX if needed. Return True if language data was found."""
    def has_lang(d: str) -> bool:
        return bool(d) and os.path.isfile(os.path.join(d, f"{lang.split('+')[0]}.traineddata"))

    current = os.environ.get("TESSDATA_PREFIX")
    if has_lang(current):
        return True

    candidates = []
    conda = os.environ.get("CONDA_PREFIX")
    if conda:
        candidates.append(os.path.join(conda, "share", "tessdata"))
    tess = shutil.which("tesseract")
    if tess:
        base = os.path.dirname(os.path.dirname(os.path.realpath(tess)))
        candidates.append(os.path.join(base, "share", "tessdata"))
    candidates += [
        "/usr/share/tessdata",
        "/usr/local/share/tessdata",
        "/opt/homebrew/share/tessdata",
    ]
    candidates += sorted(glob.glob("/usr/share/tesseract-ocr/*/tessdata"))

    for d in candidates:
        if has_lang(d):
            os.environ["TESSDATA_PREFIX"] = d
            return True
    return False
