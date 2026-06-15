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
- Claude charter: `$HOME/crew/<name>/CLAUDE.md`

## Bundled team docs (`deps/`)

Charters tell every worker to read `<root>/shared/agent-onboarding.md` (+ the
Discord access guide) first. Those docs are bundled in `deps/` so the app is
self-contained. On `/act.provision`, any bundled doc that is **missing** from
`<root>/shared/` is copied there; an existing copy is never overwritten. This
makes a fresh root (or a different machine) self-healing.

`crew/shared/*.md` remains the live master. After editing it, refresh the
bundle before committing: `cp ../../../crew/shared/agent-onboarding.md ../../../crew/shared/discord-access-guide.md deps/`.

Override the root with:

```bash
export SPAWN_AGENT_ROOT=/home/ubuntu/crew
```

## Claude Code plugin and channel

`/act.provision` ensures the String Claude Code plugin is installed:

```bash
claude plugin marketplace add string-os/string
claude plugin install string@string-os
```

`/act.launch` starts Claude Code with:

```bash
STRING_AGENT_ID=<name> claude \
  --allow-dangerously-skip-permissions \
  --dangerously-load-development-channels plugin:string@string-os
```

This matches the normal Claude Code plugin setup: the plugin provides the
`string` MCP tool, and `STRING_AGENT_ID` selects which local String agent/home
the session uses.

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
