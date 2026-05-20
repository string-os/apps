---
title: Document Tools — Requirements
---

# Requirements

| Package         | Used by                                    |
|-----------------|--------------------------------------------|
| `pandoc`        | `read`, `to_docx`, `to_pdf`, `create`      |
| `poppler-utils` | `read_pdf`                                 |
| `libreoffice`   | `docx_to_pdf`                              |
| `wkhtmltopdf`   | `to_pdf` (PDF engine — or `texlive-xetex`) |

```bash
apt install pandoc poppler-utils libreoffice wkhtmltopdf
brew install pandoc poppler wkhtmltopdf && brew install --cask libreoffice
```
