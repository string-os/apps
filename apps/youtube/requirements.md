# Requirements

| Package   | Used by                  |
|-----------|--------------------------|
| `yt-dlp`  | all actions              |
| `python3` | `transcript`, `search`   |

```bash
pip install yt-dlp        # any OS
brew install yt-dlp       # macOS alternative
```

`ffmpeg` is **not** required — `/act.transcript` parses `.vtt` directly.
