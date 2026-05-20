---
name: youtube
namespace: stringhub
version: 1.0.1
description: Fetch YouTube video transcripts and metadata. Summarize, search, and extract information from videos.
tags: [data, youtube, transcript, video, summary, captions]
type: app
---

[!requirements](./requirements.md)

# YouTube

Fetch transcripts and metadata from YouTube videos via [yt-dlp](https://github.com/yt-dlp/yt-dlp). No API key.

## Actions

- `/act.transcript --url <youtube-url>` — fetch auto-generated or manual captions as plain text (returns "No captions available" if the video has none)
- `/act.info --url <youtube-url>` — title, channel, duration, views, upload date, description (first 500 chars)
- `/act.search --query <text> [--limit 5]` — search YouTube and list results

```act.transcript
CLI yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt -o "/tmp/yt-%(id)s" {url} >/dev/null 2>&1 && python3 -c "import glob,re,sys;files=glob.glob('/tmp/yt-*.en.vtt');[sys.exit('No captions available for this video.') if not files else None];raw=open(files[0]).read();body=raw.split('\n\n',1)[1] if '\n\n' in raw else raw;blocks=[b for b in body.split('\n\n') if b.strip() and '-->' in b];lines=[];[lines.extend(l for l in b.split('\n')[1:] if l.strip() and not l.startswith('NOTE')) for b in blocks];text=re.sub(r'<[^>]+>','',' '.join(lines));seen=set();out=[];[out.append(s) for s in text.split('. ') if s.strip() and s not in seen and not seen.add(s)];print('. '.join(out))" && rm -f /tmp/yt-*.vtt 2>/dev/null || echo "Failed to fetch transcript. Make sure the video has captions and yt-dlp is installed."
  url: string (required) "YouTube video URL"
```

```act.info
CLI yt-dlp --skip-download --print "## %(title)s" --print "" --print "- **Channel:** %(channel)s" --print "- **Duration:** %(duration_string)s" --print "- **Views:** %(view_count)s" --print "- **Upload date:** %(upload_date)s" --print "" --print "%(description).500s" {url}
  url: string (required) "YouTube video URL"
```

```act.search
CLI yt-dlp "ytsearch{limit}:{query}" --skip-download --flat-playlist --print "### %(title)s\n- **Channel:** %(channel)s · **Duration:** %(duration_string)s\n- **URL:** https://www.youtube.com/watch?v=%(id)s\n" 2>/dev/null || echo "Search failed."
  query: string (required) "Search query"
  limit: number (optional) "Max results" = "5"
```
