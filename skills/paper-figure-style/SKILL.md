---
name: paper-figure-style
description: >-
  The house style and production workflow for this user's publication matplotlib figures — Arial 9 pt, inward four-sided ticks, no grid, frameless legend, fixed PALETTE, single-column 4.3x3.2 in, exported as 600 dpi PNG + vector PDF via the shared plotting/nature_style.py module. Use whenever producing, restyling, or exporting a matplotlib figure for a paper, notebook, report, or analysis in this user's projects — including any request phrased as 画图, 作图, 出图, 配图, 科研绘图, 论文图表, plot, chart, figure, restyle a plot, "make it Nature style", or "publication quality". Also carries the notebook-building workflow (nbformat builder script -> nbclient execute -> read back the rendered PNG and visually verify -> fix -> rerun) and the specific layout traps that workflow catches.
version: 1.0.0
author: Denghui Pan (dpan13@ucsc.edu)
---

# Paper figure house style

Every matplotlib figure produced for this user's manuscripts follows this style. It is
not a suggestion layer — it is the default. Deviate only when the user asks.

If `nature-figure` is also active, that skill governs *what* the figure argues
(conclusion, evidence chain, archetype). **This skill governs the concrete rendering
settings, and its numbers win** on any conflict about fonts, ticks, colors, sizes, or export.

---

## 1. Load the shared style module — do not hand-roll rcParams

The canonical style lives in a real module. Import it; never retype the settings.

```python
import sys
from pathlib import Path

PLOTTING_DIR = Path(r"D:\OneDrive\UCSC\Paper\End-facet\plotting")
if str(PLOTTING_DIR) not in sys.path:
    sys.path.insert(0, str(PLOTTING_DIR))
from nature_style import *   # rcParams, PALETTE, CYCLE, style_axes, panel_label, ...

# nature_style creates figure_mock/ in cwd on import; remove it if unused
_mock = Path("figure_mock")
if _mock.exists() and not any(_mock.iterdir()):
    _mock.rmdir()
```

**Two gotchas in that module:**

- `nature_style.save()` writes into `figure_mock/`, not your output dir. Define a local
  `save_fig()` instead (§3).
- The import has the `figure_mock/` side effect above. Clean it up.

If `plotting/nature_style.py` is unreachable (different machine, different repo), fall back
to [assets/style_header.py](assets/style_header.py), which inlines the identical settings.
Do not silently fall back to matplotlib defaults.

## 2. The style itself

| Setting | Value |
|---|---|
| Font | Arial (fallback DejaVu Sans), 9 pt base; axis labels 11 pt; titles 10 pt; legend 6.5–8 pt; in-axes annotations 6.5–7 pt |
| Ticks | `direction="in"`, `top=True`, `right=True`, minor ticks visible, major size 4, width 1.0 |
| Spines | all four, `linewidth=1.0` |
| Grid | **off** |
| Legend | `frameon=False`, `handlelength=1.8`, `labelspacing=0.3` |
| Lines | `lw=1.8` for the primary series, 1.2–1.4 for secondary, 1.0–1.2 for reference lines |
| Markers | `ms≈4`, `markeredgecolor="white"`, `markeredgewidth=0.6` |
| Export | PNG **600 dpi** + **PDF vector**, both, `bbox_inches="tight"`, `pdf.fonttype=42` |

**Palette — use these, never `tab10`:**

```
blue #2C6AB4   red #E84143   green #39AF6B   purple #B69BC8
skyblue #5AB2E4   salmon #EA998F   sand #F5DEA8   gray #807979
```

Access as `PALETTE["blue"]`. Reference/guide lines use neutral grays `"0.35"` (emphasis)
and `"0.65"` (faint), not palette colors.

**Figure sizes** (inches, matching the existing notebooks exactly):

| Layout | Size |
|---|---|
| Single column, one panel | `(4.3, 3.2)` |
| Double column, two panels side by side | `(7.0, 2.9)` |
| Single column, two panels stacked | `(4.3, 4.8)` |

Multi-panel figures get bold lowercase labels via `panel_label(ax, "a", dx=-0.20, dy=1.08, size=11)`.

## 3. The export helper

