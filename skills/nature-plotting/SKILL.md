---
name: nature-plotting
description: >-
  Publication figures in Nature-journal style with matplotlib: house rcParams (np_final preset, 89/183 mm,
  5-7 pt Arial, inward four-sided ticks, no grid, 600 dpi PNG + editable PDF), 53 ready templates covering
  line/trend, profile, comparison, distribution, relationship, matrix/field, ML, colour-map/colour-bar and
  concept-diagram figures, house colour maps and colour-bar helpers, schematic primitives, and pre-submission
  QA. Use for any plot, chart, figure, colour bar, schematic or figure layout for a paper. Triggers: 画图,
  作图, 出图, 配图, 科研绘图, 色条, colorbar, 示意图, 概念图, plot, chart, figure, Nature style, publication quality.
version: 3.0.0
author: Denghui Pan (dpan13@ucsc.edu)
---

# Nature plotting

Visual house style (`assets/nature_style.py`) + chart builders (`assets/nature_charts.py`) + colour maps and
colour bars (`assets/nature_cmaps.py`) + diagram primitives (`assets/nature_schematic.py`) + one runnable
template per figure type (`templates/`, previews in `gallery/`, overview in `README.md`).

For panel archetypes and figure-level story logic beyond this skill, also read the `nature-figure` skill.

## 0. Figure contract -- before any code

1. **Core conclusion** -- one sentence the figure must prove.
2. **Evidence chain** -- each panel maps to that claim; drop decorative panels.
3. **Chart type** -- pick from section 2 by the *question the data answers*, not by habit.
4. **Export contract** -- `np_final`, single (89 mm) or double (183 mm) column, height <= 170 mm.
5. **Statistics** -- n, centre, error definition, test; source data for every quantitative panel.

