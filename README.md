# String Apps

A curated collection of ready-to-use String apps for the [String](https://github.com/string-os/string) runtime. Each app is a self-contained markdown document (or directory) the agent installs once and uses through `/open` and `/act`.

This is the source repo. Apps published from here also appear in the [StringHub marketplace](https://stringhub.org) under the `stringhub` namespace.

---

## What's in this repo

| App | What it does | Key dependencies | Auth |
|---|---|---|---|
| [translate](./apps/translate/) | Translate text between languages (MyMemory API) | none | none |
| [websearch](./apps/websearch/) | Search Wikipedia, Hacker News, DuckDuckGo | none | none |
| [weather](./apps/weather/) | Current weather, forecast, city lookup (Open-Meteo) | none | none |
| [gh-issue](./apps/gh-issue/) | GitHub issue triage: list, search, read, comment, label, assign | `gh` | `gh auth login` (one-time, human) |
| [github](./apps/github/) | Issues, PRs, repos, notifications via `gh` CLI | `gh` | `gh auth login` (one-time, human) |
| [youtube](./apps/youtube/) | Video metadata + transcript via `yt-dlp` | `yt-dlp` | none |
| [humanizer](./apps/humanizer/) | Detect AI-writing patterns and suggest fixes | `python3` | none |
| [docx](./apps/docx/) | Word/PDF read/write, format conversion via `pandoc` | `pandoc` (+ optional `wkhtmltopdf`, `pdftotext`, `libreoffice`) | none |
| [whisper](./apps/whisper/) | Local speech-to-text with OpenAI Whisper | `whisper`, `ffmpeg` | none |
| [notion](./apps/notion/) | Search, read, write, comment on pages; query databases | `curl`, `python3` | `$NOTION_TOKEN` |
| [google](./apps/google/) | Gmail, Calendar, Drive via gcloud ADC + REST APIs | `gcloud` | `gcloud auth login` (one-time, human) |
| [gh-kanban](./apps/gh-kanban/) | View a GitHub Projects v2 board as text | `gh` | `gh auth login` + `OWNER`/`PROJECT_NUMBER` |
| [appkit](./apps/appkit/) | Scaffold, validate, and learn to write String apps | none | none |
| [instatoon](./apps/instatoon/) | Multi-cut Instagram comic (인스타툰) — character → storyboard → cuts → 2×2 grid → bundle | `python3` + `pillow` | `$GEMINI_API_KEY` |

Every app has a `requirements.md` that spells out exactly what to install and how to authenticate. Agents should read it before running any action.

---

## Install

The easy way (from the StringHub marketplace):

```
/install https://stringhub.org/api/install/stringhub/<app-name>
```

For example:

```
/install https://stringhub.org/api/install/stringhub/translate
/open app:translate
/act.translate --text "Hello, world" --from en --to ko
```

The local way (cloning this repo and installing from disk):

```bash
git clone https://github.com/string-os/apps.git
cd apps
```

Then in your String session:

```
/install ./apps/translate
/open app:translate
```

Local install is useful when you want to fork an app, edit it, and try the change without going through publish.

---

## Anatomy of an app

Each app under `apps/<name>/` has at minimum:

```
apps/translate/
├── string.md          ← entry point — opens with /open app:translate
└── requirements.md    ← dependencies, auth, setup steps (read before use)
```

The setup doc must be named `requirements.md` (plural): the runtime auto-detects a sibling by that name and surfaces it (`Setup: /open requirements.md`) on a missing-env warning or an action error. For the hosted/marketplace path, also declare it explicitly with a `[!requirements](./requirements.md)` directive near the top of `string.md`.

Multi-page apps add more `.md` files alongside (and optionally a `nav/main.md`):

```
apps/github/
├── string.md
├── requirements.md
├── nav/main.md
├── repos.md
├── issues.md
├── prs.md
└── actions.md
```

For the SFMD format itself, see the [spec](https://github.com/string-os/string/tree/main/docs/sfmd).
For runtime semantics (how `/open`, `/act`, `/install` work), see the [runtime docs](https://github.com/string-os/string/tree/main/docs/runtime).

---

## Frontmatter conventions used here

```yaml
---
name: translate              # local registry key (after /install)
namespace: stringhub         # publisher — collision detection identity
version: 1.0.0
type: app                    # or "tool" — decides app: vs tool: lookup
description: ...
tags: [...]
default: <action-id>         # auto-runs on /open, /refresh, /back — only if it takes no required args (optional)
requires: [NOTION_TOKEN]     # required env vars — runtime warns "[!] Missing required env" if unset (optional)
env:                         # human-readable descriptions of those vars; documentation only (optional)
  - name: NOTION_TOKEN
    description: ...
---
```

`(namespace, name)` is the canonical identity. Two apps that share `name` but differ in `namespace` install side-by-side; the same `(namespace, name)` re-installs in place.

Note: only `requires:` triggers the missing-env warning. An `env:` block alone is descriptive and does **not** surface a warning — list the var in `requires:` too if it's mandatory.

---

## Contributing a new app

1. Make a directory under `apps/<name>/` with a `string.md` and `requirements.md`.
2. Set `namespace` to your own publisher handle (not `stringhub`) and pick a `name`.
3. Test locally: `/install ./apps/<name>` then run every action.
4. Open a PR. We'll review for: dependencies clearly stated, every action returns useful output, no destructive operations without explicit user confirmation.

If your app needs human-driven OAuth (browser login), `requirements.md` MUST tell the AI to ask the human to run the login command — agents can't complete OAuth flows themselves.

---

## License

MIT. See [LICENSE](./LICENSE).
