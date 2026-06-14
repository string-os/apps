---
name: gh-kanban
namespace: stringhub
version: 0.1.0
description: Operate a GitHub Projects v2 kanban board as an agent-friendly text surface.
tags: [devtools, github, projects, kanban, productivity]
type: app
default: board
requires: [OWNER, PROJECT_NUMBER]
---

# GitHub Kanban

Operate a GitHub Projects v2 board as an agent-friendly text surface. Each
card becomes a named tuple shortcut `@card-N` carrying both issue number and
repo, so mutations take a single argument without re-copying GitHub URLs.

```
/open app:gh-kanban                    # see board (default)
/act.add -r owner/repo -t "Task" -l ai:jordan      # create + assign a card
/act.board --status "In progress"      # filter by status
/act.card @card-1                      # drill into a card
/act.move @card-1 Ready                # change status
/act.comment @card-1 "ship"            # add a comment
/act.columns                           # valid Status values
/act.close @card-1 --confirm yes       # close the issue
/act.refresh                           # re-fetch board
```

Full signatures: `/act.<name> --help`.

[!requirements](./requirements.md)

```act.board
CLI ./kanban board $OWNER $PROJECT_NUMBER "{status}" {limit}
  status, -s: string (optional) "Only show cards with this Status, or all" = "all"
  limit, -l: number (optional) "Max cards per column" = "50"
```

```act.board.response
# GitHub Kanban — {Response.body.owner} / Project {Response.body.project}

Filter: {Response.body.filter} · Total {Response.body.total} · Limit per column {Response.body.limit_per_column}

Summary: Backlog {Response.body.summary.backlog} · Todo {Response.body.summary.todo} · Ready {Response.body.summary.ready} · In progress {Response.body.summary.in_progress} · In review {Response.body.summary.in_review} · Done {Response.body.summary.done} · Other {Response.body.summary.other}

## Backlog

for: it in Response.body.backlog
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Todo

for: it in Response.body.todo
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Ready

for: it in Response.body.ready
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## In progress

for: it in Response.body.in_progress
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## In review

for: it in Response.body.in_review
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Done

for: it in Response.body.done
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Other

for: it in Response.body.other
{@card} = ({it.number}, {it.repo})
- {@card} [{it.status}] {it.title}
end:

next: /act.card @card-N  ·  /act.move @card-N <status>  ·  /act.comment @card-N "..."  ·  /act.columns  ·  /act.refresh
```

```act.refresh
CLI ./kanban board $OWNER $PROJECT_NUMBER all 50
```

```act.refresh.response
# GitHub Kanban — {Response.body.owner} / Project {Response.body.project}

Summary: Backlog {Response.body.summary.backlog} · Todo {Response.body.summary.todo} · Ready {Response.body.summary.ready} · In progress {Response.body.summary.in_progress} · In review {Response.body.summary.in_review} · Done {Response.body.summary.done} · Other {Response.body.summary.other}

## Backlog

for: it in Response.body.backlog
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Todo

for: it in Response.body.todo
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Ready

for: it in Response.body.ready
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## In progress

for: it in Response.body.in_progress
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## In review

for: it in Response.body.in_review
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Done

for: it in Response.body.done
{@card} = ({it.number}, {it.repo})
- {@card} {it.title}
end:

## Other

for: it in Response.body.other
{@card} = ({it.number}, {it.repo})
- {@card} [{it.status}] {it.title}
end:

next: /act.card @card-N  ·  /act.move @card-N <status>  ·  /act.comment @card-N "..."  ·  /act.columns
```

```act.columns
CLI ./kanban columns $OWNER $PROJECT_NUMBER
```

```act.columns.response
# Status columns

for: it in Response.body.statuses
- {it.name}
end:

next: /act.board --status "<status>"  ·  /act.move @card-N <status>
```

```act.card
CLI ./kanban card {card[0]} {card[1]}
  card, -c: tuple (required) "Card ref @card-N from board"
```

```act.card.response
# {Response.body.repo}#{Response.body.number}: {Response.body.title}

State: {Response.body.state} · Updated: {Response.body.updatedAt}
Author: {Response.body.author}
Assignees: {Response.body.assignees}
Labels: {Response.body.labels}
URL: {Response.body.url}

## Body

{Response.body.body}

## Recent comments

for: c in Response.body.comments
- {c.author} ({c.createdAt}): {c.body}
end:

next: /act.move @card-N <status>  ·  /act.comment @card-N "..."  ·  /act.close @card-N --confirm yes  ·  /act.refresh
```

```act.move
CLI ./kanban move $OWNER $PROJECT_NUMBER {card[0]} {card[1]} "{to}"
  card, -c: tuple (required) "Card ref @card-N from board"
  to, -t:   string (required) "Target Status option name"
```

```act.move.response
Moved {Response.body.repo}#{Response.body.number}: {Response.body.title}

{Response.body.from} -> {Response.body.to}

next: /act.refresh
```

```act.comment
CLI gh issue comment {card[0]} --repo {card[1]} --body "{body}"
  card, -c: tuple (required) "Card ref @card-N from board"
  body, -b: string (required) "Comment body"
```

```act.comment.response
Comment added.

{Response.body}

next: /act.card @card-N  ·  /act.refresh
```

```act.close
CLI ./kanban close {card[0]} {card[1]} {confirm}
  card, -c: tuple (required) "Card ref @card-N from board"
  confirm: string (optional) "Must be yes to close the issue" = "no"
```

```act.close.response
{Response.body}
```

```act.add
CLI ./kanban add $OWNER $PROJECT_NUMBER {repo} {title} {body} {bodyfile} {labels}
  repo, -r:     string (required) "owner/repo for the new issue"
  title, -t:    string (required) "Card title"
  body, -b:     string "Single-line body (use --bodyfile for multiline specs)" = ""
  bodyfile, -f: string "Path to a multiline body file (preferred for task specs; preserves newlines)" = ""
  labels, -l:   string "Comma-separated labels, e.g. ai:jordan" = ""
```

```act.add.response
{Response.body}

next: /act.refresh  ·  /act.move @card-N "In progress"
```
