---
name: github
namespace: stringhub
version: 1.0.0
description: GitHub client for String. Issues, PRs, repos, actions, and notifications via gh CLI.
tags: [devtools, github, issues, pull-requests, repos, actions, developer-tools]
type: app
---

[!nav:main](./nav/main.md)

# GitHub

Manage your GitHub workflow without leaving String. Issues, pull requests, repos, CI/CD, and notifications — all via `gh` CLI.

> **Setup:** See [Requirements][@main.requirement] for `gh` installation and auth.

---

## Quick Actions

`/act.my_issues` — your open issues across all repos
`/act.my_prs` — your open pull requests
`/act.notifications` — unread notifications

---

## My Open Issues (across all repos)

```act.my_issues
CLI gh search issues --assignee @me --state open --limit 20 --json repository,number,title,updatedAt --template '{{range .}}### {{.repository.nameWithOwner}}#{{.number}}: {{.title}}{{"\n"}}- **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
```

## My Open PRs (across all repos)

```act.my_prs
CLI gh search prs --author @me --state open --limit 20 --json repository,number,title,updatedAt --template '{{range .}}### {{.repository.nameWithOwner}}#{{.number}}: {{.title}}{{"\n"}}- **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
```

## Notifications

```act.notifications
CLI gh api notifications --jq '.[] | "### \(.subject.title)\n- **Repo:** \(.repository.full_name)\n- **Type:** \(.subject.type)\n- **Reason:** \(.reason)\n- **Updated:** \(.updated_at)\n"' 2>/dev/null || echo "No unread notifications."
```
