[!nav:main](./nav/main.md)

# Issues

Create, search, and manage GitHub issues.

## Actions

- `/act.list_issues --repo <owner/repo> [--state open|closed|all] [--limit 20]` — list issues in a repo
- `/act.view_issue --repo <owner/repo> --number <n>` — view an issue with body and comments
- `/act.create_issue --repo <owner/repo> --title <text> [--body <markdown>]` — create a new issue
- `/act.close_issue --repo <owner/repo> --number <n> [--comment <text>]` — close an issue with optional comment
- `/act.comment_issue --repo <owner/repo> --number <n> --body <text>` — add a comment to an issue
- `/act.search_issues --query <github-search-syntax> [--limit 20]` — cross-repo search (e.g. `is:open label:bug repo:owner/repo`)

```act.list_issues
CLI gh issue list --repo {repo} --state {state} --limit {limit} --json number,title,state,labels,assignees,createdAt --template '{{range .}}### #{{.number}}: {{.title}}{{"\n"}}- **State:** {{.state}}{{"\n"}}- **Labels:** {{range .labels}}{{.name}} {{end}}{{"\n"}}- **Assignees:** {{range .assignees}}{{.login}} {{end}}{{"\n"}}- **Created:** {{.createdAt}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
  state: string (optional) "open|closed|all" = "open"
  limit: number (optional) "Max results" = "20"
```

```act.view_issue
CLI gh issue view {number} --repo {repo} --json number,title,body,state,labels,assignees,comments --template '# #{{.number}}: {{.title}}{{"\n\n"}}**State:** {{.state}}{{"\n"}}**Labels:** {{range .labels}}{{.name}} {{end}}{{"\n"}}**Assignees:** {{range .assignees}}{{.login}} {{end}}{{"\n\n"}}---{{"\n\n"}}{{.body}}{{"\n\n"}}---{{"\n\n"}}## Comments ({{len .comments}}){{"\n\n"}}{{range .comments}}**{{.author.login}}** ({{.createdAt}}):{{"\n"}}{{.body}}{{"\n\n"}}---{{"\n\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
  number: number (required) "Issue number"
```

```act.create_issue
CLI gh issue create --repo {repo} --title "{title}" --body "{body}"
  repo: string (required) "Repository (e.g. owner/repo)"
  title: string (required) "Issue title"
  body: string (optional) "Issue body (markdown)" = ""
```

```act.close_issue
CLI gh issue close {number} --repo {repo} --comment "{comment}"
  repo: string (required) "Repository"
  number: number (required) "Issue number"
  comment: string (optional) "Close comment" = "Closed."
```

```act.comment_issue
CLI gh issue comment {number} --repo {repo} --body "{body}"
  repo: string (required) "Repository"
  number: number (required) "Issue number"
  body: string (required) "Comment text"
```

```act.search_issues
CLI gh search issues "{query}" --limit {limit} --json repository,number,title,state,updatedAt --template '{{range .}}### {{.repository.nameWithOwner}}#{{.number}}: {{.title}}{{"\n"}}- **State:** {{.state}} · **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
  query: string (required) "GitHub search query"
  limit: number (optional) "Max results" = "20"
```
