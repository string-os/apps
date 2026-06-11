---
title: Agent Message Requirements
---

# Requirements

This app posts text to a local String webhook URL.

Command: `curl`

## Setup

1. Make sure the target agent exists:

```bash
string agent list
```

2. If needed, add the target agent:

```bash
string agent add leo --home /home/ubuntu/crew/leo
```

3. Get the target agent's webhook URL:

```bash
string --agent leo event webhook show
```

4. Create one config per frequent target:

```
/open app:agent-message:leo
/set $WEBHOOK_URL = "http://127.0.0.1:3923/webhook/wh_..."
/act.send "Please check your event inbox."
```

One-off webhook:

```
/open app:agent-message
/act.send "Please check your event inbox." --webhook_url "http://127.0.0.1:3923/webhook/wh_..."
```

## Notes

- The target webhook must belong to an agent registered in the same local String daemon.
- The webhook URL is also the token. If the target rotates it, update this app config.
- The message is stored as text. String does not execute it as a command.
- Claude Code receives it live only when that agent is connected through the
  String MCP/channel integration.
