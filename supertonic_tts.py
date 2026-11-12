#!/usr/bin/env python3
"""Synthesize speech with on-device Supertonic 3 (CPU, no API key).

Usage:
  supertonic_tts.py <voice> <text_file> <output> [speed]
  supertonic_tts.py --voice F1 --text-file in.txt --output out.mp3 --speed 1.05

Voice styles: F1–F5 (female), M1–M5 (male).
Output may be .wav or .mp3 (mp3 is converted with ffmpeg at 44.1 kHz).
Language defaults to Korean (ko).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

VOICES = [f"{g}{i}" for g in ("F", "M") for i in range(1, 6)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Supertonic 3 on-device TTS (CPU). Reads a text file verbatim."
    )
    parser.add_argument("voice_pos", nargs="?", help="Voice style, e.g. F1")
    parser.add_argument("text_file_pos", nargs="?", help="Input text file")
    parser.add_argument("output_pos", nargs="?", help="Output .wav or .mp3 path")
    parser.add_argument("speed_pos", nargs="?", type=float, help="Speed (default 1.05)")
    parser.add_argument("--voice", "-v", dest="voice", help="Voice style (F1–F5, M1–M5)")
    parser.add_argument("--text-file", "-t", dest="text_file", help="Input text file")
    parser.add_argument("--output", "-o", dest="output", help="Output audio path")
    parser.add_argument("--speed", "-s", dest="speed", type=float, help="Speed 0.7–2.0 (default 1.05)")
    parser.add_argument("--lang", default="ko", help="Language code (default: ko)")
    parser.add_argument("--steps", type=int, default=8, help="Quality steps 5–12 (default 8)")
    args = parser.parse_args(argv)

    voice = args.voice or args.voice_pos
    text_file = args.text_file or args.text_file_pos
    output = args.output or args.output_pos
    speed = args.speed if args.speed is not None else args.speed_pos
    if speed is None:
        speed = 1.05

    if not voice or not text_file or not output:
        parser.error("voice, text file, and output path are required")

    voice = voice.upper()
    if voice not in VOICES:
        parser.error(f"unknown voice {voice!r}; expected one of: {', '.join(VOICES)}")
    if not 0.7 <= speed <= 2.0:
        parser.error("speed must be between 0.7 and 2.0")

    args.voice = voice
    args.text_file = Path(text_file)
    args.output = Path(output)
    args.speed = speed
    return args


def wav_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(wav_path),
        "-ar",
        "44100",
        "-ac",
        "1",
        "-c:a",
        "libmp3lame",
        "-q:a",
        "2",
        str(mp3_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(f"ffmpeg failed converting {wav_path} -> {mp3_path}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not args.text_file.is_file():
        raise SystemExit(f"text file not found: {args.text_file}")

    # Read verbatim; only drop a single trailing newline from the file.
    text = args.text_file.read_text(encoding="utf-8")
    if text.endswith("\n"):
        text = text[:-1]
    if not text.strip():
        raise SystemExit(f"text file is empty: {args.text_file}")

    from supertonic import TTS

    tts = TTS(auto_download=True)
    style = tts.get_voice_style(voice_name=args.voice)
    wav, duration = tts.synthesize(
        text=text,
        voice_style=style,
        lang=args.lang,
        speed=args.speed,
        total_steps=args.steps,
        verbose=False,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    suffix = args.output.suffix.lower()
    if suffix == ".mp3":
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_wav = Path(tmp.name)
        try:
            tts.save_audio(wav, str(tmp_wav))
            wav_to_mp3(tmp_wav, args.output)
        finally:
            tmp_wav.unlink(missing_ok=True)
    else:
        if suffix != ".wav":
            # Default to writing WAV bytes if the extension is unusual.
            pass
        tts.save_audio(wav, str(args.output))

    import numpy as np
    duration_s = float(np.asarray(duration).reshape(-1)[0])
    print(
        f"Wrote {args.output} ({duration_s:.2f}s, voice={args.voice}, "
        f"lang={args.lang}, speed={args.speed})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
