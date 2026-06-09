#!/usr/bin/env bash
# export.sh — Bundle one toon's outputs into a publish-ready folder + manifest.
# Usage: export.sh <title_dir> [caption]
#   <title_dir>: the title's out subfolder, e.g. ~/.string/.../apps/instatoon/out/marathon
#   [caption]:   optional Instagram caption text
set -euo pipefail

TITLE_DIR="${1:?title_dir required}"
CAPTION="${2:-}"
TITLE="$(basename "$TITLE_DIR")"
BUNDLE_DIR="$TITLE_DIR/bundle"

if [ ! -d "$TITLE_DIR" ]; then
  echo "✗ Title dir does not exist: $TITLE_DIR"
  exit 1
fi

mkdir -p "$BUNDLE_DIR"

# Collect cuts present
MISSING_CUTS=()
CUTS_FOUND=0
for n in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16; do
  if [ -f "$TITLE_DIR/cut-${n}.png" ]; then
    cp "$TITLE_DIR/cut-${n}.png" "$BUNDLE_DIR/cut-${n}.png"
    CUTS_FOUND=$((CUTS_FOUND + 1))
  fi
done

# Collect grids
GRIDS_FOUND=0
for grid in "$TITLE_DIR"/grid-*.png; do
  if [ -f "$grid" ]; then
    cp "$grid" "$BUNDLE_DIR/"
    GRIDS_FOUND=$((GRIDS_FOUND + 1))
  fi
done

# Storyboard + character
[ -f "$TITLE_DIR/storyboard.txt" ] && cp "$TITLE_DIR/storyboard.txt" "$BUNDLE_DIR/"
[ -f "$TITLE_DIR/character.png" ] && cp "$TITLE_DIR/character.png" "$BUNDLE_DIR/"

# Caption
if [ -n "$CAPTION" ]; then
  echo "$CAPTION" > "$BUNDLE_DIR/caption.txt"
fi

# Manifest
cat > "$BUNDLE_DIR/manifest.json" <<EOF
{
  "title": "$TITLE",
  "timestamp": "$(date -u +%FT%TZ)",
  "cuts_count": $CUTS_FOUND,
  "grids_count": $GRIDS_FOUND,
  "has_storyboard": $([ -f "$BUNDLE_DIR/storyboard.txt" ] && echo true || echo false),
  "has_character_ref": $([ -f "$BUNDLE_DIR/character.png" ] && echo true || echo false),
  "has_caption": $([ -f "$BUNDLE_DIR/caption.txt" ] && echo true || echo false)
}
EOF

echo "Bundle ready: $BUNDLE_DIR"
echo "  title:        $TITLE"
echo "  cuts:         $CUTS_FOUND"
echo "  grids:        $GRIDS_FOUND"
echo "  storyboard:   $([ -f "$BUNDLE_DIR/storyboard.txt" ] && echo ✓ || echo ✗)"
echo "  character:    $([ -f "$BUNDLE_DIR/character.png" ] && echo ✓ || echo ✗)"
echo "  caption:      $([ -f "$BUNDLE_DIR/caption.txt" ] && echo ✓ || echo "(none)")"
echo ""
echo "Upload to Instagram from: $BUNDLE_DIR"
