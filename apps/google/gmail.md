[!nav:main](./nav/main.md)

# Gmail

Read, search, and send email via Gmail API. All actions use `gcloud auth print-access-token` — if you see `Need OAuth`, ask the human to follow `requirements.md`.

## Actions

- `/act.inbox [--limit 10]` — recent inbox messages with subject, from, date, snippet, id
- `/act.read_email --id <message-id>` — full message body (plain text)
- `/act.search_email --query <gmail-search-syntax> [--limit 10]` — search inbox (e.g. `from:boss@x.com is:unread`)
- `/act.send --to <email> --subject <text> --body <text>` — send a plain-text email

```act.inbox
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — ask the human to run: gcloud auth login --update-adc --scopes=https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/calendar" && exit 1; curl -s -H "Authorization: Bearer $TOKEN" "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:inbox&maxResults={limit}" | T="$TOKEN" python3 -c "import json,sys,urllib.request,os; t=os.environ['T']; ids=[m['id'] for m in json.load(sys.stdin).get('messages',[])]; [print(f'### {h.get(\"Subject\",\"(no subject)\")}\n- **From:** {h.get(\"From\",\"?\")}\n- **Date:** {h.get(\"Date\",\"\")}\n- **ID:** {mid}\n- **Snippet:** {m.get(\"snippet\",\"\")[:160]}\n') for mid in ids for m in [json.loads(urllib.request.urlopen(urllib.request.Request(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{mid}?format=metadata&metadataHeaders=Subject&metadataHeaders=From&metadataHeaders=Date', headers={'Authorization':'Bearer '+t})).read())] for h in [{x['name']:x['value'] for x in m.get('payload',{}).get('headers',[])}]] or print('Inbox empty.')"
  limit: number (optional) "Max messages" = "10"
```

```act.read_email
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; curl -s -H "Authorization: Bearer $TOKEN" "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format=full" | python3 -c "import json,sys,base64; m=json.load(sys.stdin); h={x['name']:x['value'] for x in m.get('payload',{}).get('headers',[])}; pl=m.get('payload',{}); flat=[pl]+[c for p in pl.get('parts',[]) for c in [p]+p.get('parts',[])]; texts=[base64.urlsafe_b64decode(p['body']['data']).decode('utf-8','replace') for p in flat if p.get('mimeType','').startswith('text/plain') and p.get('body',{}).get('data')]; body=''.join(texts) or m.get('snippet','(no body)'); print('## '+h.get('Subject','(no subject)')+'\n'); print('**From:** '+h.get('From','?')); print('**To:** '+h.get('To','?')); print('**Date:** '+h.get('Date','')); print(); print(body[:5000])"
  id: string (required) "Message ID (from inbox listing)"
```

```act.search_email
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; Q={query}; N={limit}; curl -s -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$Q" --data-urlencode "maxResults=$N" -G "https://gmail.googleapis.com/gmail/v1/users/me/messages" | T="$TOKEN" python3 -c "import json,sys,urllib.request,os; t=os.environ['T']; ids=[m['id'] for m in json.load(sys.stdin).get('messages',[])]; print(f'## Search results: {len(ids)}\n') if ids else print('No matches.'); [print(f'### {h.get(\"Subject\",\"(no subject)\")}\n- **From:** {h.get(\"From\",\"?\")}\n- **ID:** {mid}\n- **Snippet:** {m.get(\"snippet\",\"\")[:160]}\n') for mid in ids for m in [json.loads(urllib.request.urlopen(urllib.request.Request(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{mid}?format=metadata&metadataHeaders=Subject&metadataHeaders=From', headers={'Authorization':'Bearer '+t})).read())] for h in [{x['name']:x['value'] for x in m.get('payload',{}).get('headers',[])}]]"
  query: string (required) "Gmail search query (same syntax as Gmail search bar)"
  limit: number (optional) "Max results" = "10"
```

```act.send
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; TO={to} SUBJ={subject} BODY={body} python3 -c "import json,os,base64; raw=base64.urlsafe_b64encode(('To: '+os.environ['TO']+'\nSubject: '+os.environ['SUBJ']+'\nContent-Type: text/plain; charset=UTF-8\n\n'+os.environ['BODY']).encode('utf-8')).decode(); print(json.dumps({'raw':raw}))" | curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data-binary @- "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" | python3 -c "import json,sys; r=json.load(sys.stdin); print('Sent. Message ID: '+r['id']) if 'id' in r else print('Error: '+json.dumps(r))"
  to: string (required) "Recipient email"
  subject: string (required) "Email subject"
  body: string (required) "Email body"
```
