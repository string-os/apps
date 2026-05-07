# Requirements

## System Dependencies

| Package | Required for | Install |
|---------|--------------|---------|
| `pandoc` | All conversions (MD↔DOCX, MD→PDF, DOCX→MD) | `apt install pandoc` / `brew install pandoc` / `choco install pandoc` |
| `wkhtmltopdf` | MD→PDF (recommended PDF engine) | `apt install wkhtmltopdf` / `brew install wkhtmltopdf` |
| `pdftotext` | `/act.read_pdf` | `apt install poppler-utils` / `brew install poppler` |
| `libreoffice` | `/act.docx_to_pdf` (DOCX→PDF) | `apt install libreoffice-writer` / `brew install --cask libreoffice` |

## Verification

```bash
pandoc --version | head -1     # pandoc 3.x
wkhtmltopdf --version          # wkhtmltopdf 0.12.6+
pdftotext -v 2>&1 | head -1    # pdftotext version 24.x
libreoffice --version          # LibreOffice 24.x
```

## What each action needs

- `/act.read` (DOCX → text) → `pandoc`
- `/act.read_pdf` → `pdftotext`
- `/act.create` (write MD as DOCX) → `pandoc`
- `/act.to_docx` → `pandoc`
- `/act.to_pdf` (MD → PDF) → `pandoc` **and** a PDF engine (`wkhtmltopdf` is the easiest; `xelatex` from texlive works but is much heavier)
- `/act.docx_to_pdf` → `libreoffice`

## Notes

- **`pandoc` is the core dependency.** Install it first; everything else gates only specific actions.
- **PDF engine choice:** `wkhtmltopdf` is the lightest and most predictable for HTML-style output. `xelatex` (`apt install texlive-xetex`) handles Unicode and complex layouts better but adds 1+ GB. Pick one based on your input.
- For styled DOCX output, generate a reference template once: `pandoc --print-default-data-file reference.docx > template.docx`, then pass `--reference-doc=template.docx`.
- **`libreoffice` runs headless** for `/act.docx_to_pdf` (`--headless --convert-to pdf`). It's slower than pandoc-based conversion but renders fonts and layout closer to Word.
