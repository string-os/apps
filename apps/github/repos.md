[!nav:main](./nav/main.md)

# Repos

List, create, and inspect repositories.

## Actions

- `/act.my_repos [--owner <user-or-org>] [--limit 20]` — list repos owned by you or another user/org
- `/act.view_repo --repo <owner/repo>` — repo metadata: stars, forks, license, languages, default branch
- `/act.create_repo --name <text> [--description <text>] [--visibility public|private]` — create a new repo
- `/act.branches --repo <owner/repo>` — list branches (protected branches marked 🔒)
- `/act.commits --repo <owner/repo> [--limit 10]` — recent commits with sha, author, message
- `/act.tree --repo <owner/repo> [--branch main]` — recursive file tree with sizes

```act.my_repos
CLI gh repo list {owner} --limit {limit} --json nameWithOwner,description,isPrivate,stargazerCount,updatedAt --template '{{range .}}### {{.nameWithOwner}}{{if .isPrivate}} 🔒{{end}}{{"\n"}}{{if .description}}- {{.description}}{{"\n"}}{{end}}- ⭐ {{.stargazerCount}} · Updated: {{.updatedAt}}{{"\n\n"}}{{end}}'
  owner: string (optional) "User or org name (default: your account)"
  limit: number (optional) "Max results" = "20"
```

```act.view_repo
CLI gh repo view {repo} --json name,description,homepageUrl,isPrivate,stargazerCount,forkCount,openIssues,defaultBranchRef,languages,licenseInfo --template '# {{.name}}{{if .isPrivate}} 🔒{{end}}{{"\n\n"}}{{if .description}}> {{.description}}{{"\n\n"}}{{end}}{{if .homepageUrl}}**Homepage:** {{.homepageUrl}}{{"\n"}}{{end}}**Stars:** {{.stargazerCount}} · **Forks:** {{.forkCount}} · **Issues:** {{len .openIssues}}{{"\n"}}**Default branch:** {{.defaultBranchRef.name}}{{"\n"}}{{if .licenseInfo}}**License:** {{.licenseInfo.name}}{{"\n"}}{{end}}{{"\n"}}## Languages{{"\n\n"}}{{range .languages}}- {{.name}}{{"\n"}}{{end}}'
  repo: string (required) "Repository (e.g. owner/repo)"
```

```act.create_repo
CLI gh repo create {name} --{visibility} --description "{description}" --confirm
  name: string (required) "Repository name"
  description: string (optional) "Repository description" = ""
  visibility: string (optional) "public|private" = "private"
```

```act.branches
CLI gh api repos/{repo}/branches --jq '.[] | "- **\(.name)**\(if .protected then " 🔒" else "" end)"'
  repo: string (required) "Repository (e.g. owner/repo)"
```

```act.commits
CLI gh api repos/{repo}/commits?per_page={limit} --jq '.[] | "### \(.sha[:7]) \(.commit.message | split("\n") | .[0])\n- **Author:** \(.commit.author.name) · \(.commit.author.date)\n"'
  repo: string (required) "Repository"
  limit: number (optional) "Max results" = "10"
```

```act.tree
CLI gh api repos/{repo}/git/trees/{branch}?recursive=1 --jq '.tree[] | select(.type=="blob") | "- \(.path) (\(.size // 0) bytes)"'
  repo: string (required) "Repository"
  branch: string (optional) "Branch name" = "main"
```
