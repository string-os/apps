#!/usr/bin/env python3
"""
render.py — call Gemini 3 Pro Image with a variable number of reference images.

Used by /act.render. Builds the Gemini multipart body dynamically so we can pass
N character refs (one per character that appears in the cut) plus an optional
"previous panel" reference for sequence consistency.

Usage:
  render.py <title_dir> <cut> <characters_csv> <prev_ref|""> <style> <output_path> <storyboard_path>

  title_dir       e.g. ~/.string/users/default/apps/instatoon/out/marathon
  cut             cut number (string ok)
  characters_csv  comma-separated character names. Reads <title_dir>/character-<name>.png for each.
                  If empty string, falls back to <title_dir>/character.png (single-character toons).
  prev_ref        absolute path to the previously rendered cut. Empty string to skip.
  style           visual style hint
  output_path     where to save the resulting PNG
  storyboard_path absolute path to storyboard.txt
"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error


def b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def main() -> int:
    if len(sys.argv) != 8:
        print(f"✗ Usage: {sys.argv[0]} <title_dir> <cut> <characters_csv> <prev_ref> <style> <output> <storyboard>", file=sys.stderr)
        return 1

    title_dir, cut, characters_csv, prev_ref, style, output, storyboard_path = sys.argv[1:8]

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("✗ GEMINI_API_KEY is not set in env", file=sys.stderr)
        return 1

    if not os.path.isfile(storyboard_path):
        print(f"✗ Storyboard not found: {storyboard_path}", file=sys.stderr)
        return 1

    # Resolve character ref paths.
    char_paths = []
    char_names = [n.strip() for n in characters_csv.split(",") if n.strip()]
    if not char_names:
        # Backwards-compat: single character toon, look for plain character.png.
        single = os.path.join(title_dir, "character.png")
        if not os.path.isfile(single):
            print(f"✗ No --characters given and no fallback {single}", file=sys.stderr)
            return 1
        char_paths.append(single)
        char_names = ["(default)"]
    else:
        for name in char_names:
            p = os.path.join(title_dir, f"character-{name}.png")
            if not os.path.isfile(p):
                print(f"✗ Character ref missing: {p}", file=sys.stderr)
                print(f"  Run /act.character --title <T> --name {name} ... first.", file=sys.stderr)
                return 1
            char_paths.append(p)

    parts = []

    # All character references first, each labelled by name in a preceding text part.
    char_label_text = (
        "Reference images for the characters in this comic. Treat each one as "
        "ground truth for the character it depicts. Preserve their face shape, "
        "eyes, hairstyle, skin tone, accessories (glasses, beard, etc.) and "
        "clothing palette throughout. Characters appearing in this cut (in order):"
    )
    for name in char_names:
        char_label_text += f"\n- {name}"
    parts.append({"text": char_label_text})
    for path in char_paths:
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(path)}})

    # Optional: previous-panel reference for sequence consistency.
    if prev_ref:
        if not os.path.isfile(prev_ref):
            print(f"✗ --prev_ref path does not exist: {prev_ref}", file=sys.stderr)
            return 1
        parts.append({"text":
            "The image that follows is the most recently rendered panel in this "
            "series. Match its color palette, line weight, and character "
            "appearance for visual continuity."
        })
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(prev_ref)}})

    # Render instructions.
    instruction = (
        f"You are illustrating one panel of an instatoon (Instagram comic). "
        f"Render ONLY cut #{cut}.\n\n"
        f"# Character consistency (CRITICAL)\n"
        f"For every character that appears in this cut, look up their reference "
        f"image above and reproduce them faithfully: same face shape, eye shape, "
        f"eyebrow style, hairstyle and hair color (length, parting, fringe, "
        f"texture), skin tone, accessories (glasses, earrings, beard, scars), "
        f"clothing silhouette and palette (unless the storyboard explicitly "
        f"changes outfit), and body proportions. Never invent new accessories or "
        f"drop existing ones. If multiple characters appear, keep their relative "
        f"scale and distinguishing features clear.\n\n"
        f"# Visual style (use throughout)\n{style}\n\n"
        f"# Text rendering rules\n"
        f"- Narration → render as a clean caption banner at the TOP of the panel, "
        f"in the same language as the storyboard.\n"
        f"- Dialogue → render the EXACT text from the storyboard inside a "
        f"comic-style speech bubble next to the speaking character. If Dialogue "
        f"is \"none\", do NOT draw a speech bubble.\n"
        f"- Visual note → informs composition, background, props. Never draw "
        f"this text — only the scene it describes.\n"
        f"- Emotion: show through facial expression + body language + props. "
        f"Never draw labels like \"sad\" or \"happy\".\n"
        f"- Cut 1 (thumbnail): add a LARGE hook text overlay (the Narration "
        f"line, oversized).\n"
        f"- Last cut (CTA): include a subtle like/follow visual hint per Visual "
        f"note.\n\n"
        f"# Format\n1:1 square, white or light textured background (unless the "
        f"style dictates otherwise).\n\n"
        f"# Storyboard (use ONLY the section for cut #{cut})"
    )
    parts.append({"text": instruction})

    # Storyboard text as its own part — guarantees auto JSON-escape isn't needed.
    with open(storyboard_path, "r", encoding="utf-8") as f:
        parts.append({"text": f.read()})

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"imageSize": "1K", "aspectRatio": "1:1"},
        },
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")[:1000]
        print(f"✗ Gemini HTTP {e.code}: {msg}", file=sys.stderr)
        return 1

    # Extract image bytes.
    try:
        candidates = payload["candidates"]
        parts_out = candidates[0]["content"]["parts"]
        img_part = next(p for p in parts_out if "inlineData" in p)
        img_b64 = img_part["inlineData"]["data"]
    except (KeyError, StopIteration) as e:
        print(f"✗ Could not find image in response: {e}", file=sys.stderr)
        print(json.dumps(payload, indent=2)[:1000], file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    img_bytes = base64.b64decode(img_b64)
    with open(output, "wb") as f:
        f.write(img_bytes)
    # Verify the write actually persisted (catch silent stub-fs / chroot weirdness).
    try:
        size = os.path.getsize(output)
    except OSError as e:
        print(f"✗ Wrote {len(img_bytes)} bytes but stat({output}) failed: {e}", file=sys.stderr)
        return 1
    if size != len(img_bytes):
        print(f"✗ Write size mismatch: expected {len(img_bytes)}, on disk {size}", file=sys.stderr)
        return 1

    print(f"Cut {cut} rendered → {output} ({size} bytes)")
    print(f"  characters: {', '.join(char_names)}")
    print(f"  prev_ref:   {prev_ref or '(none)'}")
    print(f"  style:      {style[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
