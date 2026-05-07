# Requirements

## System Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `gh` | GitHub CLI | [cli.github.com](https://cli.github.com) — `brew install gh` / `apt install gh` / `winget install GitHub.cli` |

## Authentication

`gh` uses OAuth — no API key needed. One-time setup:

```
gh auth login
```

Follow the browser prompt to authorize. Token is stored locally.

**Verify:** `gh auth status` should show your username.

## Notes

- All commands use `gh` CLI with `--json` + `--template` for clean output
- Repo arguments use `owner/repo` format (e.g. `H1R-AI/stringhub-web`)
- Search queries follow [GitHub search syntax](https://docs.github.com/en/search-github/searching-on-github)
