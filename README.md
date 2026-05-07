# String Apps

A curated collection of production-grade SFMD apps for the [String](https://github.com/string-os/string) runtime. Each app is a self-contained markdown document (or directory) the agent installs once and uses through `/open` and `/act`.

This is the source repo. Apps published from here also appear in the [StringHub marketplace](https://stringhub.org) under the `stringhub` namespace.

---

## What's in this repo

| App | What it does | Key dependencies | Auth |
|---|---|---|---|
| [translate](./apps/translate/) | Translate text between languages (MyMemory API) | none | none |
| [websearch](./apps/websearch/) | Search Wikipedia, Hacker News, DuckDuckGo | `curl`, `python3` | none |
| [weather](./apps/weather/) | Current weather, forecast, city lookup (Open-Meteo) | none | none |
| [github](./apps/github/) | Issues, PRs, repos, notifications via `gh` CLI | `gh` | `gh auth login` (one-time, human) |
| [youtube](./apps/youtube/) | Video metadata + transcript via `yt-dlp` | `yt-dlp` | none |
| [humanizer](./apps/humanizer/) | Detect AI-writing patterns and suggest fixes | `python3` | none |
| [docx](./apps/docx/) | Word/PDF read/write, format conversion via `pandoc` | `pandoc` (+ optional `wkhtmltopdf`, `pdftotext`, `libreoffice`) | none |
| [whisper](./apps/whisper/) | Local speech-to-text with OpenAI Whisper | `whisper`, `ffmpeg` | none |
| [notion](./apps/notion/) | Search, read, create Notion pages and databases | `curl`, `python3` | `$NOTION_TOKEN` |

Every app has a `requirement.md` that spells out exactly what to install and how to authenticate. Agents should read it before running any action.

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
├── string.md         ← entry point — opens with /open app:translate
└── requirement.md    ← dependencies, auth, setup steps (read before use)
```

Multi-page apps add more `.md` files alongside (and optionally a `nav/main.md`):

```
apps/github/
├── string.md
├── requirement.md
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
default: <action-id>         # auto-runs on /open, /refresh, /back (optional)
env:                         # required environment variables (optional)
  - name: NOTION_TOKEN
    description: ...
---
```

`(namespace, name)` is the canonical identity. Two apps that share `name` but differ in `namespace` install side-by-side; the same `(namespace, name)` re-installs in place.

---

## Contributing a new app

1. Make a directory under `apps/<name>/` with a `string.md` and `requirement.md`.
2. Set `namespace` to your own publisher handle (not `stringhub`) and pick a `name`.
3. Test locally: `/install ./apps/<name>` then run every action.
4. Open a PR. We'll review for: dependencies clearly stated, every action returns useful output, no destructive operations without explicit user confirmation.

If your app needs human-driven OAuth (browser login), `requirement.md` MUST tell the AI to ask the human to run the login command — agents can't complete OAuth flows themselves.

---

## License

MIT. See [LICENSE](./LICENSE).
