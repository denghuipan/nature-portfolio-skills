"""
Portable import helper for nature_style.py.

Resolution order:
  1. Environment variable NATURE_PLOTTING_DIR
  2. ~/.nature-portfolio/state.json  -> plotting_dir
  3. BUNDLE_ROOT.txt (from install.ps1) -> .../skills/nature-plotting/assets
  4. This file's directory (bundled assets)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_ASSETS_DIR = Path(__file__).resolve().parent


def resolve_plotting_dir() -> Path:
    env = os.environ.get("NATURE_PLOTTING_DIR", "").strip()
    if env:
        p = Path(env).expanduser()
        if (p / "nature_style.py").is_file():
            return p.resolve()
        raise FileNotFoundError(f"NATURE_PLOTTING_DIR has no nature_style.py: {p}")

    state_path = Path.home() / ".nature-portfolio" / "state.json"
    if state_path.is_file():
        data = json.loads(state_path.read_text(encoding="utf-8-sig"))
        plot = data.get("plotting_dir")
        if plot:
            p = Path(plot)
            if (p / "nature_style.py").is_file():
                return p.resolve()
        bundle = data.get("bundle_root")
        if bundle:
            p = Path(bundle) / "skills" / "nature-plotting" / "assets"
            if (p / "nature_style.py").is_file():
                return p.resolve()

    for agent_dir in (".cursor", ".claude", ".codex", ".agents"):
        hint = Path.home() / agent_dir / "skills" / "nature-portfolio" / "BUNDLE_ROOT.txt"
        if hint.is_file():
            bundle = Path(hint.read_text(encoding="utf-8").strip())
            p = bundle / "skills" / "nature-plotting" / "assets"
            if (p / "nature_style.py").is_file():
                return p.resolve()

    if (_ASSETS_DIR / "nature_style.py").is_file():
        return _ASSETS_DIR

    raise FileNotFoundError(
        "Cannot find nature_style.py. Clone nature-portfolio-skills, run scripts/install.ps1, "
        "or set NATURE_PLOTTING_DIR to a folder containing nature_style.py."
    )


def load():
    """Insert plotting dir on sys.path (idempotent)."""
    d = resolve_plotting_dir()
    s = str(d)
    if s not in sys.path:
        sys.path.insert(0, s)
    return d


# Convenience: import load_nature_style before nature_style in notebooks
load()
