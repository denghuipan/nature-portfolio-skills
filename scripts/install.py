#!/usr/bin/env python3
"""Install Nature Portfolio skills (macOS, Linux, Windows)."""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_simple_yaml(path: Path) -> dict:
    data = {
        "canonical_plotting_dir": "",
        "sync_nature_style": True,
        "agents": {},
    }
    for line in path.read_text(encoding="utf-8").splitlines():
        t = line.strip()
        m = re.match(r'^canonical_plotting_dir:\s*"(.*)"\s*$', t)
        if m:
            data["canonical_plotting_dir"] = m.group(1)
        m = re.match(r"^sync_nature_style_to_plotting_dir:\s*(true|false)\s*$", t)
        if m:
            data["sync_nature_style"] = m.group(1) == "true"
        for key in ("cursor", "claude", "codex", "agents"):
            m = re.match(rf"^{key}:\s*(true|false)\s*$", t)
            if m:
                data["agents"][key] = m.group(1) == "true"
    return data


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "config.yaml"
    skills_src = root / "skills"
    default_assets = skills_src / "nature-plotting" / "assets"
    home = Path.home()

    if not config_path.is_file():
        example = root / "config.example.yaml"
        if example.is_file():
            shutil.copy(example, config_path)
            print("Created config.yaml from config.example.yaml — edit if needed, then re-run.")
            return 2
        raise SystemExit(f"Missing config.yaml at {config_path}")

    cfg = read_simple_yaml(config_path)
    user_plot = cfg["canonical_plotting_dir"].strip()
    plot_dir = Path(user_plot).expanduser() if user_plot else default_assets

    agent_map = {
        "cursor": home / ".cursor" / "skills",
        "claude": home / ".claude" / "skills",
        "codex": home / ".codex" / "skills",
        "agents": home / ".agents" / "skills",
    }
    target_keys = [k for k in agent_map if cfg["agents"].get(k)]
    targets = [agent_map[k] for k in target_keys]

    state_dir = home / ".nature-portfolio"
    state_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "bundle_root": str(root.resolve()),
        "plotting_dir": str(plot_dir.resolve()),
        "user_plotting_override": bool(user_plot),
        "installed_at": datetime.now(timezone.utc).isoformat(),
    }
    (state_dir / "state.json").write_text(
        json.dumps(state, indent=2), encoding="utf-8"
    )

    if not skills_src.is_dir():
        raise SystemExit(f"Missing skills folder: {skills_src}")

    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        for skill in skills_src.iterdir():
            if not skill.is_dir():
                continue
            dest = target / skill.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(skill, dest)
        bundle_file = target / "nature-portfolio" / "BUNDLE_ROOT.txt"
        if bundle_file.parent.is_dir():
            bundle_file.write_text(str(root.resolve()), encoding="utf-8")

    if cfg["sync_nature_style"] and user_plot:
        src_style = default_assets / "nature_style.py"
        plot_dir.mkdir(parents=True, exist_ok=True)
        if src_style.is_file():
            shutil.copy2(src_style, plot_dir / "nature_style.py")
            print(f"Synced nature_style.py -> {plot_dir}")

    print()
    print("Nature Portfolio install complete.")
    print(f"  Bundle:       {root.resolve()}")
    print(f"  Plotting dir: {plot_dir.resolve()}")
    print(f"  Targets:      {', '.join(target_keys)}")
    print(f"  Skills:       {len(list(skills_src.iterdir()))} folders x {len(targets)} agents")
    print()
    print("Restart Cursor / Claude / Codex to reload skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
