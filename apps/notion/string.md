---
name: notion
namespace: stringhub
version: 1.1.0
description: Notion client for String. Search, read, write, comment on Notion pages; query and inspect databases.
tags: [notion, notes, database, productivity, wiki]
type: app
requires: [NOTION_TOKEN]
env:
  - name: NOTION_TOKEN
    description: Notion integration token (from notion.so/my-integrations)
---

[!requirements](./requirements.md)

# Notion

Search, read, write, and comment on Notion pages; query and inspect databases. Requires `$NOTION_TOKEN` (Notion integration token) — see `requirements.md` for setup.

## Actions

- `/act.search --query <text> [--limit 10]` — search across pages and databases shared with the integration
- `/act.read --page_id <id>` — read a page's content (paragraphs, headings, list items, quotes, callouts, todos, toggles)
- `/act.create --parent_page_id <id> --title <text>` — create a new page **under another page** (database row creation requires schema-aware properties — not supported here)
- `/act.append --page_id <id> --content <text>` — append a paragraph block to an existing page
- `/act.rename --page_id <id> --title <text>` — rename a page (only works for pages whose title property is named `title`; database rows with custom title property names are not supported)
- `/act.query_db --database_id <id> [--limit 20]` — list rows from a database (the parent must be a database, not a page)
- `/act.get_db --database_id <id>` — retrieve a database's schema (property names + types)
- `/act.comment --page_id <id> --content <text>` — post a comment on a page (requires `Insert content` capability)
- `/act.comments --page_id <id>` — list existing comments on a page

```act.search
CLI Q={query} LIMIT={limit} python3 -c "import json,os,sys; sys.stdout.write(json.dumps({'query':os.environ['Q'],'page_size':int(os.environ['LIMIT'])}))" | curl -s -X POST https://api.notion.com/v1/search -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" --data-binary @- | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; rs=d.get('results',[]); _t=lambda r: (''.join(p.get('plain_text','') for p in (r.get('title',[]) if r.get('object')=='database' else next((v.get('title',[]) for v in r.get('properties',{}).values() if v.get('type')=='title'),[])))) or 'Untitled'; print('No results found.') if not rs else [(print('### '+_t(r)), print('- **Type:** '+r.get('object','')+' | **ID:** '+r.get('id','')), print('- **URL:** '+r.get('url','')), print()) for r in rs]"
  query: string (required) "Search query"
  limit: number (optional) "Max results" = "10"
```

```act.read
CLI curl -s https://api.notion.com/v1/blocks/{page_id}/children?page_size=100 -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; bs=d.get('results',[]); _txt=lambda b: ' '.join(t.get('plain_text','') for t in b.get(b.get('type',''),{}).get('rich_text',[])); print('(empty page)') if not bs else [print(_txt(b) or '') for b in bs if b.get('type') in ('paragraph','heading_1','heading_2','heading_3','bulleted_list_item','numbered_list_item','quote','to_do','toggle','callout')]"
  page_id: string (required) "Page ID (from search results)"
```

```act.create
CLI PARENT={parent_page_id} TITLE={title} python3 -c "import json,os,sys; sys.stdout.write(json.dumps({'parent':{'page_id':os.environ['PARENT']},'properties':{'title':{'title':[{'text':{'content':os.environ['TITLE']}}]}}}))" | curl -s -X POST https://api.notion.com/v1/pages -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" --data-binary @- | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; print('Created: '+d.get('url','(no url)')+((' (id: '+d['id']+')') if d.get('id') else ''))"
  parent_page_id: string (required) "Parent page ID (must be a page, not a database)"
  title: string (required) "Page title"
```

```act.append
CLI CONTENT={content} python3 -c "import json,os,sys; sys.stdout.write(json.dumps({'children':[{'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':os.environ['CONTENT']}}]}}]}))" | curl -s -X PATCH https://api.notion.com/v1/blocks/{page_id}/children -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" --data-binary @- | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; r=d.get('results',[]); print('Appended '+str(len(r))+' block(s).')"
  page_id: string (required) "Page ID to append to"
  content: string (required) "Paragraph text"
```

```act.rename
CLI TITLE={title} python3 -c "import json,os,sys; sys.stdout.write(json.dumps({'properties':{'title':{'title':[{'text':{'content':os.environ['TITLE']}}]}}}))" | curl -s -X PATCH https://api.notion.com/v1/pages/{page_id} -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" --data-binary @- | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; print('Renamed: '+d.get('url','(no url)'))"
  page_id: string (required) "Page ID"
  title: string (required) "New page title"
```

```act.query_db
CLI LIMIT={limit} python3 -c "import json,os,sys; sys.stdout.write(json.dumps({'page_size':int(os.environ['LIMIT'])}))" | curl -s -X POST https://api.notion.com/v1/databases/{database_id}/query -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" --data-binary @- | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')+'  (Hint: --database_id must be a database, not a page. /act.search results show Type: database for valid IDs.)'), sys.exit(1)) if d.get('object')=='error' else None; rs=d.get('results',[]); _t=lambda r: (''.join(p.get('plain_text','') for p in next((v.get('title',[]) for v in r.get('properties',{}).values() if v.get('type')=='title'),[]))) or '(untitled)'; print('No rows.') if not rs else [print('- '+_t(r)+'  \`'+r.get('id','')+'\`') for r in rs]"
  database_id: string (required) "Database ID"
  limit: number (optional) "Max results" = "20"
```

```act.get_db
CLI curl -s https://api.notion.com/v1/databases/{database_id} -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')+'  (Hint: --database_id must be a database, not a page. /act.search results show Type: database for valid IDs.)'), sys.exit(1)) if d.get('object')=='error' else None; ti=d.get('title',[]); t=(''.join(p.get('plain_text','') for p in ti)) or 'Untitled'; props=d.get('properties',{}); print('## '+t); print(); print('- **ID:** '+d.get('id','')); print('- **URL:** '+d.get('url','')); print(); print('| Property | Type |'); print('|----------|------|'); [print('| '+name+' | '+p.get('type','?')+' |') for name,p in props.items()]"
  database_id: string (required) "Database ID"
```

```act.comment
CLI PAGE={page_id} CONTENT={content} python3 -c "import json,os,sys; sys.stdout.write(json.dumps({'parent':{'page_id':os.environ['PAGE']},'rich_text':[{'text':{'content':os.environ['CONTENT']}}]}))" | curl -s -X POST https://api.notion.com/v1/comments -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" --data-binary @- | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; print('Commented on page '+d.get('parent',{}).get('page_id','?'))"
  page_id: string (required) "Page ID to comment on"
  content: string (required) "Comment text"
```

```act.comments
CLI curl -s "https://api.notion.com/v1/comments?block_id={page_id}" -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); (print('Error '+str(d.get('status',''))+' '+d.get('code','')+': '+d.get('message','')), sys.exit(1)) if d.get('object')=='error' else None; rs=d.get('results',[]); _txt=lambda c: ' '.join(t.get('plain_text','') for t in c.get('rich_text',[])); print('No comments yet.') if not rs else [print('- '+_txt(c)+'  _('+c.get('created_time','?')+')_') for c in rs]"
  page_id: string (required) "Page ID to read comments from"
```
