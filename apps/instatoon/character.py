#!/usr/bin/env python3
"""
character.py — generate a single-character reference sheet via Gemini 3 Pro
Image and save it under the toon's out directory.

Used by /act.character. Wraps the Gemini API call so this app doesn't need a
templated `filename` field default in string.md.

Usage:
  character.py <title_dir> <name> <description> <style>

  title_dir     absolute path to the toon's out directory.
                SFMD passes `$HOME/apps/instatoon/out/<title>` and the daemon
                expands $HOME before this script runs.
  name          character name slug (used in filename + --characters CSV)
  description   visual description (mention species / identifying traits)
  style         visual style — keep consistent across storyboard/render
"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error


def main() -> int:
    if len(sys.argv) != 5:
        print(f"✗ Usage: {sys.argv[0]} <title_dir> <name> <description> <style>", file=sys.stderr)
        return 1

    title_dir, name, description, style = sys.argv[1:5]
    os.makedirs(title_dir, exist_ok=True)
    output = os.path.join(title_dir, f"character-{name}.png")

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("✗ GEMINI_API_KEY is not set in env", file=sys.stderr)
        return 1

    prompt = (
        f"Character reference sheet for an instatoon, white background, single "
        f"character: {description}. Character name: {name}. Visual style: "
        f"{style}. Show the character in a neutral pose, expressing emotion "
        f"through body language. High consistency, recognizable silhouette."
    )

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"imageSize": "1K", "aspectRatio": "1:1"},
        },
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")[:1000]
        print(f"✗ Gemini HTTP {e.code}: {msg}", file=sys.stderr)
        return 1

    try:
        img_b64 = next(
            p for p in payload["candidates"][0]["content"]["parts"]
            if "inlineData" in p
        )["inlineData"]["data"]
    except (KeyError, StopIteration) as e:
        print(f"✗ Could not find image in response: {e}", file=sys.stderr)
        print(json.dumps(payload, indent=2)[:1000], file=sys.stderr)
        return 1

    with open(output, "wb") as f:
        f.write(base64.b64decode(img_b64))

    size = os.path.getsize(output)
    print(f"Character \"{name}\" saved → {output} ({size} bytes)")
    print(f"  style applied: {style}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
