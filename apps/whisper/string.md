---
name: whisper
namespace: stringhub
version: 1.0.0
description: Local speech-to-text with OpenAI Whisper CLI. Transcribe audio and video files offline. No API key required.
tags: [utilities, whisper, speech-to-text, transcription, audio, stt]
type: app
default: transcribe
---

# Whisper

Local speech-to-text using OpenAI's Whisper model. Transcribe audio and video files entirely on your machine. No API key, no data sent to the cloud.

---

## Transcribe

`/act.transcribe --file "recording.mp3"`

```act.transcribe
CLI whisper "{file}" --model {model} --language {language} --output_format txt --output_dir /tmp/whisper-out 2>/dev/null && cat /tmp/whisper-out/*.txt && rm -rf /tmp/whisper-out || echo "Transcription failed. Ensure whisper is installed: pip install openai-whisper"
  file: string (required) "Path to audio/video file (mp3, wav, m4a, mp4, webm, etc.)"
  model: string (optional) "Model size: tiny, base, small, medium, large" = "base"
  language: string (optional) "Language code (en, ko, ja, etc.) or auto-detect" = "en"
```

---

## Transcribe with Timestamps

`/act.transcribe_srt --file "meeting.mp3"`

```act.transcribe_srt
CLI whisper "{file}" --model {model} --language {language} --output_format srt --output_dir /tmp/whisper-out 2>/dev/null && cat /tmp/whisper-out/*.srt && rm -rf /tmp/whisper-out || echo "Failed. Install: pip install openai-whisper"
  file: string (required) "Path to audio/video file"
  model: string (optional) "Model size" = "base"
  language: string (optional) "Language code" = "en"
```

---

## Models

| Model | Size | Speed | Quality | VRAM |
|-------|------|-------|---------|------|
| tiny | 39M | Fastest | Basic | ~1GB |
| base | 74M | Fast | Good | ~1GB |
| small | 244M | Medium | Better | ~2GB |
| medium | 769M | Slow | Great | ~5GB |
| large | 1.5G | Slowest | Best | ~10GB |

Start with `base` for speed, use `small` or `medium` for accuracy.

---

## Tips

- Supports: mp3, wav, m4a, flac, mp4, webm, and most audio/video formats
- First run downloads the model (~74MB for base) — subsequent runs are instant
- For non-English audio, set `--language` or omit for auto-detection
- Combine with YouTube Watcher: download video with `yt-dlp`, then transcribe
- Requires: `whisper` (`pip install openai-whisper`), `ffmpeg`
