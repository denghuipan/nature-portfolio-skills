---
name: nature-plotting
description: >-
  Publication matplotlib workflow for this user's manuscripts (Nature Photonics /
  Nature Portfolio): load canonical nature_style.py with default np_final preset
  (89/183 mm widths, 5-7 pt type at print size), house PALETTE, inward four-sided
  ticks, no grid, PNG 600 dpi + editable PDF. Before plotting, apply the figure
  contract (conclusion, evidence panels, QA); use apply_preset("mock") only for
  large group-meeting previews. Triggers: 画图, 作图, 出图, 配图, 科研绘图, plot,
  Nature style, publication quality.
version: 2.0.0
author: Denghui Pan (dpan13@ucsc.edu)
---

# Nature plotting (style + submission logic)

This skill merges **visual house style** (`nature_style.py`) with the **figure
contract** from `nature-figure` (what to show, how to defend it, what to check
before submission). Style without logic produces pretty but review-weak figures;
logic without style misses Nature Photonics artwork rules.

## 0. Figure contract — before any code

Do this in prose (or bullet form) **before** importing matplotlib for a
manuscript figure:

1. **Core conclusion** — one sentence the figure must prove.
2. **Evidence chain** — each panel maps to that claim; drop decorative panels.
3. **Archetype** — e.g. schematic + quant grid, spectrum plate + metrics.
4. **Export contract** — preset `np_final`, column width, which panels are vector
   vs microscopy (≥300 dpi raster, scale bar, no flattened labels).
5. **Statistics / integrity** — `n`, error bars, tests, source data path; photo
   processing notes if any.

For deep panel archetypes or R backend, invoke the **`nature-figure`** skill.
For matplotlib panels in this repo, stay in Python and this module.

## 1. Load the canonical module — never hand-roll rcParams

Paths are **not** hard-coded. After `scripts/install.ps1`, use the portable loader
(bundled under this skill's `assets/`):

```python
import sys
from pathlib import Path

# Path to .../nature-plotting/assets (installed skill dir or git clone)
ASSETS = Path(__file__).resolve().parent / "assets"  # adjust if notebook lives elsewhere
sys.path.insert(0, str(ASSETS))
import load_nature_style  # resolves dir via state.json / NATURE_PLOTTING_DIR / bundle
from nature_style import *

# Optional: large preview for slides / group meeting only
# apply_preset("mock")
```

**Resolution order:** `NATURE_PLOTTING_DIR` env → `~/.nature-portfolio/state.json`
(`plotting_dir`) → `BUNDLE_ROOT.txt` from install → bundled `assets/nature_style.py`.

Optional: set `canonical_plotting_dir` in repo `config.yaml` before install to sync
`nature_style.py` into your paper project's `plotting/` folder.

## 2. Presets and print sizes

**Default: `np_final`** (Nature Portfolio / Nature Photonics artwork guide).

| Item | `np_final` | `mock` (legacy) |
|------|------------|-----------------|
| Single-column width | **89 mm** | ~109 mm (4.3 in) |
| Double-column width | **183 mm** | ~178 mm (7.0 in) |
| Base font | **7 pt** | 9 pt |
| Tick labels | **6 pt** | 9 pt |
| Panel label | **8 pt bold lowercase** | 11 pt |
| Line width (primary) | **1.5** | 1.8 |

**Use helpers — do not hard-code inches:**

```python
fig, ax = plt.subplots(figsize=figsize_1col())           # 89 × 66 mm
fig, ax = plt.subplots(figsize=figsize_2col())           # 183 × 76 mm
fig, ax = plt.subplots(figsize=figsize_1col_tall())      # 89 × 100 mm
fig, ax = plt.subplots(figsize=figsize_mm(89, 120))      # custom height ≤ 170 mm
```

Full composite figures must stay **≤ 170 mm** tall including room for legend.

## 3. Visual style (unchanged identity)

| Setting | Value |
|---|---|
| Font | Arial (fallback DejaVu Sans) |
| Ticks | inward, four sides, minor ticks on |
| Grid | **off** |
| Legend | `frameon=False` |
| Export | PNG **600 dpi** + **PDF** (`pdf.fonttype=42`, editable text) |
| Color | `PALETTE` / `CYCLE` / `SPECTRAL` — never `tab10` |

Reference lines: grays `"0.35"` / `"0.65"`. Markers: `ms≈4`, white edge.

Call `style_axes(ax)` on every axes before save. Panel labels: `panel_label(ax, "a")`.

## 4. Export

Prefer the module helper (writes to your chosen directory):

```python
OUT_DIR = Path("figures/np_final")
save_fig(fig, "fig2_panel_b", outdir=OUT_DIR)
```

Submit **PDF** for vector charts; PNG is for preview and visual QA.

## 5. Language rule

**All text inside figures is English.** No CJK in axes, legends, or annotations.

## 6. Production workflow

1. Complete **section 0** (contract).
2. Explore ranges in a throwaway cell/script.
3. Plot with `np_final` + `figsize_*` helpers.
4. Execute; `save_fig`; **read every PNG** and fix layout.
5. Run **section 7 QA** before calling the figure done.
6. Cache heavy arrays to `.npz` when iterating style.

## 7. Pre-submission QA (Nature Photonics)

| Check | Pass |
|-------|------|
| Width | 89 mm or 183 mm per panel column |
| Height | Composite ≤ 170 mm |
| Type | 5–7 pt body/ticks at final size (`np_final`) |
| Panels | Lowercase bold **a**, **b**, … top-left |
| Vector | PDF text editable; no rasterized axes |
| Photos | ≥300 dpi, scale bar, labels not burned in |
| Stats | `n`, error bars, test documented in caption or panel |
| Source data | Quant panels traceable to CSV/script |
| Integrity | Any image processing disclosed |

Official refs: [Nature figure guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/), [Nature Photonics formatting](https://nature.com/nphoton/submission-guidelines/aip-and-formatting).

## 8. Layout traps

Same as before: annotation placement, inherited axis limits, overlapping curves,
legend vs peaks, two-line y-labels on narrow panels.

## 9. Do not

- Do not use matplotlib defaults, `tab10`, seaborn themes.
- Do not use `mock` preset for final Nature Photonics submission without user request.
- Do not export PNG-only or skip visual inspection.

## 10. Canonical module

Shipped at `assets/nature_style.py` (+ `assets/load_nature_style.py`). Sample
manuscript constants: `TBL`, `HENE_*`, `SNR3_THRESHOLD` (replace for your paper).
