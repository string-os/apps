# Requirements

## System Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `whisper` | OpenAI Whisper speech-to-text CLI | See install options below |
| `ffmpeg` | Audio decoding (Whisper internal dependency) | `apt install ffmpeg` / `brew install ffmpeg` / `choco install ffmpeg` |
| `python3` | Whisper runtime | Pre-installed on most systems |

## Install options

`pip install openai-whisper` is the simple route, but it pulls in PyTorch which by default downloads ~1 GB of CUDA libraries even on CPU-only machines.

**CPU-only (recommended for laptops without NVIDIA GPU)** — much faster install (~200 MB):

```bash
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install openai-whisper
```

**With CUDA (GPU)** — the default. Use this if you have an NVIDIA GPU and want fast transcription:

```bash
pip install openai-whisper
```

## Verification

```bash
which whisper              # /home/.../bin/whisper
ffmpeg -version | head -1  # should print version
whisper --help | head -3   # should print usage
```

## First-run model download

Whisper downloads its model on first use (cached in `~/.cache/whisper/`):

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 39 MB | very fast | low |
| `base` | 74 MB | fast | OK |
| `small` | 244 MB | medium | good |
| `medium` | 769 MB | slow | better |
| `large` | 1.5 GB | very slow | best |

The actions in this app default to a smaller model. To force a specific size, edit the action's `--model` flag.

## Notes

- **No API key needed** — runs entirely on your machine.
- **GPU detection is automatic.** If `torch.cuda.is_available()` is true, Whisper uses GPU; otherwise CPU.
- Supported input: `mp3`, `wav`, `m4a`, `flac`, `mp4`, `webm`, `mov`, and most other formats `ffmpeg` can decode.
- For short clips (~1 min) on CPU, expect ~10–30 seconds of processing for `base`. For 1-hour audio with `small`, expect 5–15 minutes on CPU.
