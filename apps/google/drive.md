[!nav:main](./nav/main.md)

# Drive

List, search, and download Google Drive files. All actions use `gcloud auth print-access-token` — if you see `Need OAuth`, ask the human to follow `requirements.md`. Native Google Docs/Sheets/Slides cannot be downloaded directly via `alt=media` — open them in browser via the `Link` field instead.

## Actions

- `/act.files [--limit 10]` — recent files (name, type, modified, id, link)
- `/act.search_drive --query <text> [--limit 10]` — search by file name (full [Drive query syntax](https://developers.google.com/drive/api/guides/search-files) supported)
- `/act.download_file --file_id <id> [--output /tmp/drive-download]` — download a file by ID

```act.files
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — ask the human to run: gcloud auth login --update-adc --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/calendar" && exit 1; curl -s -G -H "Authorization: Bearer $TOKEN" --data-urlencode "pageSize={limit}" --data-urlencode "orderBy=modifiedTime desc" --data-urlencode "fields=files(id,name,mimeType,modifiedTime,size,webViewLink)" "https://www.googleapis.com/drive/v3/files" | python3 -c "import json,sys; data=json.load(sys.stdin); files=data.get('files',[]); print(f'## Recent files ({len(files)})\n') if files else print('No files.'); [print(f'### {f[\"name\"]}\n- **Type:** {f.get(\"mimeType\",\"?\")}\n- **Modified:** {f.get(\"modifiedTime\",\"?\")[:10]}\n- **Size:** {f.get(\"size\",\"-\")}\n- **ID:** {f[\"id\"]}\n- **Link:** {f.get(\"webViewLink\",\"-\")}\n') for f in files]"
  limit: number (optional) "Max results" = "10"
```

```act.search_drive
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; Q={query}; N={limit}; curl -s -G -H "Authorization: Bearer $TOKEN" --data-urlencode "q=name contains '$Q' and trashed=false" --data-urlencode "pageSize=$N" --data-urlencode "fields=files(id,name,mimeType,modifiedTime,webViewLink)" "https://www.googleapis.com/drive/v3/files" | python3 -c "import json,sys; data=json.load(sys.stdin); files=data.get('files',[]); print(f'## Search: {len(files)} match(es)\n') if files else print('No matches.'); [print(f'### {f[\"name\"]}\n- **Type:** {f.get(\"mimeType\",\"?\")}\n- **Modified:** {f.get(\"modifiedTime\",\"?\")[:10]}\n- **ID:** {f[\"id\"]}\n- **Link:** {f.get(\"webViewLink\",\"-\")}\n') for f in files]"
  query: string (required) "File name contains"
  limit: number (optional) "Max results" = "10"
```

```act.download_file
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; O={output}; HTTP=$(curl -s -o "$O" -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"); if [ "$HTTP" = "200" ]; then echo "Downloaded to $O ($(wc -c < "$O") bytes)"; else echo "HTTP $HTTP — check file ID and permissions"; head -c 300 "$O" 2>/dev/null; fi
  file_id: string (required) "Google Drive file ID"
  output: string (optional) "Local save path" = "/tmp/drive-download"
```
