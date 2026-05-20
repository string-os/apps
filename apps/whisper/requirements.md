# Requirements

| Package    | Used by                              |
|------------|--------------------------------------|
| `whisper`  | both actions                         |
| `ffmpeg`   | audio decoding (whisper dependency)  |

```bash
# CPU-only (smaller install, ~200 MB instead of ~1 GB)
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install openai-whisper
apt install ffmpeg          # or: brew install ffmpeg

# With CUDA GPU (default; pulls full PyTorch)
pip install openai-whisper
```

Models download on first use into `~/.cache/whisper/`: `tiny` 39 MB, `base` 74 MB, `small` 244 MB, `medium` 769 MB, `large` 1.5 GB.
