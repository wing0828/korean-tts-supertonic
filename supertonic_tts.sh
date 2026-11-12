#!/usr/bin/env bash
# Synthesize speech with on-device Supertonic 3 (CPU, no API key).
#
# Usage:
#   supertonic_tts.sh <voice> <text_file> <output> [speed]
#   supertonic_tts.sh --voice F1 --text-file in.txt --output out.mp3 --speed 1.05
#
# Voice styles: F1–F5 (female), M1–M5 (male).
# Language defaults to Korean (ko). Speed defaults to 1.05.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${SCRIPT_DIR}/.venv-supertonic/bin/python"
if [[ ! -x "$VENV_PY" ]]; then
  echo "Supertonic venv not found at $VENV_PY" >&2
  echo "Install with: python3 -m venv $SCRIPT_DIR/.venv-supertonic && $SCRIPT_DIR/.venv-supertonic/bin/pip install 'supertonic==1.3.1'" >&2
  exit 1
fi
exec "$VENV_PY" "${SCRIPT_DIR}/supertonic_tts.py" "$@"
