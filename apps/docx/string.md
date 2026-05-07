---
name: docx
namespace: stringhub
version: 1.0.0
description: Create, read, and convert Word documents and PDFs. Markdown to DOCX, DOCX to Markdown, PDF to text.
tags: [utilities, docx, word, pdf, document, convert, pandoc]
type: app
default: read
---

# Document Tools

Read, create, and convert documents. Word (DOCX), PDF, and Markdown interconversion.

---

## Read DOCX as Markdown

`/act.read --file "report.docx"`

```act.read
CLI pandoc "{file}" -t markdown --wrap=none 2>/dev/null || echo "Failed. Install: apt install pandoc / brew install pandoc"
  file: string (required) "Path to .docx file"
```

---

## Read PDF as Text

`/act.read_pdf --file "paper.pdf"`

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

---

## Markdown → DOCX

`/act.to_docx --input "report.md" --output "report.docx"`

```act.to_docx
CLI pandoc "{input}" -o "{output}" --from=markdown --to=docx 2>/dev/null && echo "Created: {output}" || echo "Failed. Install pandoc."
  input: string (required) "Path to .md file"
  output: string (required) "Output .docx path"
```

---

## Markdown → PDF

`/act.to_pdf --input "report.md" --output "report.pdf"`

```act.to_pdf
CLI pandoc "{input}" -o "{output}" --from=markdown --pdf-engine=xelatex 2>/dev/null || pandoc "{input}" -o "{output}" --from=markdown --pdf-engine=wkhtmltopdf 2>/dev/null && echo "Created: {output}" || echo "Failed. Install pandoc + a PDF engine (xelatex or wkhtmltopdf)."
  input: string (required) "Path to .md file"
  output: string (required) "Output .pdf path"
```

---

## DOCX → PDF

`/act.docx_to_pdf --input "report.docx" --output "report.pdf"`

```act.docx_to_pdf
CLI libreoffice --headless --convert-to pdf --outdir "$(dirname {output})" "{input}" 2>/dev/null && echo "Created: {output}" || echo "Failed. Install LibreOffice: apt install libreoffice-writer"
  input: string (required) "Path to .docx file"
  output: string (required) "Output .pdf path"
```

---

## Create DOCX from Text

`/act.create --output "letter.docx" --content "Dear team, ..."`

```act.create
CLI echo "{content}" | pandoc -o "{output}" --from=markdown --to=docx 2>/dev/null && echo "Created: {output}" || echo "Failed. Install pandoc."
  output: string (required) "Output .docx path"
  content: string (required) "Document content (markdown supported)"
```

---

## Tips

- `pandoc` handles most conversions: MD↔DOCX, MD→PDF, DOCX→MD
- PDF reading uses `pdftotext` (poppler-utils) — fast and accurate for text-based PDFs
- DOCX→PDF uses LibreOffice headless mode for best fidelity
- For styled DOCX, create a reference template: `pandoc --reference-doc=template.docx`
- Requires: `pandoc`, optionally `poppler-utils`, `libreoffice`, LaTeX
