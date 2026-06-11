---
name: spawn-agent
namespace: stringhub
version: 0.1.0
description: Provision and launch a local Claude Code worker with a String agent id, home, MCP config, and String channel.
tags: [agent, claude-code, mcp, channel, tmux, automation]
type: app
---

[!requirements](./requirements.md)

# Spawn Agent

Create a local worker agent with its own String home and Claude Code session.

```
/act.provision kai "review pull requests and report concise findings"
/act.launch kai
```

Provision creates:

- String agent id: `kai`
- workspace: `$HOME/crew/kai`
- Claude Code charter: `CLAUDE.md`
- MCP config: `.mcp.json` with server `string`
- tmux session: `kai`

Launch starts Claude Code with String MCP and the String Claude Code channel.
Local webhook events for this String agent can then arrive directly in Claude
Code, while the normal `string` MCP tool remains available.

```act.provision
CLI ROOT={root}; if [ -n "$ROOT" ]; then ./spawn-agent --root "$ROOT" provision {name} {role}; else ./spawn-agent provision {name} {role}; fi
  name: string (required) "Agent id, lowercase letters/numbers/hyphens/underscores"
  role: string (required) "One-line role written into CLAUDE.md"
  root: path "Override agent root directory" = ""
```

```act.launch
CLI ROOT={root}; if [ -n "$ROOT" ]; then ./spawn-agent --root "$ROOT" launch {name}; else ./spawn-agent launch {name}; fi
  name: string (required) "Agent id to launch"
  root: path "Override agent root directory" = ""
```
