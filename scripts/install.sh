#!/usr/bin/env bash
# macOS / Linux: install skills into ~/.cursor, ~/.claude, ~/.codex
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="${1:-$ROOT/config.yaml}"
if [[ ! -f "$CONFIG" ]]; then
  cp "$ROOT/config.example.yaml" "$CONFIG"
  echo "Created config.yaml — edit canonical_plotting_dir, then re-run."
  exit 2
fi
exec powershell.exe -ExecutionPolicy Bypass -File "$ROOT/scripts/install.ps1" -ConfigPath "$CONFIG" 2>/dev/null || \
  python3 "$ROOT/scripts/install.py" "$CONFIG"
