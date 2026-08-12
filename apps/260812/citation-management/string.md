---
title: Citation Management
name: citation-management
namespace: stringhub
type: app
version: 0.1.0
description: "Comprehensive citation management for academic research. Search Google Scholar and PubMed for papers, extract accurate metadata, validate citations, and generate properly formatted BibTeX entries. This skill should be used when you need to find papers, verify citation information, convert DOIs to BibTeX, or ensure reference accuracy in scientific writing."
tags: [citations, bibtex, pubmed, scholar, metadata]
---

[!requirements](./requirements.txt)

# Citation Management

Search academic databases, extract paper metadata, and produce/validate BibTeX through
actions. The daemon runs the underlying API clients (CrossRef, PubMed E-utilities, arXiv,
Google Scholar) — call an action instead of writing the requests. Actions print to stdout
or write to a `--output` file (JSON or BibTeX).

Each action's first String field is its query/file; remaining flags go in a `flags`/`args`
field as ONE space-separated string. Optionals below shown as `[--flag <type>]` with default.

## Search for papers
**Decision:** Scholar = general/cross-field coverage + citation impact (best for citation counts,
seminal work); PubMed = biomedical/life-sciences, MeSH terms, publication-type/date precision.
- **`/act.search_google_scholar`** `--query <q>` (positional String field) `[--limit <n>]` (default
  `50`) `[--year-start <y>]` `[--year-end <y>]` `[--sort-by relevance|citations]` (default `relevance`)
  `[--use-proxy]` `[--output <file> | -o]` (default stdout) `[--format json|bibtex]` (default `json`).
- **`/act.search_pubmed`** `--query <expr>` (positional String field; or use `--query <q>` / `--query-file
  <path>` in flags) `[--limit <n>]` (default `100`) `[--date-start <y>]` `[--date-end <y>]`
  `[--publication-types <types>]` `[--output <file> | -o]` `[--format json|bibtex]` (default `json`)
  `[--api-key <key>]` `[--email <addr>]`.

## Identifier → metadata / BibTeX
**Decision:** prefer DOIs (most reliable, CrossRef-sourced). Use `doi_to_bibtex` for fast bulk DOI→BibTeX;
use `extract_metadata` for richer extraction or non-DOI ids (PMID/arXiv/URL/mixed file).
- **`/act.doi_to_bibtex`** `<doi> [<doi> ...]` (positional, via the `args` field) OR `--input <file> | -i`
  (one DOI per line) `[--output <file> | -o]` `[--delay <sec>]` (default `0.5`) `[--format bibtex|json]`
  (default `bibtex`). The whole `args` string is required — pass DOIs and/or flags.
- **`/act.extract_metadata`** — supply ONE identifier flag in the required `flags` field: `--doi <doi>`
  | `--pmid <pmid>` | `--arxiv <id>` | `--url <url>` | `--input <file> | -i` (mixed ids); plus
  `[--output <file> | -o]` `[--format bibtex|json]` (default `bibtex`) `[--email <addr>]`.

## Format & validate BibTeX
- **`/act.format_bibtex`** `--file <.bib>` (positional String field) `[--output <file> | -o]` (default:
  overwrite input) `[--deduplicate]` `[--sort key|year|author|title]` `[--descending]` `[--no-fix]`
  (skip common-syntax fixes; fixes run by default) — standardize a `.bib` file.
- **`/act.validate_citations`** `--file <.bib>` (positional String field) `[--check-dois]` (verify DOIs
  resolve — slow) `[--auto-fix]` (attempt safe fixes) `[--report <file>]` (write JSON report)
  `[--verbose]` — verify required fields per entry type, duplicates, format compliance.

Typical bibliography build: search → `extract_metadata` (or `doi_to_bibtex`) →
`format_bibtex --deduplicate --sort year` → `validate_citations --check-dois`. Always
validate before final submission, and spot-check key citations against the source.

Deep-reference docs are bundled under `references/` (Scholar/PubMed search syntax,
metadata sources, validation criteria, BibTeX entry types) and `assets/` (a BibTeX
template + checklist) — you shouldn't need them to run the actions.

## Actions

```act.search_google_scholar
CLI ./scripts/_optshim.sh python3 ./scripts/search_google_scholar.py "{query}" -- {flags}
  query: string (required) "Search query for Google Scholar"
  flags: string (optional) "Extra CLI flags, e.g. --limit 50 --year-start 2020 --output results.json" = ""
```

```act.search_pubmed
CLI ./scripts/_optshim.sh python3 ./scripts/search_pubmed.py "{query}" -- {flags}
  query: string (required) "Search query / PubMed expression"
  flags: string (optional) "Extra CLI flags, e.g. --date-start 2020 --publication-types Review --output out.json" = ""
```

```act.extract_metadata
CLI ./scripts/_optshim.sh python3 ./scripts/extract_metadata.py -- {flags}
  flags: string (required) "Identifier flags, e.g. --doi 10.1038/... | --pmid 34265844 | --arxiv 2103.14030 | --input ids.txt --output refs.bib"
```

```act.doi_to_bibtex
CLI ./scripts/_optshim.sh python3 ./scripts/doi_to_bibtex.py -- {args}
  args: string (required) "One or more DOIs, or flags like --input dois.txt --output references.bib"
```

```act.format_bibtex
CLI ./scripts/_optshim.sh python3 ./scripts/format_bibtex.py "{bibfile}" -- {flags}
  bibfile: string (required) "Path to the .bib file to format"
  flags: string (optional) "Extra flags, e.g. --sort year --descending --deduplicate --output out.bib" = ""
```

```act.validate_citations
CLI ./scripts/_optshim.sh python3 ./scripts/validate_citations.py "{bibfile}" -- {flags}
  bibfile: string (required) "Path to the .bib file to validate"
  flags: string (optional) "Extra flags, e.g. --auto-fix --report validation.json --output fixed.bib" = ""
```
