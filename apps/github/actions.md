[!nav:main](./nav/main.md)

# Actions (CI/CD)

Monitor GitHub Actions workflows and runs.

---

## List Workflows

`/act.workflows --repo "owner/repo"`

```act.workflows
CLI gh workflow list --repo {repo} --json name,state,id --template '{{range .}}### {{.name}}{{"\n"}}- **State:** {{.state}} · **ID:** {{.id}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository"
```

---

## Recent Runs

`/act.runs --repo "owner/repo"`

```act.runs
CLI gh run list --repo {repo} --limit {limit} --json databaseId,displayTitle,status,conclusion,headBranch,createdAt,updatedAt --template '{{range .}}### {{.displayTitle}}{{"\n"}}- **Status:** {{.status}} {{if .conclusion}}({{.conclusion}}){{end}}{{"\n"}}- **Branch:** {{.headBranch}}{{"\n"}}- **Run ID:** {{.databaseId}}{{"\n"}}- **Created:** {{.createdAt}}{{"\n\n"}}{{end}}'
  repo: string (required) "Repository"
  limit: number (optional) "Max results" = "10"
```

---

## View Run

`/act.view_run --repo "owner/repo" --run_id 123456`

```act.view_run
CLI gh run view {run_id} --repo {repo} --json databaseId,displayTitle,status,conclusion,headBranch,jobs,createdAt,updatedAt --template '# Run: {{.displayTitle}}{{"\n\n"}}**Status:** {{.status}} {{if .conclusion}}({{.conclusion}}){{end}}{{"\n"}}**Branch:** {{.headBranch}}{{"\n"}}**Run ID:** {{.databaseId}}{{"\n"}}**Created:** {{.createdAt}}{{"\n\n"}}---{{"\n\n"}}## Jobs{{"\n\n"}}{{range .jobs}}- **{{.name}}**: {{.status}} {{if .conclusion}}({{.conclusion}}){{end}}{{"\n"}}{{end}}'
  repo: string (required) "Repository"
  run_id: number (required) "Run ID (from /act.runs)"
```

---

## Run Logs

`/act.run_logs --repo "owner/repo" --run_id 123456`

```act.run_logs
CLI gh run view {run_id} --repo {repo} --log 2>&1 | tail -50
  repo: string (required) "Repository"
  run_id: number (required) "Run ID"
```

---

## Re-run Failed

`/act.rerun --repo "owner/repo" --run_id 123456`

```act.rerun
CLI gh run rerun {run_id} --repo {repo} --failed
  repo: string (required) "Repository"
  run_id: number (required) "Run ID"
```
