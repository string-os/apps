---
title: Spawn Agent Requirements
---

# Requirements

Commands:

- `string`
- `claude`
- `tmux`
- `python3`

## Defaults

- Agent root: `$HOME/crew`
- Agent home: `$HOME/crew/<name>`
- Claude MCP config: `$HOME/crew/<name>/.mcp.json`
- Claude charter: `$HOME/crew/<name>/CLAUDE.md`

Override the root with:

```bash
export SPAWN_AGENT_ROOT=/home/ubuntu/crew
```

## Claude Code channel

`/act.launch` starts Claude Code with:

```bash
--mcp-config <home>/.mcp.json
--dangerously-load-development-channels server:string
```

The MCP server name stays `string`, so the tool id remains stable. The selected
String agent is controlled by `--agent <name>` inside `.mcp.json` and by
`STRING_AGENT_ID=<name>` in the launched process.

## Optional Discord channel

If this file exists:

```text
~/.claude/channels/discord-<name>/.env
```

then launch also enables Anthropic's official Discord channel:

```bash
--channels plugin:discord@claude-plugins-official
```

The app does not create or store Discord bot tokens. A human must write that
`.env` file if Discord is wanted.
