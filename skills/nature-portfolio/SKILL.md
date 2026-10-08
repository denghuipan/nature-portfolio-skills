---
name: nature-portfolio
description: >-
  Install, update, or repair the Nature Portfolio skill bundle on this computer
  (nature-writing, nature-figure, nature-plotting, citations, reviewer, PPT, etc.).
  Use when the user says install nature skills, 移植 skill, 新电脑, sync skills,
  setup nature-portfolio, or after cloning the nature-portfolio-skills repo.
version: 1.0.0
author: Denghui Pan (dpan13@ucsc.edu)
---

# Nature Portfolio — install & sync

This skill is the **bootstrap** for the full bundle. Other `nature-*` skills live
in the same install set; they are copied into agent skill directories by the
install script.

## When to run

- New computer or new agent install (Cursor, Claude Code, Codex)
- User edited skills in the **repo bundle** and wants agents refreshed
- `nature_style.py` or plotting paths changed

## Agent procedure (follow in order)

1. **Locate the bundle root** (folder that contains `skills/` and `scripts/install.ps1`):
   - Read `%USERPROFILE%\.nature-portfolio\state.json` field `bundle_root` if present
   - Or read `BUNDLE_ROOT.txt` next to this skill in the installed copy
   - Or ask the user where they cloned/copied `nature-portfolio-skills`

2. **Config**: In the bundle root, ensure `config.yaml` exists (copy from
   `config.example.yaml`). `canonical_plotting_dir` is **optional** — leave `""`
   to use bundled `skills/nature-plotting/assets`. Set it only to sync
   `nature_style.py` into a paper project's `plotting/` folder.

3. **Install** (Windows):

   ```powershell
   powershell -ExecutionPolicy Bypass -File "<BUNDLE_ROOT>\scripts\install.ps1"
   ```

   Use `-Force` to overwrite existing skill dirs without prompt.

4. **Verify**: Confirm `%USERPROFILE%\.cursor\skills\nature-plotting\SKILL.md`
   exists (and `.claude`, `.codex` if enabled in config).

5. Tell the user to **restart** the agent app so skills reload.

## What install does

- Copies every folder under `<BUNDLE_ROOT>/skills/` into each enabled agent's
  `skills/` directory (see `config.yaml` → `agents:`).
- Patches `nature-plotting` paths to `canonical_plotting_dir`.
- Optionally syncs `assets/nature_style.py` into that plotting directory.
- Writes `%USERPROFILE%\.nature-portfolio\state.json` with `bundle_root`.

## Bundle contents (installed skills)

`nature-academic-search`, `nature-citation`, `nature-data`, `nature-figure`,
`nature-paper-to-patent`, `nature-paper2ppt`, `nature-plotting`, `nature-polishing`,
`nature-reader`, `nature-response`, `nature-reviewer`, `nature-writing`,
`paper-figure-style`, and this `nature-portfolio` installer.

## Editing skills

- **Source of truth**: edit files under `<BUNDLE_ROOT>/skills/`, then re-run install.
- Do not treat `%USERPROFILE%\.cursor\skills\` as the master copy unless the user
  explicitly asks to pull changes back into the bundle.

## New machine (human checklist)

1. Copy or git clone `nature-portfolio-skills` to disk (OneDrive/USB ok).
2. Edit `config.yaml` → `canonical_plotting_dir`.
3. Run `scripts/install.ps1` (or ask the agent using this skill).
4. Restart Cursor / Claude / Codex.
