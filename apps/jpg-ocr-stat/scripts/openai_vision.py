#!/usr/bin/env python3
"""OpenAI vision OCR/analysis for one image -> JSON.

Uses a vision-capable GPT model to read text or describe an image. Needs
OPENAI_API_KEY in the environment. Good fallback when Tesseract struggles
(handwriting, stylized fonts, complex layouts).
"""

import argparse
import base64
import json
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: openai. "
                      "Install: pip install openai (or conda install -c conda-forge openai)"}))
    sys.exit(1)

MEDIA = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
         "gif": "image/gif", "webp": "image/webp"}


def main():
    ap = argparse.ArgumentParser(description="Analyze/OCR an image with OpenAI vision.")
    ap.add_argument("--image", required=True, help="Path to image")
    ap.add_argument("--prompt", default="Extract ALL text from this image in reading order. "
                    "Return only the text, nothing else.", help="Instruction for the model")
    ap.add_argument("--model", default="gpt-4o", help="Vision model id")
    ap.add_argument("--detail", default="high", choices=["low", "high", "auto"],
                    help="Image detail level (high = best for OCR)")
    args = ap.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print(json.dumps({"success": False, "error": "OPENAI_API_KEY not set. "
                          "Export it or add to .env (chmod 600): export OPENAI_API_KEY=sk-..."}))
        sys.exit(1)
    if not os.path.isfile(args.image):
        print(json.dumps({"success": False, "error": f"Image not found: {args.image}"}))
        sys.exit(1)

    ext = args.image.lower().rsplit(".", 1)[-1]
    media = MEDIA.get(ext, "image/jpeg")
    with open(args.image, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    try:
        client = OpenAI()
        resp = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": args.prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:{media};base64,{b64}", "detail": args.detail}},
            ]}],
            max_tokens=1500,
        )
    except Exception as e:
        print(json.dumps({"success": False, "error": f"OpenAI API call failed: {e}"}))
        sys.exit(1)

    usage = getattr(resp, "usage", None)
    print(json.dumps({
        "success": True,
        "filename": os.path.basename(args.image),
        "model": args.model,
        "detail": args.detail,
        "result": resp.choices[0].message.content,
        "token_usage": {"prompt": getattr(usage, "prompt_tokens", None),
                        "completion": getattr(usage, "completion_tokens", None)} if usage else None,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
