---
name: schedule
namespace: stringhub
version: 0.1.1
description: Schedule recurring webhook pings to yourself via OS cron.
tags: [schedule, cron, webhook, agent, local]
type: app
---

[!requirements](./requirements.md)

# Schedule

Durable, session-proof scheduling for the current agent. Each schedule is an OS `cron`
entry that POSTs a message to **your own** local webhook. Because it lives in the system
crontab, it keeps firing even when no Claude Code session is open — the message lands in
your event inbox and is delivered live the next time you are connected through the String
channel.

You only ever schedule, list, and remove your own entries; the current agent's webhook is
resolved automatically, so there is no agent to specify.

Add a daily 09:00 KST briefing trigger (09:00 KST = 00:00 UTC):

```
/act.add --cron "0 0 * * *" --message "Time for the morning briefing."
```

List your schedules:

```
/act.list
```

Remove one by id:

```
/act.remove --id sch_1750000000
```

## Notes

- **Times are UTC** (the server's clock). KST = UTC + 9, so KST 09:00 → `0 0 * * *`,
  KST 12:00 → `0 3 * * *`, KST 15:00 → `0 6 * * *`, KST 18:00 → `0 9 * * *`.
- Cron format: `minute hour day-of-month month day-of-week`.
- Each schedule is tagged with your agent id; `/act.list` and `/act.remove` only ever
  touch your own entries, never another agent's.
- The message is delivered as a pending String event, not executed as a command.
- Keep messages simple text. A single quote inside the message will break the shell
  line; escape or avoid it for now.

```act.add
CLI WH=$(string event webhook show 2>/dev/null); URL=$(printf '%s' "$WH" | grep -Eo 'https?://[^[:space:]]+' | head -1); ME=$(printf '%s' "$WH" | sed -nE "s/.*agent '([^']+)'.*/\1/p" | head -1); if [ -z "$URL" ] || [ -z "$ME" ]; then echo "Could not resolve current agent's webhook. Is the daemon running?"; exit 1; fi; CRON={cron}; MSG={message}; ID="sch_$(date +%s)"; LINE="$CRON curl -sS -X POST -H 'Content-Type: text/plain' --data-binary \"$MSG\" \"$URL\" >/dev/null 2>&1 # string-schedule:$ID agent=$ME"; ( crontab -l 2>/dev/null; printf '%s\n' "$LINE" ) | crontab - && printf 'Scheduled %s for %s\n  when: %s (UTC)\n  message: %s\n' "$ID" "$ME" "$CRON" "$MSG"
  cron: string (required) "Cron expression in UTC, e.g. '0 0 * * *' for daily 09:00 KST"
  message: string (required) "Text delivered to you on each fire"
```

```act.add.response
{Response.body}

next: /act.list to confirm, or /act.remove --id <id> to undo.
```

```act.list
CLI ME=$(string event webhook show 2>/dev/null | sed -nE "s/.*agent '([^']+)'.*/\1/p" | head -1); crontab -l 2>/dev/null | grep "string-schedule:.* agent=$ME" || echo "(no schedules for $ME)"
```

```act.list.response
Your schedules:

{Response.body}
```

```act.remove
CLI ME=$(string event webhook show 2>/dev/null | sed -nE "s/.*agent '([^']+)'.*/\1/p" | head -1); ID={id}; if crontab -l 2>/dev/null | grep -q "string-schedule:$ID agent=$ME"; then crontab -l 2>/dev/null | grep -v "string-schedule:$ID agent=$ME" | crontab - && echo "Removed $ID"; else echo "No schedule '$ID' owned by $ME"; fi
  id: string (required) "Schedule id (sch_...) shown by /act.list"
```

```act.remove.response
{Response.body}
```
