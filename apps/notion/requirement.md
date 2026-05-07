# Requirements

## Environment Variables

| Variable | Required | Description | How to obtain |
|----------|----------|-------------|---------------|
| `$NOTION_TOKEN` | Yes | Notion integration token | [notion.so/my-integrations](https://www.notion.so/my-integrations) |

## Setup (one-time, ~3 minutes)

### 1. Create a Notion integration

1. Visit <https://www.notion.so/my-integrations>
2. Click **+ New integration**
3. Name it (e.g. "String") — workspace defaults to your current one
4. Type: **Internal** (default)
5. **Capabilities:** at minimum check `Read content`. For `/act.create` also enable `Insert content`. For `/act.query_db` also enable `Read user information without email addresses`.
6. Click **Save**, then **Show** next to "Internal Integration Secret" — that's your token. Starts with `ntn_...` (new format) or `secret_...` (legacy).

### 2. Store the token in String

```
/set $NOTION_TOKEN = "ntn_..."
```

This persists in the user's global env (`config.json` env section) — it survives daemon restarts and is available to every topic.

### 3. **Share each target page or database with the integration**

This is the step that's easy to miss. **The token alone gives you nothing — you must also share each page/db with the integration:**

1. Open the page or database in Notion
2. Click `•••` (top right) → **Connections** → **Add connections**
3. Pick your integration (the name you chose in step 1)
4. Confirm

Pages inside a shared page inherit access. So for most users: share your top-level "Workspace" or "Personal" page once, then every sub-page is reachable.

## System Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `curl` | HTTP requests | Pre-installed on most systems |
| `python3` | JSON processing | Pre-installed on most systems |

## Verification

```
/act.search --query "anything"
```

If the token is wrong: `401 Unauthorized` from the API. If the token is right but no pages were shared: `200 OK` with empty results — share at least one page (step 3 above).

## Notes

- Tokens are workspace-scoped — one token = one Notion workspace.
- For multiple workspaces, set per-config env: `/set $NOTION_TOKEN = "..."` inside an `app:notion:work` topic stores it under that config only.
- The integration only sees pages explicitly shared with it. Notion's permission model is opt-in, not opt-out.
