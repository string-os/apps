---
title: gh-kanban — Requirements
---

# Requirements

## System dependencies

| Tool | Why | Install |
|---|---|---|
| `gh` | GitHub CLI | [cli.github.com](https://cli.github.com) |
| `jq` | JSON pivot for board grouping | `brew install jq` / `apt install jq` |
| `bash` | Multi-line action scripts | (system default on macOS/Linux) |

## Authentication

The default `gh auth login` does **not** include the `project` scope. Add it:

```bash
gh auth refresh -s project,read:project
```

Verify:

```bash
gh auth status            # should show your login
gh project list --owner <your-org-or-user>   # should list projects
```

## Configure the board

Set the project owner and number as session variables. These are read by
every action in this app.

```
/set $OWNER = "H1R-AI"
/set $PROJECT_NUMBER = "4"
```

`OWNER` is the org or user that owns the project. `PROJECT_NUMBER` is the
integer in the project URL: `https://github.com/orgs/H1R-AI/projects/4` →
`4`.

## Per-board configs (optional)

If you track multiple boards, use String app configs:

```
string app:gh-kanban:h1r '/set $OWNER = "H1R-AI"'
string app:gh-kanban:h1r '/set $PROJECT_NUMBER = "4"'

string app:gh-kanban:string '/set $OWNER = "string-os"'
string app:gh-kanban:string '/set $PROJECT_NUMBER = "1"'
```

Then open with `string app:gh-kanban:h1r` or `:string` to land on the
respective board.

## Verify

```
string app:gh-kanban
```

The default `/act.board` runs and renders the kanban as columns.
