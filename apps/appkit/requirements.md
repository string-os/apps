---
title: appkit — Requirements
---

# Requirements

`appkit` ships as a pure shell helper plus an SFMD spec — no API keys,
no env vars. The runtime itself is the only dependency.

## System

| Tool | Why | Install |
|---|---|---|
| `bash` | The `appkit` helper script | (system default on macOS/Linux) |
| `string` | Daemon that runs SFMD apps | `npm install -g @string-os/string` |

## Verify

```
string app:appkit
```

Should render this file's body. Then:

```
string app:appkit '/act.new probe'
ls probe/
string app:appkit '/act.validate probe/string.md'
```

You should see `OK (0 warnings)`. Clean up with `rm -rf probe`.
