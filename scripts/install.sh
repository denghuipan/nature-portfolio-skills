#!/usr/bin/env bash
# macOS / Linux install
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="${1:-$ROOT/config.yaml}"
exec python3 "$ROOT/scripts/install.py" "$CONFIG"
