---
name: github
namespace: stringhub
version: 1.0.1
description: GitHub client for String. Issues, PRs, repos, actions, and notifications via gh CLI.
tags: [devtools, github, issues, pull-requests, repos, actions, developer-tools]
type: app
---

[!requirements](./requirements.md)

[!nav:main](./nav/main.md)

# GitHub

Manage your GitHub workflow without leaving String. Issues, pull requests, repos, CI/CD, notifications — all via [`gh` CLI](https://cli.github.com). Requires `gh auth login` once — see `requirements.md`.

## Pages

- `@main.issues` — list / view / create / close / comment / search issues
- `@main.prs` — list / view / create / merge / diff / review pull requests
- `@main.repos` — list / view / create repos, branches, commits, file tree
- `@main.actions` — workflows, runs, logs, re-runs

## Actions (this page — across-repo overviews)

- `/act.my_issues` — your open issues across all repos
- `/act.my_prs` — your open pull requests across all repos
- `/act.notifications` — unread notifications

```act.my_issues
CLI gh search issues --assignee @me --state open --limit 20 --json repository,number,title,updatedAt --template '{{range .}}### {{.repository.nameWithOwner}}#{{.number}}: {{.title}}{{"\n"}}- **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
```

```act.my_prs
CLI gh search prs --author @me --state open --limit 20 --json repository,number,title,updatedAt --template '{{range .}}### {{.repository.nameWithOwner}}#{{.number}}: {{.title}}{{"\n"}}- **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
```

```act.notifications
CLI gh api notifications --jq '.[] | "### \(.subject.title)\n- **Repo:** \(.repository.full_name)\n- **Type:** \(.subject.type)\n- **Reason:** \(.reason)\n- **Updated:** \(.updated_at)\n"' 2>/dev/null || echo "No unread notifications."
```
