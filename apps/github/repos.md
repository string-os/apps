[!nav:main](./nav/main.md)

# Repos

List, create, and inspect repositories.

---

## My Repos

`/act.my_repos --owner "H1R-AI"`

```act.my_repos
CLI gh repo list {owner} --limit {limit} --json nameWithOwner,description,isPrivate,stargazerCount,updatedAt --template '{{range .}}### {{.nameWithOwner}}{{if .isPrivate}} 🔒{{end}}{{"\n"}}{{if .description}}- {{.description}}{{"\n"}}{{end}}- ⭐ {{.stargazerCount}} · Updated: {{.updatedAt}}{{"\n\n"}}{{end}}'
  owner: string (optional) "User or org name (default: your account)"
  limit: number (optional) "Max results" = "20"
```

---

## View Repo

`/act.view_repo --repo "owner/repo"`

```act.view_repo
CLI gh repo view {repo} --json name,description,homepageUrl,isPrivate,stargazerCount,forkCount,openIssues,defaultBranchRef,languages,licenseInfo --template '# {{.name}}{{if .isPrivate}} 🔒{{end}}{{"\n\n"}}{{if .description}}> {{.description}}{{"\n\n"}}{{end}}{{if .homepageUrl}}**Homepage:** {{.homepageUrl}}{{"\n"}}{{end}}**Stars:** {{.stargazerCount}} · **Forks:** {{.forkCount}} · **Issues:** {{len .openIssues}}{{"\n"}}**Default branch:** {{.defaultBranchRef.name}}{{"\n"}}{{if .licenseInfo}}**License:** {{.licenseInfo.name}}{{"\n"}}{{end}}{{"\n"}}## Languages{{"\n\n"}}{{range .languages}}- {{.name}}{{"\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
```

---

## Create Repo

`/act.create_repo --name "my-project" --description "A cool project"`

```act.create_repo
CLI gh repo create {name} --{visibility} --description "{description}" --confirm
  name: string (required) "Repository name"
  description: string (optional) "Repository description" = ""
  visibility: string (optional) "public|private" = "private"
```

---

## List Branches

`/act.branches --repo "owner/repo"`

```act.branches
CLI gh api repos/{repo}/branches --jq '.[] | "- **\(.name)**\(if .protected then " 🔒" else "" end)"'
  repo: string (required) "Repository (e.g. owner/repo)"
```

---

## Recent Commits

`/act.commits --repo "owner/repo"`

```act.commits
CLI gh api repos/{repo}/commits?per_page={limit} --jq '.[] | "### \(.sha[:7]) \(.commit.message | split("\n") | .[0])\n- **Author:** \(.commit.author.name) · \(.commit.author.date)\n"'
  repo: string (required) "Repository"
  limit: number (optional) "Max results" = "10"
```

---

## Repo Files

`/act.tree --repo "owner/repo"`

```act.tree
CLI gh api repos/{repo}/git/trees/{branch}?recursive=1 --jq '.tree[] | select(.type=="blob") | "- \(.path) (\(.size // 0) bytes)"'
  repo: string (required) "Repository"
  branch: string (optional) "Branch name" = "main"
```
