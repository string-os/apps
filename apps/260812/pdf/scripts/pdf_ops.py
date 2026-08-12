#!/usr/bin/env python3
"""General PDF operations the `pdf` skill teaches, exposed as String actions.

Each subcommand wraps the exact library usage documented in the skill guide
(pypdf / pdfplumber / poppler), so the agent calls an action instead of writing
the boilerplate. All output is JSON ({"ok": true, ...} / {"ok": false, "error"})
unless a subcommand writes a file, in which case it reports the path.
"""
import sys, os, json, subprocess


def _clean(v):
    """Optional String flags arrive as '' (literal two chars), an unsubstituted
    {placeholder}, or empty. Normalize all of those to '' (unset)."""
    if v is None:
        return ""
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    if v.startswith("{") and v.endswith("}"):
        return ""
    return v


def out(d):
    print(json.dumps(d))
    sys.exit(0 if d.get("ok") else 1)


def err(msg):
    out({"ok": False, "error": msg})


def extract_text(args):
    import pdfplumber
    pdf = _clean(args.get(0)); dest = _clean(args.get(1)); layout = _clean(args.get(2)) in ("1", "true", "layout", "yes")
    if not pdf or not os.path.exists(pdf):
        err(f"PDF not found: {pdf!r}. Usage: extract_text <pdf> [out_txt] [layout]")
    chunks = []
    with pdfplumber.open(pdf) as doc:
        for page in doc.pages:
            chunks.append(page.extract_text(layout=True) if layout else page.extract_text() or "")
    text = "\n\n".join(chunks)
    if dest:
        open(dest, "w").write(text)
        out({"ok": True, "pages": len(chunks), "out": dest, "chars": len(text)})
    out({"ok": True, "pages": len(chunks), "text": text})


def extract_tables(args):
    import pdfplumber, csv
    pdf = _clean(args.get(0)); dest = _clean(args.get(1)); fmt = _clean(args.get(2)) or "json"
    if not pdf or not os.path.exists(pdf):
        err(f"PDF not found: {pdf!r}. Usage: extract_tables <pdf> [out] [json|csv]")
    tables = []
    with pdfplumber.open(pdf) as doc:
        for i, page in enumerate(doc.pages):
            for t in page.extract_tables():
                tables.append({"page": i + 1, "rows": t})
    if dest and fmt == "csv":
        with open(dest, "w", newline="") as f:
            w = csv.writer(f)
            for tb in tables:
                w.writerow([f"# page {tb['page']}"])
                w.writerows(tb["rows"])
        out({"ok": True, "tables": len(tables), "out": dest})
    if dest:
        json.dump(tables, open(dest, "w"))
        out({"ok": True, "tables": len(tables), "out": dest})
    out({"ok": True, "tables": len(tables), "data": tables})


def metadata(args):
    from pypdf import PdfReader
    pdf = _clean(args.get(0))
    if not pdf or not os.path.exists(pdf):
        err(f"PDF not found: {pdf!r}. Usage: metadata <pdf>")
    r = PdfReader(pdf)
    m = r.metadata or {}
    out({"ok": True, "pages": len(r.pages),
         "title": getattr(m, "title", None), "author": getattr(m, "author", None),
         "subject": getattr(m, "subject", None), "creator": getattr(m, "creator", None),
         "producer": getattr(m, "producer", None)})


def merge(args):
    from pypdf import PdfReader, PdfWriter
    inputs = _clean(args.get(0)); dest = _clean(args.get(1))
    files = [p for p in inputs.split() if p]
    if len(files) < 2 or not dest:
        err('Usage: merge "<a.pdf b.pdf ...>" <out.pdf> (inputs are one space-separated quoted string)')
    w = PdfWriter()
    for fp in files:
        if not os.path.exists(fp):
            err(f"input not found: {fp}")
        for page in PdfReader(fp).pages:
            w.add_page(page)
    with open(dest, "wb") as f:
        w.write(f)
    out({"ok": True, "merged": files, "out": dest})


def split(args):
    from pypdf import PdfReader, PdfWriter
    pdf = _clean(args.get(0)); out_dir = _clean(args.get(1)) or "."
    if not pdf or not os.path.exists(pdf):
        err(f"PDF not found: {pdf!r}. Usage: split <pdf> [out_dir]")
    os.makedirs(out_dir, exist_ok=True)
    r = PdfReader(pdf); written = []
    for i, page in enumerate(r.pages):
        w = PdfWriter(); w.add_page(page)
        p = os.path.join(out_dir, f"page_{i+1}.pdf")
        with open(p, "wb") as f:
            w.write(f)
        written.append(p)
    out({"ok": True, "pages": len(written), "out_dir": out_dir, "files": written})


