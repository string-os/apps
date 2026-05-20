---
name: docx
namespace: stringhub
version: 1.0.1
description: Create, read, and convert Word documents and PDFs. Markdown to DOCX, DOCX to Markdown, PDF to text.
tags: [utilities, docx, word, pdf, document, convert, pandoc]
type: app
default: read
---

[!requirements](./requirements.md)

# Document Tools

Read, create, and convert Word (DOCX), PDF, and Markdown documents.
Backed by [pandoc](https://pandoc.org) for most conversions,
`pdftotext` (poppler-utils) for PDF reading, and headless LibreOffice for
DOCX→PDF. Install the binaries once; no API key, no signup.

## Actions

- `/act.read --file <path.docx>` — DOCX → Markdown
- `/act.read_pdf --file <path.pdf>` — PDF → plain text
- `/act.to_docx --input <path.md> --output <path.docx>` — Markdown → DOCX
- `/act.to_pdf --input <path.md> --output <path.pdf>` — Markdown → PDF
- `/act.docx_to_pdf --input <path.docx> --output <path.pdf>` — DOCX → PDF
- `/act.create --output <path.docx> --content <markdown>` — write a DOCX from inline content

```act.read
CLI pandoc "{file}" -t markdown --wrap=none 2>/dev/null || echo "Failed. Install: apt install pandoc / brew install pandoc"
  file: string (required) "Path to .docx file"
```

```act.read_pdf
CLI pdftotext "{file}" - 2>/dev/null || python3 -c "
import subprocess,sys
try:
    r=subprocess.run(['pdftotext',sys.argv[1],'-'],capture_output=True,text=True)
    print(r.stdout)
except:
    print('Failed. Install: apt install poppler-utils / brew install poppler')
" "{file}" || echo "Failed. Install poppler-utils."
  file: string (required) "Path to .pdf file"
```

```act.to_docx
CLI pandoc "{input}" -o "{output}" --from=markdown --to=docx 2>/dev/null && echo "Created: {output}" || echo "Failed. Install pandoc."
  input: string (required) "Path to .md file"
  output: string (required) "Output .docx path"
```

```act.to_pdf
CLI pandoc "{input}" -o "{output}" --from=markdown --pdf-engine=xelatex 2>/dev/null || pandoc "{input}" -o "{output}" --from=markdown --pdf-engine=wkhtmltopdf 2>/dev/null && echo "Created: {output}" || echo "Failed. Install pandoc + a PDF engine (xelatex or wkhtmltopdf)."
  input: string (required) "Path to .md file"
  output: string (required) "Output .pdf path"
```

```act.docx_to_pdf
CLI libreoffice --headless --convert-to pdf --outdir "$(dirname {output})" "{input}" 2>/dev/null && echo "Created: {output}" || echo "Failed. Install LibreOffice: apt install libreoffice-writer"
  input: string (required) "Path to .docx file"
  output: string (required) "Output .pdf path"
```

```act.create
CLI echo "{content}" | pandoc -o "{output}" --from=markdown --to=docx 2>/dev/null && echo "Created: {output}" || echo "Failed. Install pandoc."
  output: string (required) "Output .docx path"
  content: string (required) "Document content (markdown supported)"
```
