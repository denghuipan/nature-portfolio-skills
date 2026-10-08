# Nature Portfolio Skills

Portable **Nature / Nature Photonics** agent skill bundle: writing, figures,
plotting (`nature_style.py`), citations, reviewer response, PPT, etc.

## Quick install

1. `git clone https://github.com/denghuipan/nature-portfolio-skills.git`
2. Copy `config.example.yaml` → `config.yaml` (optional: set `canonical_plotting_dir`; default `""` uses bundled assets).
3. Run the installer for your OS:

**macOS / Linux**

```bash
cd nature-portfolio-skills
cp config.example.yaml config.yaml
chmod +x scripts/install.sh
./scripts/install.sh
# or: python3 scripts/install.py
```

**Windows**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
```

4. Restart **Cursor**, **Claude Code**, and/or **Codex**.

Install copies `skills/*` into:

| Agent | macOS / Linux | Windows |
|-------|----------------|---------|
| Cursor | `~/.cursor/skills/` | `%USERPROFILE%\.cursor\skills\` |
| Claude Code | `~/.claude/skills/` | `%USERPROFILE%\.claude\skills\` |
| Codex | `~/.codex/skills/` | `%USERPROFILE%\.codex\skills\` |

Toggle agents in `config.yaml` under `agents:`.

## Use the agent to install

After the first manual copy of this repo, open any agent and say:

> 用 nature-portfolio 安装/同步 Nature skills

The **nature-portfolio** skill tells the agent to run `scripts/install.ps1`.

## What's inside `skills/`

| Skill | Role |
|-------|------|
| nature-portfolio | Install & sync (this bootstrap) |
| nature-plotting | Matplotlib house style + NP sizes (`np_final`) |
| nature-figure | Figure contract, layouts, QA |
| nature-writing | Manuscript sections |
| nature-polishing | English polish |
| nature-citation | CNS-family citations |
| nature-academic-search | Literature search & bibliographies |
| nature-data | Data availability |
| nature-reviewer / nature-response | Pre-review & rebuttal |
| nature-reader | Bilingual paper reader |
| nature-paper2ppt / nature-paper-to-patent | Slides & patent draft |
| paper-figure-style | Legacy; prefer nature-plotting |

## Maintenance

- Edit skills under **`skills/`** in this repo, then re-run `install.ps1`.
- Canonical plotting module: `skills/nature-plotting/assets/nature_style.py`
  (install can sync it to `canonical_plotting_dir`).

## State file

`%USERPROFILE%\.nature-portfolio\state.json` records `bundle_root` for agents.

## Publish to GitHub (this machine)

1. One-time login: `gh auth login` (browser device flow).
2. From repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\publish_github.ps1
```

Default: **private** repo `nature-portfolio-skills`. Pass `-Visibility public` if you want it public.

`config.yaml` is gitignored (local paths). Only `config.example.yaml` is tracked.

## Backups

Legacy pre-`np_final` matplotlib module: `backups/nature_style.pre_np_final_backup.py`.

## License

Personal academic workflow; individual skill files may carry their own attribution.
