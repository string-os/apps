---
title: Schedule Requirements
---

# Requirements

This app registers OS cron jobs that POST to a local String webhook URL.

Command: crontab

## Also used

- `curl` — sends the scheduled POST to the agent's webhook.
- `string` — resolves a target agent's webhook URL by id (`string --agent <id> event webhook show`).

## Setup

1. Make sure the target agent exists and has a webhook:

```bash
string agent list
string --agent leo event webhook show
```

2. Add a schedule (times are UTC; KST = UTC + 9):

```
/open app:schedule
/act.add --agent leo --cron "0 0 * * *" --message "Time for the morning briefing."
```

3. Confirm and manage:

```
/act.list
/act.remove --id sch_1750000000
```

## Notes

- The schedule lives in the user's crontab, so it survives session restarts.
- Each fire POSTs to the agent's webhook; the message becomes a pending String event.
- The agent receives it live only when connected through the String MCP/channel.
- Removing the app does not remove already-registered cron entries — use `/act.remove`
  (or `crontab -e`) to clean those up.
