---
name: notion
namespace: stringhub
version: 1.0.0
description: Notion client for String. Search pages, read content, create pages, and query databases.
tags: [notion, notes, database, productivity, wiki]
type: app
env:
  - name: NOTION_TOKEN
    description: Notion integration token (from notion.so/my-integrations)
---

# Notion

Search, read, and create Notion pages. Query databases and manage your workspace.

> **Setup:** Create an integration at [notion.so/my-integrations](https://www.notion.so/my-integrations), then:
> `/set $NOTION_TOKEN = "ntn_..."`

---

## Search

`/act.search --query "meeting notes"`

```act.search
CLI curl -s -X POST https://api.notion.com/v1/search -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" -d "{\"query\":\"{query}\",\"page_size\":{limit}}" | python3 -c "import json,sys;d=json.loads(sys.stdin.read());[(print('### '+((r.get('properties',{}).get('title',{}).get('title',[{}]) or [{}])[0].get('plain_text','Untitled'))),print('- **Type:** '+r.get('object','')+' | **ID:** '+r.get('id','')),print('- **URL:** '+r.get('url','')),print()) for r in d.get('results',[])] if d.get('results') else print('No results found.')"
  query: string (required) "Search query"
  limit: number (optional) "Max results" = "10"
```

---

## Read Page

`/act.read --page_id "PAGE_ID"`

```act.read
CLI curl -s https://api.notion.com/v1/blocks/{page_id}/children?page_size=100 -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" | python3 -c "import json,sys;d=json.loads(sys.stdin.read());[print((' '.join(t.get('plain_text','') for t in b.get(b['type'],{}).get('rich_text',[]))) or '') for b in d.get('results',[]) if b.get('type') in ('paragraph','heading_1','heading_2','heading_3','bulleted_list_item','numbered_list_item')]"
  page_id: string (required) "Page ID (from search results)"
```

---

## Create Page

`/act.create --parent_id "PAGE_ID" --title "New Page"`

```act.create
CLI curl -s -X POST https://api.notion.com/v1/pages -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" -d "{\"parent\":{\"page_id\":\"{parent_id}\"},\"properties\":{\"title\":{\"title\":[{\"text\":{\"content\":\"{title}\"}}]}}}" | python3 -c "import json,sys;d=json.loads(sys.stdin.read());print('Created: '+d.get('url','failed'))"
  parent_id: string (required) "Parent page or database ID"
  title: string (required) "Page title"
```

---

## Query Database

`/act.query_db --database_id "DB_ID"`

```act.query_db
CLI curl -s -X POST https://api.notion.com/v1/databases/{database_id}/query -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" -d "{\"page_size\":{limit}}" | python3 -c "import json,sys;d=json.loads(sys.stdin.read());[print('- '+str(next((v['title'][0]['plain_text'] for v in r.get('properties',{}).values() if v.get('type')=='title' and v.get('title')),r.get('id','?')))) for r in d.get('results',[])]"
  database_id: string (required) "Database ID"
  limit: number (optional) "Max results" = "20"
```

---

## Tips

- Get your token at [notion.so/my-integrations](https://www.notion.so/my-integrations)
- Share pages/databases with your integration for access
- Page IDs: copy from Notion URL (32-char hex after the page name)
