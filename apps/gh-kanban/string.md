---
name: gh-kanban
namespace: stringhub
version: 0.1.0
description: View and use a GitHub Projects v2 kanban board as text. Open the app, see the board.
tags: [devtools, github, projects, kanban, productivity]
type: app
default: board
requires: [OWNER, PROJECT_NUMBER]
---

# GitHub Kanban

Read and operate a GitHub Projects v2 board as text. Each card becomes a
named tuple shortcut `@card-N` carrying both issue number and repo, so
mutations take a single argument.

```
/open app:gh-kanban           # see board (default)
/act.card @card-1             # drill into a card
/act.move @card-1 Ready       # change status
/act.comment @card-1 "ship"   # add a comment
/act.close @card-1            # close the issue
/act.refresh                  # re-fetch board
```

Full signatures: `/act.<name> --help`.

[!requirements](./requirements.md)

```act.board
CLI gh project item-list $PROJECT_NUMBER --owner $OWNER --format json --limit 200 --jq '. as $r | ["Backlog","Todo","Ready","In progress","In Progress","Doing","In review","In Review","Done"] as $order | {total: ($r.items | length), items: ($r.items | sort_by(.status // "" | . as $s | ($order | index($s)) // 99) | map({number: (.content.number // null), repo: (.content.repository // ""), status: (.status // "(none)"), title: .title}))}'
```

```act.board.response
# {Response.body.total} items

for: it in Response.body.items
{@card} = ({it.number}, {it.repo})
- {@card} [{it.status}]: {it.title}
end:

next: /act.card @card-N  ·  /act.move @card-N <status>  ·  /act.comment @card-N "..."  ·  /act.refresh
```

```act.refresh
CLI gh project item-list $PROJECT_NUMBER --owner $OWNER --format json --limit 200 --jq '. as $r | ["Backlog","Todo","Ready","In progress","In Progress","Doing","In review","In Review","Done"] as $order | {total: ($r.items | length), items: ($r.items | sort_by(.status // "" | . as $s | ($order | index($s)) // 99) | map({number: (.content.number // null), repo: (.content.repository // ""), status: (.status // "(none)"), title: .title}))}'
```

```act.refresh.response
# {Response.body.total} items

for: it in Response.body.items
{@card} = ({it.number}, {it.repo})
- {@card} [{it.status}]: {it.title}
end:
```

```act.card
CLI gh issue view {card[0]} --repo {card[1]} --comments
  card, -c: tuple (required) "Card ref @card-N from board"
```

```act.card.response
{Response.body}

next: /act.move @card-N <status>  ·  /act.comment @card-N "..."  ·  /act.close @card-N  ·  /act.refresh
```

```act.move
CLI ./kanban move $OWNER $PROJECT_NUMBER {card[0]} {to}
  card, -c: tuple (required) "Card ref @card-N from board"
  to, -t:   string (required) "Target Status option name"
```

```act.move.response
{Response.body}

next: /act.refresh
```

```act.comment
CLI gh issue comment {card[0]} --repo {card[1]} --body "{body}"
  card, -c: tuple (required) "Card ref @card-N from board"
  body, -b: string (required) "Comment body"
```

```act.comment.response
{Response.body}
```

```act.close
CLI gh issue close {card[0]} --repo {card[1]}
  card, -c: tuple (required) "Card ref @card-N from board"
```

```act.close.response
{Response.body}
```
