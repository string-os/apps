# Requirements

`jpg-ocr-stat` runs Python helpers under `scripts/`. Install what each page needs.

## Python packages (all pages rely on some of these)

| Package | Used by | Install |
|---------|---------|---------|
| `pytesseract`, `Pillow` | Home, Image OCR | `conda install -c conda-forge pytesseract pillow` |
| `openpyxl` | Home, XLSX | `conda install -c conda-forge openpyxl` |
| `openai` | OpenAI Vision | `pip install openai` |
| `opencv-python-headless` (`cv2`) | Video → frames | `pip install opencv-python-headless` |

## System binaries

| Binary | Used by | Install |
|--------|---------|---------|
| `tesseract` | Home, Image OCR | `conda install -c conda-forge tesseract` / `apt install tesseract-ocr` / `brew install tesseract` |
| `pdftotext`, `pdftoppm` (poppler) | PDF | `conda install -c conda-forge poppler` / `apt install poppler-utils` / `brew install poppler` |

Verify in one shot:

```bash
python3 -c "import pytesseract, PIL, openpyxl; print('py core OK')"
which tesseract pdftotext pdftoppm
python3 -c "import cv2; print('cv2', cv2.__version__)"   # only for video page
python3 -c "import openai; print('openai OK')"           # only for vision page
```

## Environment variables

| Variable | Used by | Notes |
|----------|---------|-------|
| `OPENAI_API_KEY` | OpenAI Vision | Required only for the `@vision` page. Get one at <https://platform.openai.com/api-keys>. Set via env or a `chmod 600` `.env` — never commit it. |

Tesseract-based pages (Home, Image OCR) and the PDF/XLSX/Video pages need **no**
API key. Each action fails with an actionable message (which package/binary/var
to install or set) rather than a stack trace.

## Pages in this app

- [`string.md`](string.md) — **Home**: receipt images → stats xlsx (default `/act.stat`)
- [`image-ocr.md`](image-ocr.md) — Tesseract OCR for a single image
- [`openai-vision.md`](openai-vision.md) — OpenAI vision OCR / analysis
- [`pdf.md`](pdf.md) — PDF → text, or PDF pages → images
- [`video-frame-extraction.md`](video-frame-extraction.md) — video → frames
- [`xlsx.md`](xlsx.md) — read / write .xlsx

Navigate with the menu shortcuts (`@home`, `@imageocr`, `@vision`, `@pdf`,
`@video`, `@xlsx`) or `/open <file>.md`.
