---
name: whisper
namespace: stringhub
version: 1.0.1
description: Local speech-to-text with OpenAI Whisper CLI. Transcribe audio and video files offline. No API key required.
tags: [utilities, whisper, speech-to-text, transcription, audio, stt]
type: app
default: transcribe
---

[!requirements](./requirements.md)

# Whisper

Local speech-to-text via [OpenAI Whisper](https://github.com/openai/whisper). Transcribes audio/video files entirely on your machine — no API key, no cloud upload. Supports mp3, wav, m4a, flac, mp4, webm, mov, and most formats `ffmpeg` can decode.

## Actions

- `/act.transcribe --file <path> [--model tiny|base|small|medium|large] [--language <code>]` — transcribe to plain text
- `/act.transcribe_srt --file <path> [--model …] [--language …]` — transcribe to SRT with timestamps

```act.transcribe
CLI whisper "{file}" --model {model} --language {language} --output_format txt --output_dir /tmp/whisper-out 2>/dev/null && cat /tmp/whisper-out/*.txt && rm -rf /tmp/whisper-out || echo "Transcription failed. Ensure whisper is installed: pip install openai-whisper"
  file: string (required) "Path to audio/video file (mp3, wav, m4a, mp4, webm, etc.)"
  model: string (optional) "Model size: tiny, base, small, medium, large" = "base"
  language: string (optional) "Language code (en, ko, ja, etc.) or auto-detect" = "en"
```

```act.transcribe_srt
CLI whisper "{file}" --model {model} --language {language} --output_format srt --output_dir /tmp/whisper-out 2>/dev/null && cat /tmp/whisper-out/*.srt && rm -rf /tmp/whisper-out || echo "Failed. Install: pip install openai-whisper"
  file: string (required) "Path to audio/video file"
  model: string (optional) "Model size" = "base"
  language: string (optional) "Language code" = "en"
```
