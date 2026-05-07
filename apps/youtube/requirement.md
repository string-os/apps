# Requirements

## System Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `yt-dlp` | YouTube video/metadata/transcript fetcher | `pip install yt-dlp` (any OS) — or `brew install yt-dlp` |
| `python3` | Action scripts (transcript parser, search formatter) | Pre-installed on most systems; otherwise `apt install python3` |

## Verification

```bash
yt-dlp --version    # should print a version like 2025.x.x
python3 --version
```

## Notes

- **No API key needed** — uses YouTube public data via `yt-dlp`.
- **Transcripts** require the video to have captions (auto-generated or manual). If a video has no captions, `/act.transcript` returns `No captions available for this video.`
- **`ffmpeg` is NOT required.** Earlier versions of this app suggested ffmpeg; the current `/act.transcript` parses `.vtt` directly without conversion, so you can skip ffmpeg entirely.
- For very long videos the transcript output can be tens of KB — pipe it through your AI for summarization rather than reading it raw.
- `/act.search` returns a flat list of results; chain with `/act.info --url <url>` for details on a specific hit.
