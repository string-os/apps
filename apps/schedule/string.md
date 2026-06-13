---
name: schedule
namespace: stringhub
version: 0.1.0
description: Schedule recurring webhook pings to local String agents via OS cron.
tags: [schedule, cron, webhook, agent, local]
type: app
---

[!requirements](./requirements.md)

# Schedule

Durable, session-proof scheduling for String agents. Each schedule is an OS `cron`
entry that POSTs a message to a target agent's local webhook. Because it lives in the
system crontab, it keeps firing even when no Claude Code session is open — the message
lands in the agent's event inbox and is delivered live the next time that agent is
connected through the String channel.

The target agent's webhook URL is resolved automatically by id, so you never paste it.

Add a daily 09:00 KST briefing trigger (09:00 KST = 00:00 UTC):

```
/act.add --agent leo --cron "0 0 * * *" --message "Time for the morning briefing."
```

List what's scheduled:

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
- The target must be an agent registered in the same local daemon (it needs a webhook).
- The message is delivered as a pending String event, not executed as a command.
- Keep messages simple text. A single quote inside the message will break the shell
  line; escape or avoid it for now.

```act.add
CLI CRON={cron}; MSG={message}; AGENT={agent}; URL=$(string --agent "$AGENT" event webhook show 2>/dev/null | grep -Eo 'https?://[^[:space:]]+' | head -1); if [ -z "$URL" ]; then echo "No webhook found for agent '$AGENT'. Is it registered in this daemon?"; exit 1; fi; ID="sch_$(date +%s)"; LINE="$CRON curl -sS -X POST -H 'Content-Type: text/plain' --data-binary \"$MSG\" \"$URL\" >/dev/null 2>&1 # string-schedule:$ID agent=$AGENT"; ( crontab -l 2>/dev/null; printf '%s\n' "$LINE" ) | crontab - && printf 'Scheduled %s\n  when: %s (UTC)\n  agent: %s\n  message: %s\n' "$ID" "$CRON" "$AGENT" "$MSG"
  agent: string (required) "Target agent id whose webhook receives the message"
  cron: string (required) "Cron expression in UTC, e.g. '0 0 * * *' for daily 09:00 KST"
  message: string (required) "Text delivered to the agent on each fire"
```

```act.add.response
{Response.body}

next: /act.list to confirm, or /act.remove --id <id> to undo.
```

```act.list
CLI crontab -l 2>/dev/null | grep 'string-schedule:' || echo "(no schedules)"
```

```act.list.response
Current schedules:

{Response.body}
```

```act.remove
CLI ID={id}; if crontab -l 2>/dev/null | grep -q "string-schedule:$ID"; then crontab -l 2>/dev/null | grep -v "string-schedule:$ID" | crontab - && echo "Removed $ID"; else echo "No schedule with id $ID"; fi
  id: string (required) "Schedule id (sch_...) shown by /act.list"
```

```act.remove.response
{Response.body}
```
