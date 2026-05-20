[!nav:main](./nav/main.md)

# Actions (CI/CD)

Monitor GitHub Actions workflows and runs.

## Actions

- `/act.workflows --repo <owner/repo>` — list workflows in a repo
- `/act.runs --repo <owner/repo> [--limit 10]` — recent workflow runs (status, branch, run_id)
- `/act.view_run --repo <owner/repo> --run_id <id>` — view a single run with per-job status
- `/act.run_logs --repo <owner/repo> --run_id <id>` — last 50 lines of run logs
- `/act.rerun --repo <owner/repo> --run_id <id>` — re-run failed jobs only

```act.workflows
CLI gh workflow list --repo {repo} --json name,state,id --template '{{range .}}### {{.name}}{{"\n"}}- **State:** {{.state}} · **ID:** {{.id}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository"
```

```act.runs
CLI gh run list --repo {repo} --limit {limit} --json databaseId,displayTitle,status,conclusion,headBranch,createdAt,updatedAt --template '{{range .}}### {{.displayTitle}}{{"\n"}}- **Status:** {{.status}} {{if .conclusion}}({{.conclusion}}){{end}}{{"\n"}}- **Branch:** {{.headBranch}}{{"\n"}}- **Run ID:** {{.databaseId}}{{"\n"}}- **Created:** {{.createdAt}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository"
  limit: number (optional) "Max results" = "10"
```

```act.view_run
CLI gh run view {run_id} --repo {repo} --json databaseId,displayTitle,status,conclusion,headBranch,jobs,createdAt,updatedAt --template '# Run: {{.displayTitle}}{{"\n\n"}}**Status:** {{.status}} {{if .conclusion}}({{.conclusion}}){{end}}{{"\n"}}**Branch:** {{.headBranch}}{{"\n"}}**Run ID:** {{.databaseId}}{{"\n"}}**Created:** {{.createdAt}}{{"\n\n"}}---{{"\n\n"}}## Jobs{{"\n\n"}}{{range .jobs}}- **{{.name}}**: {{.status}} {{if .conclusion}}({{.conclusion}}){{end}}{{"\n"}}{{end}}'
  repo: string (required) "Repository"
  run_id: number (required) "Run ID (from /act.runs)"
```

```act.run_logs
CLI gh run view {run_id} --repo {repo} --log 2>&1 | tail -50
  repo: string (required) "Repository"
  run_id: number (required) "Run ID"
```

```act.rerun
CLI gh run rerun {run_id} --repo {repo} --failed
  repo: string (required) "Repository"
  run_id: number (required) "Run ID"
```
