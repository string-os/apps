[!nav:main](./nav/main.md)

# Calendar

Agenda, create / search / delete events. All actions use `gcloud auth print-access-token` — if you see `Need OAuth`, ask the human to follow `requirements.md`. Delete is by `event_id` only — get the ID from a listing first.

## Actions

- `/act.today` — today + tomorrow's events
- `/act.week` — events for the next 7 days
- `/act.agenda --start <YYYY-MM-DD> --end <YYYY-MM-DD>` — custom date range
- `/act.create_event --title <text> --when <YYYY-MM-DD HH:MM> --duration <minutes>` — create a timed event
- `/act.allday --title <text> --when <YYYY-MM-DD>` — create an all-day event
- `/act.search_cal --query <text> [--start today] [--end +180 days]` — search events by keyword
- `/act.delete_event --event_id <id>` — delete an event

```act.today
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — ask the human to run: gcloud auth login --update-adc --scopes=https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.modify" && exit 1; START=$(date -u -d 'today 00:00:00' +%Y-%m-%dT%H:%M:%SZ); END=$(date -u -d 'tomorrow 23:59:59' +%Y-%m-%dT%H:%M:%SZ); curl -s -G -H "Authorization: Bearer $TOKEN" --data-urlencode "timeMin=$START" --data-urlencode "timeMax=$END" --data-urlencode "singleEvents=true" --data-urlencode "orderBy=startTime" --data-urlencode "maxResults=50" "https://www.googleapis.com/calendar/v3/calendars/primary/events" | python3 -c "import json,sys; ev=json.load(sys.stdin).get('items',[]); print(f'## Today + tomorrow ({len(ev)} events)\n') if ev else print('No events scheduled.'); [print(f\"### {e.get('summary','(no title)')}\n- **When:** {e.get('start',{}).get('dateTime', e.get('start',{}).get('date',''))} → {e.get('end',{}).get('dateTime', e.get('end',{}).get('date',''))}\n- **Location:** {e.get('location','-')}\n- **ID:** {e.get('id','')}\n\") for e in ev]"
```

```act.week
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; START=$(date -u -d 'today 00:00:00' +%Y-%m-%dT%H:%M:%SZ); END=$(date -u -d '+7 days' +%Y-%m-%dT%H:%M:%SZ); curl -s -G -H "Authorization: Bearer $TOKEN" --data-urlencode "timeMin=$START" --data-urlencode "timeMax=$END" --data-urlencode "singleEvents=true" --data-urlencode "orderBy=startTime" --data-urlencode "maxResults=100" "https://www.googleapis.com/calendar/v3/calendars/primary/events" | python3 -c "import json,sys; ev=json.load(sys.stdin).get('items',[]); print(f'## Next 7 days ({len(ev)} events)\n') if ev else print('No events.'); [print(f\"### {e.get('summary','(no title)')}\n- **When:** {e.get('start',{}).get('dateTime', e.get('start',{}).get('date',''))} → {e.get('end',{}).get('dateTime', e.get('end',{}).get('date',''))}\n- **ID:** {e.get('id','')}\n\") for e in ev]"
```

```act.agenda
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; S={start}; E={end}; START=$(date -u -d "$S" +%Y-%m-%dT%H:%M:%SZ) || { echo "Invalid start date: $S"; exit 1; }; END=$(date -u -d "$E 23:59:59" +%Y-%m-%dT%H:%M:%SZ) || { echo "Invalid end date: $E"; exit 1; }; curl -s -G -H "Authorization: Bearer $TOKEN" --data-urlencode "timeMin=$START" --data-urlencode "timeMax=$END" --data-urlencode "singleEvents=true" --data-urlencode "orderBy=startTime" --data-urlencode "maxResults=250" "https://www.googleapis.com/calendar/v3/calendars/primary/events" | python3 -c "import json,sys; ev=json.load(sys.stdin).get('items',[]); print(f'## {len(ev)} events\n') if ev else print('No events in range.'); [print(f\"### {e.get('summary','(no title)')}\n- **When:** {e.get('start',{}).get('dateTime', e.get('start',{}).get('date',''))} → {e.get('end',{}).get('dateTime', e.get('end',{}).get('date',''))}\n- **Location:** {e.get('location','-')}\n- **ID:** {e.get('id','')}\n\") for e in ev]"
  start: string (required) "Start date (YYYY-MM-DD or 'today', 'tomorrow', '+1 day' etc.)"
  end: string (required) "End date (YYYY-MM-DD or relative)"
```

