---
title: Schedule Requirements
---

# Requirements

This app registers OS cron jobs that POST to the current agent's local webhook URL.

Command: crontab

## Also used

- `curl` — sends the scheduled POST to your webhook on each fire.
- `string` — resolves the current agent's webhook URL (`string event webhook show`).

## Setup

No agent to configure — the app schedules to the current agent automatically.

```
/open app:schedule
/act.add --cron "0 0 * * *" --message "Time for the morning briefing."
/act.list
/act.remove --id sch_1750000000
```

Times are UTC (KST = UTC + 9).

## Notes

- The schedule lives in the user's crontab, so it survives session restarts.
- Each fire POSTs to your webhook; the message becomes a pending String event.
- You receive it live only when connected through the String MCP/channel.
- Entries are tagged with your agent id; list/remove only touch your own.
- Removing the app does not remove already-registered cron entries — use `/act.remove`
  (or `crontab -e`) to clean those up.