def rotate(args):
    from pypdf import PdfReader, PdfWriter
    pdf = _clean(args.get(0)); dest = _clean(args.get(1))
    deg = int(_clean(args.get(2)) or "90"); pages = _clean(args.get(3))
    if not pdf or not os.path.exists(pdf) or not dest:
        err("Usage: rotate <pdf> <out.pdf> [degrees=90] [pages e.g. '1 3' | all]")
    want = set(int(x) for x in pages.split()) if pages and pages != "all" else None
    r = PdfReader(pdf); w = PdfWriter()
    for i, page in enumerate(r.pages, 1):
        if want is None or i in want:
            page.rotate(deg)
        w.add_page(page)
    with open(dest, "wb") as f:
        w.write(f)
    out({"ok": True, "out": dest, "degrees": deg, "rotated": "all" if want is None else sorted(want)})


def ocr(args):
    pdf = _clean(args.get(0)); dest = _clean(args.get(1))
    if not pdf or not os.path.exists(pdf):
        err(f"PDF not found: {pdf!r}. Usage: ocr <pdf> [out_txt]")
    import pytesseract
    from pdf2image import convert_from_path
    text = ""
    for i, img in enumerate(convert_from_path(pdf)):
        text += f"Page {i+1}:\n" + pytesseract.image_to_string(img) + "\n\n"
    if dest:
        open(dest, "w").write(text)
        out({"ok": True, "out": dest, "chars": len(text)})
    out({"ok": True, "text": text})


def extract_images(args):
    pdf = _clean(args.get(0)); prefix = _clean(args.get(1)) or "image"
    if not pdf or not os.path.exists(pdf):
        err(f"PDF not found: {pdf!r}. Usage: extract_images <pdf> [out_prefix]")
    os.makedirs(os.path.dirname(prefix) or ".", exist_ok=True)
    r = subprocess.run(["pdfimages", "-j", pdf, prefix], capture_output=True, text=True)
    if r.returncode != 0:
        err(f"pdfimages failed: {r.stderr.strip()}")
    import glob
    out({"ok": True, "prefix": prefix, "images": sorted(glob.glob(prefix + "*"))})


def encrypt(args):
    from pypdf import PdfReader, PdfWriter
    pdf = _clean(args.get(0)); dest = _clean(args.get(1))
    user_pw = _clean(args.get(2)); owner_pw = _clean(args.get(3)) or user_pw
    if not pdf or not os.path.exists(pdf) or not dest or not user_pw:
        err("Usage: encrypt <pdf> <out.pdf> <user_password> [owner_password]")
    r = PdfReader(pdf); w = PdfWriter()
    for page in r.pages:
        w.add_page(page)
    w.encrypt(user_pw, owner_pw)
    with open(dest, "wb") as f:
        w.write(f)
    out({"ok": True, "out": dest})


def decrypt(args):
    from pypdf import PdfReader, PdfWriter
    pdf = _clean(args.get(0)); dest = _clean(args.get(1)); pw = _clean(args.get(2))
    if not pdf or not os.path.exists(pdf) or not dest:
        err("Usage: decrypt <pdf> <out.pdf> <password>")
    r = PdfReader(pdf)
    if r.is_encrypted:
        r.decrypt(pw)
    w = PdfWriter()
    for page in r.pages:
        w.add_page(page)
    with open(dest, "wb") as f:
        w.write(f)
    out({"ok": True, "out": dest})


OPS = {"extract_text": extract_text, "extract_tables": extract_tables, "metadata": metadata,
       "merge": merge, "split": split, "rotate": rotate, "ocr": ocr,
       "extract_images": extract_images, "encrypt": encrypt, "decrypt": decrypt}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in OPS:
        err(f"unknown op. one of: {', '.join(OPS)}")
    rest = sys.argv[2:]
    args = {i: rest[i] for i in range(len(rest))}
    try:
        OPS[sys.argv[1]](type("A", (), {"get": lambda self, i: args.get(i)})())
    except Exception as e:
        err(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
