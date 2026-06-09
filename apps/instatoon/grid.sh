#!/usr/bin/env bash
# grid.sh — Compose 4 cut images into a 2x2 grid PNG.
# Usage: grid.sh <title_dir> <cuts_csv>
#   <title_dir>: the title's out subfolder, e.g. ~/.string/.../apps/instatoon/out/marathon
#   <cuts_csv>:  comma-separated 4 cut numbers, e.g. "1,2,3,4"
# Output: <title_dir>/grid-<cuts>.png
set -euo pipefail

TITLE_DIR="${1:?title_dir required}"
CUTS_CSV="${2:?cuts csv required (e.g. 1,2,3,4)}"
OUTPUT="$TITLE_DIR/grid-${CUTS_CSV}.png"

if [ ! -d "$TITLE_DIR" ]; then
  echo "✗ Title dir does not exist: $TITLE_DIR"
  echo "  Run /act.character --title <slug> first."
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"

python3 - "$TITLE_DIR" "$CUTS_CSV" "$OUTPUT" <<'PY'
import sys, os
from PIL import Image

title_dir, cuts_csv, output = sys.argv[1], sys.argv[2], sys.argv[3]
cut_nums = [int(x.strip()) for x in cuts_csv.split(",") if x.strip()]

if len(cut_nums) != 4:
    print(f"✗ Need exactly 4 cuts for 2x2 grid, got {len(cut_nums)}: {cut_nums}", file=sys.stderr)
    sys.exit(1)

paths = [os.path.join(title_dir, f"cut-{n}.png") for n in cut_nums]
missing = [p for p in paths if not os.path.isfile(p)]
if missing:
    print(f"✗ Missing cut files: {missing}", file=sys.stderr)
    sys.exit(1)

# Open all 4 cut images
images = [Image.open(p) for p in paths]
# Normalize to the smallest dim so grid is uniform
min_w = min(im.width for im in images)
min_h = min(im.height for im in images)
images = [im.resize((min_w, min_h), Image.LANCZOS) for im in images]

# Compose 2x2 with a thin gutter
GUTTER = 12
canvas_w = min_w * 2 + GUTTER * 3
canvas_h = min_h * 2 + GUTTER * 3
canvas = Image.new("RGB", (canvas_w, canvas_h), color=(255, 255, 255))

positions = [
    (GUTTER, GUTTER),
    (GUTTER * 2 + min_w, GUTTER),
    (GUTTER, GUTTER * 2 + min_h),
    (GUTTER * 2 + min_w, GUTTER * 2 + min_h),
]
for img, pos in zip(images, positions):
    canvas.paste(img, pos)

canvas.save(output, "PNG", optimize=True)
print(f"Grid composed: {output}")
print(f"  layout: 2x2 (cut-{cut_nums[0]} cut-{cut_nums[1]} / cut-{cut_nums[2]} cut-{cut_nums[3]})")
print(f"  size:   {canvas_w}x{canvas_h}")
PY
