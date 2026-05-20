[!nav:main](./nav/main.md)

# Pull Requests

Create, review, and manage pull requests.

## Actions

- `/act.list_prs --repo <owner/repo> [--state open|closed|merged|all] [--limit 20]` — list PRs
- `/act.view_pr --repo <owner/repo> --number <n>` — view a PR with diff stats and comments
- `/act.create_pr --repo <owner/repo> --title <text> --head <branch> [--body <md>] [--base main]` — create a new PR
- `/act.merge_pr --repo <owner/repo> --number <n> [--method merge|squash|rebase]` — merge and delete branch
- `/act.pr_diff --repo <owner/repo> --number <n>` — show the raw diff
- `/act.review_pr --repo <owner/repo> --number <n> --body <text> --event approve|request-changes|comment` — submit a review

```act.list_prs
CLI gh pr list --repo {repo} --state {state} --limit {limit} --json number,title,state,headRefName,author,reviewDecision,additions,deletions,updatedAt --template '{{range .}}### #{{.number}}: {{.title}}{{"\n"}}- **Branch:** {{.headRefName}} · **Author:** {{.author.login}}{{"\n"}}- **Review:** {{.reviewDecision}} · **+{{.additions}} -{{.deletions}}**{{"\n"}}- **Updated:** {{.updatedAt}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
  state: string (optional) "open|closed|merged|all" = "open"
  limit: number (optional) "Max results" = "20"
```

```act.view_pr
CLI gh pr view {number} --repo {repo} --json number,title,body,state,headRefName,baseRefName,author,reviewDecision,additions,deletions,files,comments --template '# PR #{{.number}}: {{.title}}{{"\n\n"}}**{{.headRefName}} → {{.baseRefName}}** · {{.state}}{{"\n"}}**Author:** {{.author.login}} · **Review:** {{.reviewDecision}}{{"\n"}}**Changes:** +{{.additions}} -{{.deletions}} ({{len .files}} files){{"\n\n"}}---{{"\n\n"}}{{.body}}{{"\n\n"}}---{{"\n\n"}}## Changed Files{{"\n\n"}}{{range .files}}- `{{.path}}` (+{{.additions}} -{{.deletions}}){{"\n"}}{{end}}{{"\n"}}## Comments ({{len .comments}}){{"\n\n"}}{{range .comments}}**{{.author.login}}** ({{.createdAt}}):{{"\n"}}{{.body}}{{"\n\n"}}---{{"\n\n"}}{{end}}'
  repo: string (required) "Repository"
  number: number (required) "PR number"
```

```act.create_pr
CLI gh pr create --repo {repo} --title "{title}" --body "{body}" --head {head} --base {base}
  repo: string (required) "Repository"
  title: string (required) "PR title"
  body: string (optional) "PR description" = ""
  head: string (required) "Source branch"
  base: string (optional) "Target branch" = "main"
```

```act.merge_pr
CLI gh pr merge {number} --repo {repo} --{method} --delete-branch
  repo: string (required) "Repository"
  number: number (required) "PR number"
  method: string (optional) "merge|squash|rebase" = "squash"
```

```act.pr_diff
CLI gh pr diff {number} --repo {repo}
  repo: string (required) "Repository"
  number: number (required) "PR number"
```

```act.review_pr
CLI gh pr review {number} --repo {repo} --body "{body}" --{event}
  repo: string (required) "Repository"
  number: number (required) "PR number"
  body: string (required) "Review comment"
  event: string (required) "approve|request-changes|comment"
```