```act.create_event
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; TZ_NAME=$(timedatectl show -p Timezone --value 2>/dev/null || echo "UTC"); W={when}; DUR={duration}; SE=$(date -d "$W" +%s) || { echo "Invalid date: $W"; exit 1; }; START=$(date -d "@$SE" +%Y-%m-%dT%H:%M:%S); END=$(date -d "@$((SE + DUR*60))" +%Y-%m-%dT%H:%M:%S); TITLE={title} START=$START END=$END TZ_NAME=$TZ_NAME python3 -c "import json,os; print(json.dumps({'summary':os.environ['TITLE'],'start':{'dateTime':os.environ['START'],'timeZone':os.environ['TZ_NAME']},'end':{'dateTime':os.environ['END'],'timeZone':os.environ['TZ_NAME']}}))" | curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data-binary @- "https://www.googleapis.com/calendar/v3/calendars/primary/events" | python3 -c "import json,sys; r=json.load(sys.stdin); print('Created: '+r['summary']+'\n- **When:** '+r['start']['dateTime']+' → '+r['end']['dateTime']+'\n- **ID:** '+r['id']+'\n- **Link:** '+r.get('htmlLink','-')) if 'id' in r else print('Error: '+json.dumps(r))"
  title: string (required) "Event title"
  when: string (required) "Start time (e.g. 2026-05-08 14:00)"
  duration: number (required) "Duration in minutes"
```

```act.allday
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; W={when}; SE=$(date -d "$W" +%s) || { echo "Invalid date: $W"; exit 1; }; START=$(date -d "@$SE" +%Y-%m-%d); END=$(date -d "@$((SE + 86400))" +%Y-%m-%d); TITLE={title} START=$START END=$END python3 -c "import json,os; print(json.dumps({'summary':os.environ['TITLE'],'start':{'date':os.environ['START']},'end':{'date':os.environ['END']}}))" | curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data-binary @- "https://www.googleapis.com/calendar/v3/calendars/primary/events" | python3 -c "import json,sys; r=json.load(sys.stdin); print('Created (all-day): '+r['summary']+' on '+r['start']['date']+'\n- **ID:** '+r['id']) if 'id' in r else print('Error: '+json.dumps(r))"
  title: string (required) "Event title"
  when: string (required) "Date (YYYY-MM-DD)"
```

```act.search_cal
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; Q={query}; S={start}; E={end}; START=$(date -u -d "$S" +%Y-%m-%dT%H:%M:%SZ) || { echo "Invalid start: $S"; exit 1; }; END=$(date -u -d "$E" +%Y-%m-%dT%H:%M:%SZ) || { echo "Invalid end: $E"; exit 1; }; curl -s -G -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$Q" --data-urlencode "timeMin=$START" --data-urlencode "timeMax=$END" --data-urlencode "singleEvents=true" --data-urlencode "orderBy=startTime" "https://www.googleapis.com/calendar/v3/calendars/primary/events" | python3 -c "import json,sys; ev=json.load(sys.stdin).get('items',[]); print(f'## {len(ev)} match(es)\n') if ev else print('No matches.'); [print(f\"### {e.get('summary','(no title)')}\n- **When:** {e.get('start',{}).get('dateTime', e.get('start',{}).get('date',''))}\n- **ID:** {e.get('id','')}\n\") for e in ev]"
  query: string (required) "Search keyword"
  start: string (optional) "Window start" = "today"
  end: string (optional) "Window end" = "+180 days"
```

```act.delete_event
CLI TOKEN=$(gcloud auth print-access-token 2>/dev/null); [ -z "$TOKEN" ] && echo "Need OAuth — see /open requirements.md" && exit 1; HTTP=$(curl -s -o /tmp/cal-del.txt -w "%{http_code}" -X DELETE -H "Authorization: Bearer $TOKEN" "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event_id}"); if [ "$HTTP" = "204" ]; then echo "Deleted event {event_id}"; else echo "HTTP $HTTP"; cat /tmp/cal-del.txt; fi; rm -f /tmp/cal-del.txt
  event_id: string (required) "Event ID (from /act.today, /act.search_cal, etc.)"
```
