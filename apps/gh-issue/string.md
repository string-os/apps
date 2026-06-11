---
name: gh-issue
namespace: stringhub
version: 0.1.0
description: Triage GitHub issues through a small agent-friendly String surface using only the gh CLI.
tags: [devtools, github, issues, triage, developer-tools]
type: app
requires: [REPO]
---

# GitHub Issue Triage

Triage GitHub issues without browsing GitHub like a human. The agent learns one
small surface: list or search issues, read the issue, then comment, label, or
assign it.

```
/open app:gh-issue
/act.repo
/act.search bug
/act.read @issue-1
/act.comment @issue-1 "I reproduced this. Next step: add a failing test."
/act.label @issue-1 "needs-repro"
```

Setup: [requirements.md](./requirements.md)

```act.repo
CLI gh search issues --repo $REPO --state {state} --limit {limit} --sort updated --json repository,number,title,state,labels,assignees,updatedAt,url
  state, -s: string (optional) "open|closed" = "open"
  limit, -l: number (optional) "Max issues" = "20"
```

```act.repo.response
# Issues

for: i in Response.body
{@issue} = ({i.repository.nameWithOwner}, {i.number})
- {@issue} {i.repository.nameWithOwner}#{i.number}: {i.title} — {i.state}, updated {i.updatedAt}
end:

next: /act.read @issue-N · /act.comment @issue-N "..." · /act.label @issue-N "..."
```

```act.search
CLI gh search issues "{query}" --repo $REPO --state {state} --limit {limit} --json repository,number,title,state,labels,assignees,updatedAt,url
  query, -q: string (required) "Search terms"
  state, -s: string (optional) "open|closed" = "open"
  limit, -l: number (optional) "Max issues" = "20"
```

```act.search.response
# Issue search

Query: {query} · State: {state}

for: i in Response.body
{@issue} = ({i.repository.nameWithOwner}, {i.number})
- {@issue} {i.repository.nameWithOwner}#{i.number}: {i.title} — {i.state}, updated {i.updatedAt}
end:

next: /act.read @issue-N · /act.comment @issue-N "..." · /act.label @issue-N "..."
```

```act.mine
CLI gh search issues --assignee @me --state open --limit {limit} --json repository,number,title,state,labels,assignees,updatedAt,url
  limit, -l: number (optional) "Max issues" = "20"
```

```act.mine.response
# My open issues

for: i in Response.body
{@issue} = ({i.repository.nameWithOwner}, {i.number})
- {@issue} {i.repository.nameWithOwner}#{i.number}: {i.title} — updated {i.updatedAt}
end:

next: /act.read @issue-N · /act.comment @issue-N "..." · /act.label @issue-N "..."
```

```act.read
CLI gh issue view {issue[1]} --repo {issue[0]} --json number,title,body,state,labels,assignees,comments,updatedAt,url,author
  issue, -i: tuple (required) "@issue-N from repo/search/mine"
```

```act.read.response
# {issue[0]}#{Response.body.number}: {Response.body.title}

State: {Response.body.state} · Updated: {Response.body.updatedAt}
Author: {Response.body.author.login}
URL: {Response.body.url}

Labels:
for: l in Response.body.labels
- {l.name}
end:

Assignees:
for: a in Response.body.assignees
- {a.login}
end:

## Body

{Response.body.body}

## Comments

for: c in Response.body.comments
- {c.author.login} ({c.createdAt}): {c.body}
end:

next: /act.comment @issue-N "..." · /act.label @issue-N "..." · /act.assign @issue-N <user> · /act.repo
```

```act.comment
CLI gh issue comment {issue[1]} --repo {issue[0]} --body "{body}"
  issue, -i: tuple (required) "@issue-N from repo/search/mine"
  body, -b: string (required) "Comment body"
```

```act.comment.response
Commented on {issue[0]}#{issue[1]}.

{Response.body}

next: /act.read @issue-N · /act.repo
```

```act.label
CLI gh issue edit {issue[1]} --repo {issue[0]} --add-label "{label}"
  issue, -i: tuple (required) "@issue-N from repo/search/mine"
  label, -l: string (required) "Label to add"
```

```act.label.response
Added label "{label}" to {issue[0]}#{issue[1]}.

next: /act.read @issue-N · /act.repo
```

```act.assign
CLI gh issue edit {issue[1]} --repo {issue[0]} --add-assignee "{user}"
  issue, -i: tuple (required) "@issue-N from repo/search/mine"
  user, -u: string (required) "GitHub username"
```

```act.assign.response
Assigned {issue[0]}#{issue[1]} to {user}.

next: /act.read @issue-N · /act.repo
```
