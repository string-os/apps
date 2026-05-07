[!nav:main](./nav/main.md)

# Issues

Create, search, and manage GitHub issues.

---

## List Issues

`/act.list_issues --repo "owner/repo"`

```act.list_issues
CLI gh issue list --repo {repo} --state {state} --limit {limit} --json number,title,state,labels,assignees,createdAt --template '{{range .}}### #{{.number}}: {{.title}}{{"\n"}}- **State:** {{.state}}{{"\n"}}- **Labels:** {{range .labels}}{{.name}} {{end}}{{"\n"}}- **Assignees:** {{range .assignees}}{{.login}} {{end}}{{"\n"}}- **Created:** {{.createdAt}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
  state: string (optional) "open|closed|all" = "open"
  limit: number (optional) "Max results" = "20"
```

---

## View Issue

`/act.view_issue --repo "owner/repo" --number 42`

```act.view_issue
CLI gh issue view {number} --repo {repo} --json number,title,body,state,labels,assignees,comments --template '# #{{.number}}: {{.title}}{{"\n\n"}}**State:** {{.state}}{{"\n"}}**Labels:** {{range .labels}}{{.name}} {{end}}{{"\n"}}**Assignees:** {{range .assignees}}{{.login}} {{end}}{{"\n\n"}}---{{"\n\n"}}{{.body}}{{"\n\n"}}---{{"\n\n"}}## Comments ({{len .comments}}){{"\n\n"}}{{range .comments}}**{{.author.login}}** ({{.createdAt}}):{{"\n"}}{{.body}}{{"\n\n"}}---{{"\n\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
  number: number (required) "Issue number"
```

---

## Create Issue

`/act.create_issue --repo "owner/repo" --title "Bug: login fails"`

```act.create_issue
CLI gh issue create --repo {repo} --title "{title}" --body "{body}"
  repo: string (required) "Repository (e.g. owner/repo)"
  title: string (required) "Issue title"
  body: string (optional) "Issue body (markdown)" = ""
```

---

## Close Issue

`/act.close_issue --repo "owner/repo" --number 42`

```act.close_issue
CLI gh issue close {number} --repo {repo} --comment "{comment}"
  repo: string (required) "Repository"
  number: number (required) "Issue number"
  comment: string (optional) "Close comment" = "Closed."
```

---

## Add Comment

`/act.comment_issue --repo "owner/repo" --number 42 --body "Fixed in v2.1"`

```act.comment_issue
CLI gh issue comment {number} --repo {repo} --body "{body}"
  repo: string (required) "Repository"
  number: number (required) "Issue number"
  body: string (required) "Comment text"
```

---

## Search Issues

`/act.search_issues --query "is:open label:bug repo:owner/repo"`

```act.search_issues
CLI gh search issues "{query}" --limit {limit} --json repository,number,title,state,updatedAt --template '{{range .}}### {{.repository.nameWithOwner}}#{{.number}}: {{.title}}{{"\n"}}- **State:** {{.state}} · **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
  query: string (required) "GitHub search query"
  limit: number (optional) "Max results" = "20"
```
