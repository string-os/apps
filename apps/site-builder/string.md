---
name: site-builder
namespace: stringhub
version: 0.1.0
description: Scaffold and deploy human+AI websites — styled HTML for people, raw .md for agents — to GitHub Pages or Vercel.
tags: [devtools, sfmd, astro, website, github-pages, generator]
type: app
default: help
requires: []
---

# site-builder

Spin up a **human + AI website** in one command. You get a complete Astro site
that emits two surfaces from one `content/` tree: styled **HTML for people** and
the raw **`.md` twin for agents**. Deploy it to **GitHub Pages** (static, no
server) or **Vercel** (runtime Accept-negotiation).

This app is a thin, friendly wrapper over the
[`@string-os/astro-sfmd`](https://github.com/string-os/astro-sfmd) CLI plus a
couple of content helpers.

```
/act.new -d my-site --blog --docs    # scaffold a starter site
/act.page -d my-site -t "Pricing" -p pricing       # add a page
/act.post -d my-site -t "Launch"     # add a dated blog post
/act.build -d my-site                # build + verify HTML/.md twins
/act.deploy -d my-site               # add the GitHub Pages workflow + go-live steps
```

Full signatures: `/act.<name> --help`.

[!requirements](./requirements.md)

## The human + AI model

Every page exists twice in the build output:

```
dist/about/index.html   ← styled HTML, for browsers (people)
dist/about.md           ← raw markdown twin, for AI agents
```

An agent reads any page by appending `.md` to its URL (`/about` → `/about.md`).
On a **static host like GitHub Pages there is no middleware**, but the `.md`
twins are real files emitted at build time — so the AI view works with zero
server logic. That is the frictionless default this app sets up.

## GitHub Pages vs Vercel

- **GitHub Pages (default)** — fully static. The build mirrors `.md` twins into
  `dist/`, and a generated `.github/workflows/deploy.yml` publishes on push.
  No server, no runtime cost. Agents fetch `/path.md` directly. Best for most
  landing/blog/docs sites.
- **Vercel** — adds a `middleware.ts` that negotiates on the `Accept` header, so
  the *same* clean URL serves HTML to browsers and markdown to agents
  requesting `Accept: text/markdown`. Pick this if you want header-based
  negotiation instead of explicit `.md` URLs.

## The content tree

All pages are markdown under `content/`:

```
content/
  index.md         # landing
  about.md         # a sample page
  blog/            # (with --blog) dated posts + an auto-generated index
  docs/            # (with --docs) documentation pages
  nav/main.md      # site navigation (shortcut links)
```

Add a page by dropping a `.md` file under `content/` (or use `/act.page`). Each
becomes both an HTML route and a `.md` twin. Blog posts are dated files under
`content/blog/`; their index listing is regenerated on every build.

## Typical flow

1. `/act.new -d my-site --blog` — scaffold.
2. `/act.page` / `/act.post` — add content.
3. `/act.build` — build and confirm both surfaces exist in `dist/`.
4. `/act.deploy` — write the Pages workflow, then enable Pages in repo settings.

Creating the GitHub repo and going live are deliberately left to you — this app
prepares everything up to that point.

```act.help
CLI printf '%s\n' "site-builder — scaffold human+AI (SFMD) websites." "" "Actions:" "  /act.new -d <dir> [-t github-pages|vercel] [--blog] [--docs]" "  /act.page -d <dir> -t <title> -p <path>" "  /act.post -d <dir> -t <title> [--date YYYY-MM-DD]" "  /act.build -d <dir>" "  /act.deploy -d <dir> [-t github-pages|vercel]" "" "Start with /act.new, then /act.build to see the HTML + .md twins."
```

```act.help.response
{Response.body}

next: /act.new -d my-site --blog   ·   then /act.build -d my-site
```

```act.new
CLI ./site-builder new {dir} {target} {blog} {docs}
  dir, -d:    string (required) "Directory to scaffold into (also the repo/site name)"
  target, -t: string "Host: github-pages (default) or vercel" = "github-pages"
  blog, -b:   boolean "Include a sample blog with an auto-generated index" = "false"
  docs:       boolean "Include a sample docs section" = "false"
```

```act.new.response
{Response.body}

next: /act.build -d <dir>   ·   /act.page -d <dir> -t "Title" -p path   ·   /act.deploy -d <dir>
```

```act.page
CLI ./site-builder page {dir} {title} {path}
  dir, -d:   string (required) "Site directory"
  title, -t: string (required) "Page title (frontmatter + H1)"
  path, -p:  string (required) "Route path under content/, e.g. 'pricing' or 'guides/intro'"
```

```act.page.response
{Response.body}

next: /act.build -d <dir>
```

```act.post
CLI ./site-builder post {dir} {title} {date}
  dir, -d:   string (required) "Site directory"
  title, -t: string (required) "Post title"
  date:      string "Publish date YYYY-MM-DD (defaults to today, UTC)" = ""
```

```act.post.response
{Response.body}

next: /act.build -d <dir>
```

```act.build
CLI ./site-builder build {dir}
  dir, -d: string (required) "Site directory to build"
```

```act.build.response
{Response.body}

next: /act.deploy -d <dir>   ·   add more: /act.page · /act.post
```

```act.deploy
CLI ./site-builder deploy {dir} {target}
  dir, -d:    string (required) "Site directory"
  target, -t: string "Host: github-pages (default) or vercel" = "github-pages"
```

```act.deploy.response
{Response.body}
```
