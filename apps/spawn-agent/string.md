---
name: spawn-agent
namespace: stringhub
version: 0.1.0
description: Provision and launch a local Claude Code worker with a String agent id, home, plugin, and String channel.
tags: [agent, claude-code, mcp, channel, tmux, automation]
type: app
---

[!requirements](./requirements.md)

# Spawn Agent

Create a local worker agent with its own String home and Claude Code session.

```
/act.provision kai "review pull requests and report concise findings"
/act.launch kai

/act.provision rex "port the parser" --engine codex   # spawn a Codex worker
/act.launch rex
```

Two engines:

- **claude** (default) — Claude Code with the String plugin + channel. Reached
  by webhook events (use `agent-message` `/act.send`). Charter: `CLAUDE.md`.
- **codex** — Codex CLI in tmux. No String channel; reached by typing into its
  tmux session (use `agent-message` `/act.tmux`). Charter: `AGENTS.md`.

Either way the String agent id's home equals the agent's working folder
(Claude Code project dir / Codex `-C` dir), so they always match.

Provision creates:

- String agent id: `kai`
- workspace: `$HOME/crew/kai`
- charter: `CLAUDE.md` (claude) or `AGENTS.md` (codex)
- tmux session: `kai`

Tell the user how to watch or take over the session:

```
tmux attach -t kai
```

Launch starts Claude Code with the String plugin and the String Claude Code channel.
Local webhook events for this String agent can then arrive directly in Claude
Code, while the normal `string` MCP tool remains available.

```act.provision
CLI ROOT={root}; ENG={engine}; NAME={name}; ROLE={role}; set --; [ -n "$ROOT" ] && set -- --root "$ROOT"; [ -n "$ENG" ] && set -- "$@" --engine "$ENG"; ./spawn-agent "$@" provision "$NAME" "$ROLE"
  name: string (required) "Agent id, lowercase letters/numbers/hyphens/underscores"
  role: string (required) "One-line role written into the charter (CLAUDE.md or AGENTS.md)"
  engine: string "Agent engine: claude (default) or codex" = "claude"
  root: path "Override agent root directory" = ""
```

```act.launch
CLI ROOT={root}; ENG={engine}; NAME={name}; set --; [ -n "$ROOT" ] && set -- --root "$ROOT"; [ -n "$ENG" ] && set -- "$@" --engine "$ENG"; ./spawn-agent "$@" launch "$NAME"
  name: string (required) "Agent id to launch"
  engine: string "Override engine; blank = auto-detect from how it was provisioned" = ""
  root: path "Override agent root directory" = ""
```
