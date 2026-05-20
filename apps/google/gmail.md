[!nav:main](./nav/main.md)

# Gmail

Read, search, and send email via Gmail API. All actions use `gcloud auth print-access-token` — if you see `Need OAuth`, ask the human to follow `requirements.md`.

## Actions

- `/act.inbox [--limit 10]` — recent inbox messages with subject, from, date, snippet, id
- `/act.read_email --id <message-id>` — full message body (plain text)
- `/act.search_email --query <gmail-search-syntax> [--limit 10]` — search inbox (e.g. `from:boss@x.com is:unread`)
- `/act.send --to <email> --subject <text> --body <text>` — send a plain-text email

```act.inbox
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — ask the human to run: gcloud auth login --update-adc --scopes=https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/calendar" && exit 1; curl -s -H "Authorization: Bearer $TOKEN" "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:inbox&maxResults={limit}" | python3 -c "import json,sys,urllib.request,os; t=os.environ['T']; ids=[m['id'] for m in json.load(sys.stdin).get('messages',[])]; [print(f'### {h.get(\"Subject\",\"(no subject)\")}\n- **From:** {h.get(\"From\",\"?\")}\n- **Date:** {h.get(\"Date\",\"\")}\n- **ID:** {mid}\n- **Snippet:** {m.get(\"snippet\",\"\")[:160]}\n') for mid in ids for m in [json.loads(urllib.request.urlopen(urllib.request.Request(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{mid}?format=metadata&metadataHeaders=Subject&metadataHeaders=From&metadataHeaders=Date', headers={'Authorization':'Bearer '+t})).read())] for h in [{x['name']:x['value'] for x in m.get('payload',{}).get('headers',[])}]] or print('Inbox empty.')" T="$TOKEN"
  limit: number (optional) "Max messages" = "10"
```

```act.read_email
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; curl -s -H "Authorization: Bearer $TOKEN" "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format=full" | python3 -c "import json,sys,base64; m=json.load(sys.stdin); h={x['name']:x['value'] for x in m.get('payload',{}).get('headers',[])}; print(f'## {h.get(\"Subject\",\"(no subject)\")}\n'); print(f'**From:** {h.get(\"From\",\"?\")}'); print(f'**To:** {h.get(\"To\",\"?\")}'); print(f'**Date:** {h.get(\"Date\",\"\")}'); print(); body=''; p=m.get('payload',{});\nimport re\ndef walk(part):\n    global body\n    if part.get('mimeType','').startswith('text/plain') and part.get('body',{}).get('data'):\n        body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8','replace')\n    for child in part.get('parts',[]): walk(child)\nwalk(p)\nif not body and p.get('body',{}).get('data'): body = base64.urlsafe_b64decode(p['body']['data']).decode('utf-8','replace')\nprint(body[:5000] if body else m.get('snippet','(no body)'))"
  id: string (required) "Message ID (from inbox listing)"
```

```act.search_email
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; curl -s -H "Authorization: Bearer $TOKEN" --data-urlencode "q={query}" --data-urlencode "maxResults={limit}" -G "https://gmail.googleapis.com/gmail/v1/users/me/messages" | python3 -c "import json,sys,urllib.request,os; t=os.environ['T']; ids=[m['id'] for m in json.load(sys.stdin).get('messages',[])]; print(f'## Search results: {len(ids)}\n') if ids else print('No matches.'); [print(f'### {h.get(\"Subject\",\"(no subject)\")}\n- **From:** {h.get(\"From\",\"?\")}\n- **ID:** {mid}\n- **Snippet:** {m.get(\"snippet\",\"\")[:160]}\n') for mid in ids for m in [json.loads(urllib.request.urlopen(urllib.request.Request(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{mid}?format=metadata&metadataHeaders=Subject&metadataHeaders=From', headers={'Authorization':'Bearer '+t})).read())] for h in [{x['name']:x['value'] for x in m.get('payload',{}).get('headers',[])}]]" T="$TOKEN"
  query: string (required) "Gmail search query (same syntax as Gmail search bar)"
  limit: number (optional) "Max results" = "10"
```

```act.send
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; RAW=$(printf 'To: %s\nSubject: %s\nContent-Type: text/plain; charset=UTF-8\n\n%s' "{to}" "{subject}" "{body}" | base64 -w0 | tr '+/' '-_' | tr -d '='); curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"raw\":\"$RAW\"}" "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" | python3 -c "import json,sys; r=json.load(sys.stdin); print(f'✓ Sent. Message ID: {r[\"id\"]}') if 'id' in r else print(f'✗ Error: {r}')"
  to: string (required) "Recipient email"
  subject: string (required) "Email subject"
  body: string (required) "Email body"
```