## 1. Load the modules

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill dir>/assets")))   # or: import load_nature_style
from nature_style import *        # rcParams, sizes, PALETTE, panel_label, save_fig, audit_text ...
from nature_cmaps import *        # NS_* colour maps, palettes, cbar_* helpers
from nature_charts import *       # chart builders + export()
from nature_schematic import *    # only for diagrams
use_arial_math()                  # $x$, $\mu$ in the label face
```

`load_nature_style.py` resolves the folder via `NATURE_PLOTTING_DIR`, `~/.nature-portfolio/state.json`, or the
bundled `assets/`. Never hand-roll rcParams, never use matplotlib / seaborn default styles.

## 2. Pick a template

Copy the template, replace its `MOCK DATA` block with the real arrays, keep the rest. Every template runs
stand-alone (`python templates/L01_regime_lines.py`). Full chooser with alternatives:
`references/chart-chooser.md`.

| Question the figure answers | Template |
|---|---|
| Two series vs a variable, one fails beyond a threshold | `L01_regime_lines` |
| Saturating / dose-response curves, shift between them | `L02_sigmoid_fit` |
| Family of curves ordered by a parameter | `L03_hue_lines` |
| Power-law scaling; ranked spectrum with cut-off | `L04_loglog_powerlaw` |
| Methods vs condition with uncertainty bands | `L05_ci_band` |
| Two quantities with different units, same x | `L06_dual_axis` |
| Narrow features far apart on one axis (broken axis) | `L07_broken_windows` |
| Overview + zoom of one feature, widths | `L08_inset_zoom` |
| Set-point / control history | `L09_step_series` |
| 2-4 metrics against one shared x | `L10_stacked_metrics` |
| Many examples, same comparison (small multiples) | `P01_small_multiples` |
| Ordered stack of curves with shared features | `P02_offset_curves` |
| Model mean +- sigma across conditions | `P03_uncertainty_bands` |
| Contrast between two curves (A - B) | `P04_difference_curves` |
| Few groups, small n | `C01_bar_points` |
| Two factors; composition of a total | `C02_grouped_stacked` |
| Ranking; paired before/after | `C03_lollipop_dumbbell` |
| Signed contributions to a total (budget) | `C04_waterfall_budget` |
| Benchmark against literature | `C05_landscape` |
| Spans over decades, rows of sets | `C06_range_rows` |
| Effect sizes with CIs per subgroup | `C07_forest` |
| Multi-metric profile (4-8 normalised metrics) | `C08_radar` |
| Distributions, n >= 10 | `D01_box_jitter`, `D02_raincloud` |
| Ordered processing steps, two metrics | `D03_strip_mean_twin` |
| Residual distributions, tails | `D04_hist_kde_ecdf` |
| Distribution vs an ordered factor | `D05_ridgeline` |
| Thousands of (x, y) points | `D06_joint_hexbin` |
| Prediction vs truth | `R01_parity_residual` |
| Four variables at once | `R02_scatter_color_size` |
| Calibration / scaling law with CI | `R03_fit_ci` |
| Individual results of several sample types | `R04_category_scatter` |
| Metric over two categorical factors | `M01_heatmap_annotated` |
| Pairwise correlation | `M02_corr_triangle` |
| Classification performance | `M03_confusion` |
| Images / micrographs side by side | `M04_image_plate` |
| 2-D map (linear and log), clipped range | `M05_map_extend` |
| Design-parameter sweep, optimum, constraint | `M06_contour_sweep` |
| Angles / phase; vector fields | `M07_phase_vector` |
| Shape of a 2-D function (3-D, use sparingly) | `M08_surface3d` |
| Samples x features with clusters | `M09_cluster_heatmap` |
| Training history | `N01_training_curves` |
| Detection performance | `N02_roc_pr` |
| Which colour map / colour bar / palette | `K01_colormaps`, `K02_colorbar_styles`, `K03_palettes_cvd` |
| Workflow / concept flow chart | `S01_flowchart` |
| Optical / experimental set-up line art | `S02_optical_setup` |
| Structure: isometric + cross-section + top view | `S03_device_concept` |
| Network architecture | `S04_network` |
| Qualitative trade-off / regime / before-after | `S05_concept_sketch` |
| Process / protocol steps | `S06_process_flow` |
| Full double-column composite figure | `F01_composite_figure` |

## 3. Sizes and presets

| Item | `np_final` (default) | `preview` (alias `mock`) |
|---|---|---|
| Single / double column | 89 / 183 mm | ~109 / 178 mm |
| Max height | 170 mm | -- |
| Base / tick / panel letter | 7 / 6 / 8 pt bold | 9 / 9 / 11 pt |

Helpers: `figsize_1col()`, `figsize_2col()`, `figsize_1col_tall()`, `figsize_mm(w, h)`. Nature Photonics
states a 180 mm maximum width for Extended Data pages; `ed_finish(fig)` rescales and clamps line widths.

## 4. Visual rules

- Arial (fallback Helvetica / Liberation Sans), 5-7 pt at final size, nothing below 5 pt; maths via
  `use_arial_math()`.
- Ticks inward on four sides, minor ticks on, no grid, frameless legends.
- Label curves directly (`direct_label`, `end_label`) instead of legend boxes when there are <= 4 series.
- Threshold labels beside their line (`ref_line`), regimes as gradients (`regime`), tolerance as grey bands
  (`band`), never text across data.
- Show individual points when n is small (`bars(..., points=)`, `jitter`).
- One meaning per colour across the paper: "this work" red; baselines grey/blue; losses red, gains green.
- English only inside figures.

## 5. Colour maps and colour bars

Summary (details: `references/colour-and-colorbars.md`):

- Sequential: `NS_REDS`, `NS_BLUES`, `NS_GREENS`, `NS_PURPLES`, `NS_GRAYS`, `NS_EMBER` (images),
  `NS_GLACIER`, `NS_SUNSET`; all have monotonic CIE L* (`is_monotonic(cmap)`).
- Diverging (neutral centre, matched arms): `NS_DIV_BR`, `NS_DIV_PG`, `NS_DIV_BO`, `NS_DIV_DARK`; pin the
  centre with `center_norm(vmin, 0, vmax)`.
- Cyclic (phase): `NS_PHASE`. Wavelength keys: `SPECTRUM_VNIR_SAT/SOFT`, true colour `NS_VISIBLE`.
- Categorical: `HOUSE`, `HOUSE_DARK`, `OKABE_ITO`, `PAIRED`; check with `simulate_cvd`.
- Colour bars: `cbar_side` (slim, extend triangles), `cbar_inset` (inside panel, label above), `cbar_top`,
  `cbar_span` (one bar for several panels), `cbar_discrete` (bins or named classes), `cbar_endlabels`
  ("0 ... max"), `line_mappable` (bar for a family of lines), `spectrum_strip`, `log_ticks`.
- Never rainbow / jet for ordered data; never red-green as the only contrast.

## 6. Concept diagrams

`nature_schematic.py` draws on a millimetre canvas (`canvas(ax, w_mm, h_mm)`), so diagrams share fonts and
line weights with the data panels and stay vector. Primitives: `box`, `arrow`, `elbow`, `section_header`,
`divider`, `beam`, `cone`, `lens`, `objective`, `beamsplitter`, `mirror`, `nd_filter`, `fiber`,
`fiber_coil`, `camera`, `region_topview`, `layer_stack`, `dimension`, `iso` / `iso_block`, `nn_diagram`,
`conv_blocks`, `matrix_icon`, `mini_plot`, `image_icon`, `random_field`, `periodic_field`,
`concept_axes`, `brace`, `zoom_connector`. Guide: `references/schematics.md`.

## 7. Export and QA

```python
export(fig, "fig2_b")                      # PNG 600 dpi + PDF (save_fig), prints any text < 5 pt
export(fig, "fig2", exact=True)            # full page at its exact canvas size (save_fig_exact)
```

Then:

1. Open the PNG and look at every panel: overlaps, clipped labels, legend over data, unreadable colours.
2. `python scripts/audit_layout.py fig2.pdf` (pymupdf): page size, fonts, sizes, letters, frame alignment,
   raster dpi, hairlines.
3. Checklist: `references/nature-rules.md` (sizes, fonts, colour accessibility, error bars and n, image
   integrity, Extended Data).

Gallery rebuild: `python scripts/render_gallery.py [prefix ...]`.

## 8. Do not

- Use matplotlib defaults, `tab10`, `jet`, seaborn themes or `plt.style.use`.
- Put the legend over data, the threshold label across its line, or text below 5 pt.
- Use 3-D bars or a 3-D surface where a heat map answers the question.
- Deliver a figure you have not viewed as a rendered PNG.
