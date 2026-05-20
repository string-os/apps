# Requirements

## Environment Variables

| Variable        | Required | Description              | How to obtain                                                  |
|-----------------|----------|--------------------------|----------------------------------------------------------------|
| `$NOTION_TOKEN` | Yes      | Notion integration token | [notion.so/my-integrations](https://www.notion.so/my-integrations) |

## Setup (one-time, ~3 minutes)

### 1. Create a Notion integration

1. Visit <https://www.notion.so/my-integrations>
2. **+ New integration** → name it (e.g. "String"), type **Internal**
3. **Capabilities** — pick what you need:
   - `Read content` — required for `/act.search`, `/act.read`, `/act.query_db`, `/act.get_db`
   - `Insert content` — for `/act.create`, `/act.append`
   - `Update content` — for `/act.rename`
   - `Read comments` — for `/act.comments`
   - `Insert comments` — for `/act.comment`
4. **Save** → **Show** the Internal Integration Secret. Token starts with `ntn_...` (new) or `secret_...` (legacy).

### 2. Store the token in String

```
/set $NOTION_TOKEN = "ntn_..."
```

Persists in the user's global env (`config.json`), survives daemon restarts, available to every topic.

### 3. **Share each target page or database with the integration**

The token alone gives nothing — you must also share each page or database with the integration:

1. Open the page or database in Notion
2. `•••` (top right) → **Connections** → **Add connections**
3. Pick your integration
4. Confirm

Sub-pages inherit access — share your top-level "Workspace" or "Personal" page once and every sub-page is reachable. Same for databases: sharing the database itself lets `/act.query_db` see it. **Sharing the page that *contains* a database is not enough — share the database directly.**

## Verification

```
/act.search --query "anything"
```

- Wrong token → action prints `Error 401 unauthorized: ...`
- Token OK but nothing shared → empty results (share at least one page/database)

## Notes

- Tokens are workspace-scoped — one token = one Notion workspace.
- For multiple workspaces, set per-config env: `/set $NOTION_TOKEN = "..."` inside an `app:notion:work` topic stores it under that config only.
- Notion's permission model is opt-in. The integration only sees what's explicitly shared.
