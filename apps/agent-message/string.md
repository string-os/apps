---
name: agent-message
namespace: stringhub
version: 0.1.0
description: Send text events between local String agents.
tags: [agent, message, event, webhook, local]
type: app
requires:
  - WEBHOOK_URL
---

[!requirements](./requirements.md)

# Agent Message

A tiny local messenger for String agents.

Point a config at one agent:

```
/open app:agent-message:leo
/set $WEBHOOK_URL = "http://127.0.0.1:3923/webhook/wh_..."
```

Then send:

```
/act.send "Review PR #31 when you are free."
```

One-off:

```
/act.send "Build finished. Please inspect the logs." --webhook_url "http://127.0.0.1:3923/webhook/wh_..."
```

Messages become pending String events. They are not executed as commands.

```act.send
CLI URL={webhook_url}; [ -z "$URL" ] && URL="$WEBHOOK_URL"; printf '%s' {message} | curl -sS -X POST -H 'Content-Type: text/plain' --data-binary @- "$URL"
  message: string (required) "Text message to send"
  webhook_url: string "Override webhook URL for a one-off send" = ""
```

```act.send.response
Sent message to {Response.body.agent_id}.

- event_id: {Response.body.event_id}
- next: target reads it with `/events.read {Response.body.event_id}`
```
