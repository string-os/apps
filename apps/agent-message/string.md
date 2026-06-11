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

Look up a target agent's webhook URL by id (so you don't have to know it up front):

```
/act.webhook --agent leo
```

Then point a config at that agent and paste the URL once:

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

Look up an agent's local webhook URL by id, via the String CLI. The agent must be
registered in the same local daemon. `/set $WEBHOOK_URL` to it (a one-time step), then
`/act.send`.

```act.webhook
CLI string --agent {agent} event webhook show 2>/dev/null | grep -Eo 'https?://[^[:space:]]+' | head -1
  agent: string (required) "Agent id whose local webhook URL to fetch"
```

```act.webhook.response
Webhook URL for agent {agent}:

{Response.body}

next: /set $WEBHOOK_URL = "{Response.body}"
```