Define this once per notebook/script. Always both formats, always 600 dpi.

```python
def save_fig(fig, name):
    fig.savefig(OUT_DIR / (name + ".png"), dpi=600, bbox_inches="tight")
    fig.savefig(OUT_DIR / (name + ".pdf"), bbox_inches="tight")
```

Call `style_axes(ax)` on **every** axes before saving — it enforces the spine width and
the inward four-sided ticks that rcParams alone can miss on twinned or inset axes.

## 4. Language rule — non-negotiable

**All text inside figures is English.** Arial and DejaVu Sans have no CJK glyphs; Chinese
in a figure renders as tofu boxes. Chinese belongs in the surrounding markdown, the
summary `.md`, and the prose — never in titles, axis labels, legends, or annotations.

## 5. Notebook production workflow

When the deliverable is a notebook, do not hand-write `.ipynb` JSON and do not paste cells
interactively. Use the builder pattern — see [assets/build_nb_template.py](assets/build_nb_template.py).

1. **Explore first.** Run a throwaway script in the scratchpad to get the real numeric
   ranges — min/max, where curves saturate, how many decades. Axis limits and annotation
   coordinates chosen before seeing the numbers are always wrong.
2. **Write a builder script** that assembles the notebook with `nbformat` and writes it out.
   The builder is the source of truth; edit it and rebuild, never edit the `.ipynb` by hand.
3. **Execute with `nbclient`**, then assert zero error outputs:
   ```python
   nb = nbformat.read(path, as_version=4)
   NotebookClient(nb, timeout=1800, kernel_name="python3",
                  resources={"metadata": {"path": "."}}).execute()
   nbformat.write(nb, path)
   print("errors:", sum(1 for c in nb.cells for o in c.get("outputs", [])
                        if o.output_type == "error"))
   ```
4. **Read back every rendered PNG with the Read tool and actually look at it.** This step is
   mandatory. A figure that "ran without error" is routinely unreadable — see §6.
5. **Fix in the builder, rebuild, re-execute, look again.** Repeat until clean.
6. **Emit a machine-readable companion**: a `.csv` of the plotted curves and a `_summary.md`
   with every number the figures assert, so the values can be cited without rerunning.

Cache expensive intermediates to `.npz` so reruns are fast — restyling should not re-parse
gigabytes of source data.

## 6. Layout traps this workflow exists to catch

Each of these shipped as a broken figure once and was caught only by looking at the PNG:

- **Annotations landing on curves, on the legend, or outside the axes.** Put text in
  measured empty regions; prefer `transform=ax.transAxes` fractions for corner labels.
- **Inherited axis limits.** A helper array defined for figure 1 (e.g. a fit line spanning
  extra decades) reused in figure 5 silently stretched its y-axis by 9 decades. Give each
  figure its own locally-scoped arrays, or set limits explicitly.
- **Perfectly overlapping curves.** When two series coincide (that being the point), draw
  the first thick and semi-opaque, the second thin and dashed on top — otherwise one is
  simply invisible and the reader assumes it is missing.
- **Values pinned against a reference line.** A quantity sitting at 0.9995 against a `+1`
  guide shows no structure. Plot `1 − r` on a log axis instead; the structure and the
  comparison both become visible.
- **Legend collisions with data peaks.** Extend the axis limit to make headroom rather than
  shrinking the font.
- **Rotated text along a vertical line** is nearly always worse than a short horizontal
  label placed beside the line.
- **Long y-axis labels** on narrow single-column panels: use a two-line label with `\n`.

## 7. Do not

- Do not use matplotlib defaults, `tab10`, seaborn themes, or `plt.style.use(...)`.
- Do not draw grid lines.
- Do not export at 200 dpi, or PNG only.
- Do not put Chinese characters in a figure.
- Do not deliver a figure you have not viewed.
- Do not restyle by editing the generated `.ipynb`; edit the builder.

## 8. Canonical examples

Read these before starting if the job is non-trivial — they are the reference
implementations of everything above:

- `simulation/end-facet pattern/fimmwave_780nm_fm_scan/analyze_fm_scan.ipynb`
- `simulation/end-facet pattern/analysis_500nm/decorrelation_vs_dlambda.ipynb`
