#!/usr/bin/env python3
"""
Transcribe a video/audio file to a timestamped Markdown transcript using faster-whisper.
Usage: transcribe.py <input_video> <output_md> [model_size]
  model_size: tiny.en | base.en | small.en | medium.en  (default: small.en)
Reads audio directly from the container via PyAV (no system ffmpeg needed).
"""
import sys
import os
import time
from datetime import timedelta


def fmt(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))


def main():
    if len(sys.argv) < 3:
        print("Usage: transcribe.py <input_video> <output_md> [model_size]")
        sys.exit(2)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    model_size = sys.argv[3] if len(sys.argv) > 3 else "small.en"

    if not os.path.exists(in_path):
        print(f"ERROR: input not found: {in_path}")
        sys.exit(1)

    from faster_whisper import WhisperModel

    t0 = time.time()
    # int8 on CPU = fast + low memory on Apple Silicon (NEON).
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    load_t = time.time() - t0
    print(f"[{os.path.basename(in_path)}] model '{model_size}' loaded in {load_t:.1f}s — transcribing...")

    segments, info = model.transcribe(
        in_path,
        beam_size=5,
        vad_filter=True,  # skip long silences
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    title = os.path.splitext(os.path.basename(in_path))[0]
    lines = [
        f"# Transcript: {title}",
        f"*Auto-transcribed via faster-whisper ({model_size}) — review for jargon errors*",
        "",
        f"- **Source:** `{in_path}`",
        f"- **Detected language:** {info.language} (p={info.language_probability:.2f})",
        f"- **Duration:** {fmt(info.duration)}",
        "",
        "---",
        "",
    ]

    full_text = []
    n = 0
    for seg in segments:
        ts = fmt(seg.start)
        text = seg.text.strip()
        lines.append(f"**[{ts}]** {text}")
        lines.append("")
        full_text.append(text)
        n += 1
        if n % 25 == 0:
            print(f"  ...{n} segments ({fmt(seg.end)} of {fmt(info.duration)})")

    # Append a clean continuous-prose version for easy reading/search.
    lines.append("---")
    lines.append("")
    lines.append("## Continuous Text")
    lines.append("")
    lines.append(" ".join(full_text))
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    dt = time.time() - t0
    rt = (info.duration / dt) if dt > 0 else 0
    print(f"DONE: {n} segments, {fmt(info.duration)} audio in {dt:.0f}s ({rt:.1f}x realtime)")
    print(f"WROTE: {out_path}")


if __name__ == "__main__":
    main()
