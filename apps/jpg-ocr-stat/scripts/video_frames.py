#!/usr/bin/env python3
"""Extract frames from a video into an image dir, using OpenCV -> JSON.

  --every N      keep 1 of every N frames (default 1 = all)
  --seconds S    keep one frame every S seconds (overrides --every)
  --max M        stop after saving M frames (0 = no limit)

Frames are written as frame_000001.<ext>. Feed the output dir straight into the
image-ocr or openai-vision pages.
"""

import argparse
import json
import os
import sys

try:
    import cv2
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: cv2 (opencv). "
                      "Install: pip install opencv-python-headless"}))
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Extract frames from a video with OpenCV.")
    ap.add_argument("--video", required=True, help="Path to video file")
    ap.add_argument("--outdir", required=True, help="Directory for extracted frames")
    ap.add_argument("--every", type=int, default=1, help="Keep 1 of every N frames")
    ap.add_argument("--seconds", type=float, default=0, help="Seconds between frames (overrides --every)")
    ap.add_argument("--max", type=int, default=0, help="Max frames to save (0 = unlimited)")
    ap.add_argument("--format", default="jpg", choices=["jpg", "png"], help="Output image format")
    args = ap.parse_args()

    if not os.path.isfile(args.video):
        print(json.dumps({"success": False, "error": f"Video not found: {args.video}"}))
        sys.exit(1)

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(json.dumps({"success": False, "error": f"Cannot open video (codec/path?): {args.video}"}))
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    step = args.every
    if args.seconds > 0:
        step = max(1, int(round((fps or 0) * args.seconds))) if fps > 0 else args.every
    step = max(1, step)

    os.makedirs(args.outdir, exist_ok=True)
    idx = saved = 0
    files = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            name = f"frame_{saved + 1:06d}.{args.format}"
            cv2.imwrite(os.path.join(args.outdir, name), frame)
            files.append(name)
            saved += 1
            if args.max and saved >= args.max:
                break
        idx += 1
    cap.release()

    print(json.dumps({
        "success": True,
        "video": os.path.basename(args.video),
        "outdir": args.outdir,
        "frames_extracted": saved,
        "step_frames": step,
        "video_metadata": {"total_frames": total, "fps": round(fps, 2),
                           "duration_seconds": round(total / fps, 2) if fps > 0 else None,
                           "resolution": [w, h]},
        "files": files[:50] + (["...(truncated)"] if len(files) > 50 else []),
    }, indent=2))


if __name__ == "__main__":
    main()
