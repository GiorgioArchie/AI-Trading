#!/usr/bin/env python3
"""
Extract scene-change keyframes (charts/slides) from a video using PyAV.
Usage: keyframes.py <input_video> <output_dir> [interval_seconds] [scene_threshold]
  interval_seconds: minimum gap between saved frames (default 20)
  scene_threshold:  mean abs frame diff to count as a scene change 0-255 (default 12)
Saves JPGs named <basename>_<mmss>.jpg. No system ffmpeg needed.
"""
import sys
import os


def main():
    if len(sys.argv) < 3:
        print("Usage: keyframes.py <input_video> <output_dir> [interval_seconds] [scene_threshold]")
        sys.exit(2)

    in_path = sys.argv[1]
    out_dir = sys.argv[2]
    min_gap = float(sys.argv[3]) if len(sys.argv) > 3 else 20.0
    threshold = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0

    if not os.path.exists(in_path):
        print(f"ERROR: input not found: {in_path}")
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)

    import av
    import numpy as np

    base = os.path.splitext(os.path.basename(in_path))[0].replace(" ", "_")
    container = av.open(in_path)
    stream = container.streams.video[0]
    stream.thread_type = "AUTO"

    prev_small = None
    last_saved = -1e9
    saved = 0
    for frame in container.decode(stream):
        t = float(frame.pts * stream.time_base) if frame.pts is not None else 0.0
        # downsample to grayscale ~64px wide for cheap scene-diff
        img = frame.to_ndarray(format="gray8")
        small = img[:: max(1, img.shape[0] // 64), :: max(1, img.shape[1] // 64)].astype("int16")
        is_scene = False
        if prev_small is None:
            is_scene = True
        else:
            h = min(prev_small.shape[0], small.shape[0])
            w = min(prev_small.shape[1], small.shape[1])
            diff = np.abs(small[:h, :w] - prev_small[:h, :w]).mean()
            if diff > threshold:
                is_scene = True
        prev_small = small

        if is_scene and (t - last_saved) >= min_gap:
            mm = int(t // 60)
            ss = int(t % 60)
            name = f"{base}_{mm:02d}m{ss:02d}s.jpg"
            frame.to_image().save(os.path.join(out_dir, name), quality=80)
            last_saved = t
            saved += 1

    container.close()
    print(f"DONE: saved {saved} keyframes from {os.path.basename(in_path)} -> {out_dir}")


if __name__ == "__main__":
    main()
