# Requirements

| Package | Used by | Install                                                              |
|---------|---------|----------------------------------------------------------------------|
| `gh`    | all     | `brew install gh` / `apt install gh` / `winget install GitHub.cli`   |

## Authentication

`gh` uses OAuth — no API key needed. One-time setup:

```bash
gh auth login
gh auth status     # verify
```

Repo arguments use `owner/repo` format. Search queries follow [GitHub search syntax](https://docs.github.com/en/search-github/searching-on-github).
