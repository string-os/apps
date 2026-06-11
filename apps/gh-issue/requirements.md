# gh-issue — Requirements

## System dependencies

| Tool | Why | Install |
|---|---|---|
| `gh` | GitHub CLI for issue search, read, and triage actions | [cli.github.com](https://cli.github.com) |

## Authentication

`gh` uses OAuth. Run this once outside the agent if needed:

```bash
gh auth login
```

Verify:

```bash
gh auth status
```

## Configure the repo

Set the repository once for this app session:

```
/set $REPO = "owner/repo"
```

Issue aliases carry the repo with the issue number:

```
@issue-1 = (string-os/string, 42)
```

You can still use app configs to keep separate sessions per repo:

```
string app:gh-issue:h1r '/set $REPO = "H1R-AI/stringhub-web"'
string app:gh-issue:string '/set $REPO = "string-os/string"'
```

For one repo, prefer the base app topic:

```
string app:gh-issue '/set $REPO = "string-os/string"'
string app:gh-issue '/act.repo'
```

## Notes

- This app intentionally uses only the `gh` CLI. No helper script.
- Mutating actions are limited to comment, label, and assign.
- Issue aliases like `@issue-1` carry both repo and issue number.
- Search uses the configured `$REPO` plus `gh search issues --repo`.

