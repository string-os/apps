---
title: site-builder Requirements
---

# Requirements

This app scaffolds and builds Astro + `@string-os/astro-sfmd` sites.

## Commands

- `node` (v20+) and `npm` — to install deps and build the generated site.
- `git` — to version the generated site.
- `gh` (optional) — only needed when you create the GitHub repo / enable Pages
  yourself; this app does not create repos or deploy.

`astro` and `@string-os/astro-sfmd` are pulled in per-site via `npm install`
(they are dependencies of the scaffolded `package.json`).

## How the astro-sfmd CLI is resolved

The helper prefers an `astro-sfmd` already on `PATH` (global or local install);
otherwise it falls back to `npx -y @string-os/astro-sfmd`. Scaffolding the
GitHub Pages preset (`new`, `init --github-pages`) requires
`@string-os/astro-sfmd` **>= 0.2.0**.

## Notes

- The app never creates a public GitHub repo or triggers a live deploy. It
  prepares the site and prints the one-time manual steps (enable Pages =
  "GitHub Actions", set `base` for project pages).
- Generated sites keep all content as markdown under `content/`; each page ships
  as both styled HTML and a raw `.md` twin for agents.
