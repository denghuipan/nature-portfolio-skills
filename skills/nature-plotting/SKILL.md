---
name: nature-plotting
description: >-
  Publication figures in Nature-journal style with matplotlib: house rcParams (np_final preset, 89/183 mm,
  5-7 pt Arial, open L-shaped axes with short outward ticks by default, switchable looks, 600 dpi PNG +
  editable PDF), 62 ready templates built from the layouts of recent Nature-family papers (trends and fans,
  benchmark bars with significance, mirrored counts, forest tables, distributions, dense scatter with zoom,
  volcano, embeddings, dot matrices, maps with stippling, survival, dose-response, training and scaling
  curves, alluvial flows, networks, colour maps and colour bars, pipeline / architecture / study-design
  diagrams, composite page), house colour maps and palettes, and pre-submission QA. Use for any plot, chart,
  figure, colour bar, schematic or figure layout for a paper. Triggers: 画图, 作图, 出图, 配图, 科研绘图, 色条,
  colorbar, 示意图, 概念图, 流程图, plot, chart, figure, Nature style, publication quality.
version: 4.0.0
author: Denghui Pan (dpan13@ucsc.edu)
---

# Nature plotting

Visual house style (`assets/nature_style.py`) + chart builders (`assets/nature_charts.py`) + colour maps,
palettes and colour bars (`assets/nature_cmaps.py`) + diagram primitives (`assets/nature_schematic.py`) + one
runnable template per figure type (`templates/`, previews in `gallery/`, overview in `README.md`).

The templates are original layouts with mock data (Data 1, Group A, Method B ...). They follow patterns that
recur across many recent Nature, Nature Methods, Nature Communications and Nature Climate Change figures;
they do not copy any published figure.

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
from nature_style import *        # rcParams, sizes, PALETTE, THEMES, set_look, panel_label, export helpers
from nature_cmaps import *        # NS_* colour maps, palettes, cbar_* helpers
from nature_charts import *       # chart builders + export()
from nature_schematic import *    # only for diagrams
use_arial_math()                  # $x$, $\mu$ in the label face
```

`load_nature_style.py` resolves the folder via `NATURE_PLOTTING_DIR`, `~/.nature-portfolio/state.json`, or the
bundled `assets/`. Never hand-roll rcParams, never use matplotlib / seaborn default styles.

**Axis look** (one per paper; `K04_axis_looks` shows all four):

| `set_look(...)` | Axes | Use for |
|---|---|---|
| `"open"` (default) | left + bottom spines, 2.5 pt outward ticks, no minor ticks | almost everything |
| `"grid"` | open + faint horizontal grid | dense bars, long time series |
| `"framed"` | full frame, outward ticks, faint grid | log-log physics / benchmark plots, panels with inset sketches |
| `"classic"` | full frame, inward ticks on four sides, minor ticks, older bright palette | matching an existing paper in that style |

`style_axes(ax, look)` restyles one axes; `despine`, `offset_spines`, `thousands` (1,000 separators),
`percent`, `subtitle` finish single panels.

## 2. Pick a template

Copy the template, replace its `MOCK DATA` block with the real arrays, keep the rest. Every template runs
stand-alone (`python templates/C01_bars_significance.py`). Full chooser with alternatives:
`references/chart-chooser.md`.

| Question the figure answers | Template |
|---|---|
| Measured points vs a model on a log axis, extrapolated costs | `T01_marker_decay_log` |
| Projections with uncertainty under scenarios, per region | `T02_scenario_fans` |
| Success vs budget (log x) for two methods, gap at the end | `T03_scaling_bands` |
| Growth over time, hand-over between sources | `T04_growth_bars` |
| Change of each item between two times | `T05_slopegraph` |
| Composition of a total over time | `T06_stacked_area` |
| Noisy long series with events and a window | `T07_events_timeseries` |
| Trace + event raster + state ribbon on one time axis | `T08_trace_state_raster` |
| Benchmark families: bars, error bars, stars, n | `C01_bars_significance` |
| Subset inside a larger set, log and linear | `C02_overlay_bars` |
| Left vs right (paired halves) per category | `C03_butterfly_counts` |
| Budget of contributions with an unexplained part | `C04_error_budget` |
| Ranking of many entries with CIs | `C05_dot_ranking` |
| Subgroup effects with the numbers written out | `C06_forest_table` |
| Results table + improvement scatter | `C07_table_scatter` |
| Part of a whole (donut, 100% bars, waffle) | `C08_part_of_whole` |
| Two sets on long-named categories | `C09_horizontal_pairs` |
| Before / after per item, sorted by change | `C10_dumbbell_change` |
| Group distributions with shape and tests | `D01_violin_box` |
| Histogram with fitted model(s) | `D02_hist_fit` |
| Two populations of very different size | `D03_step_hist_log` |
| Error distributions without bins; quantiles | `D04_ecdf_quantiles` |
| Distribution drift over ordered conditions | `D05_ridgeline_outline` |
| Every observation per group, no overlap | `D06_beeswarm` |
| Paired measurements and their differences | `D07_paired_points` |
| Overlapping 2-D populations | `D08_density_contours` |
| Dense agreement scatter with a magnified corner | `R01_dense_scatter_zoom` |
| Trend of a noisy outcome, support per bin | `R02_binned_trend` |
| Units of different size vs two drivers | `R03_bubble_colorbar` |
| Thousands of tested features, hits named | `R04_volcano` |
| 2-D embedding: clusters and a property | `R05_embedding_clusters` |
| Prediction vs reference for thousands of samples | `R06_parity_density` |
| Same relationship fitted per group | `R07_group_regression` |
| Two criteria at once, target quadrant | `R08_quadrant_map` |
| Features x groups, two quantities per cell | `M01_dot_matrix` |
| Clustered matrix with known row groups | `M02_cluster_heatmap` |
| Pairwise correlations | `M03_corr_circles` |
| Classifier on imbalanced classes | `M04_confusion_support` |
| Gridded change field with significance | `M05_field_stipple` |
| Micrographs: conditions x channels + zoom | `M06_image_grid` |
| Directions / phases / times of day | `M07_polar_rose` |
| Spectral content over time | `M08_spectrogram` |
| Training history over seeds | `N01_training_curves` |
| Detection performance (rare positives) | `N02_roc_pr` |
| Loss vs compute, frontier fit | `N03_scaling_law` |
| Probability calibration | `N04_calibration` |
| Time-to-event between arms | `B01_survival_km` |
| Potency of several compounds | `B02_dose_response` |
| Repeated measures over days + AUC | `B03_timecourse_stars` |
| Movement between categories over stages | `G01_alluvial` |
| Small weighted network | `G02_node_link` |
| Which colour map / colour bar / palette / axis look | `K01_colormaps`, `K02_colorbar_styles`, `K03_palettes_cvd`, `K04_axis_looks` |
| Pipeline with branches, database and loop | `S01_pipeline_loop` |
| Model architecture with streams and recycling | `S02_architecture` |
| Iterative loop + its stages with icons | `S03_cycle_stages` |
| Study design: enrolment, arms, visit schedule | `S04_study_design` |
| Qualitative sketches (scaling, landscape, sets) | `S05_concept_sketches` |
| One-line visual abstract of the workflow | `S06_icon_workflow` |
| Full double-column composite page | `F01_composite_figure` |

## 3. Sizes and presets

| Item | `np_final` (default) | `preview` (alias `mock`) |
|---|---|---|
| Single / double column | 89 / 183 mm | same figure sizes, larger type |
| Max height | 170 mm | -- |
| Base / tick / panel letter | 7 / 6 / 8 pt bold | 10 / 9 / 11 pt |
| Axes / data lines | 0.6 / 1.0 pt | 0.9 / 1.5 pt |

Helpers: `figsize_1col()`, `figsize_2col()`, `figsize_1col_tall()`, `figsize_mm(w, h)`. Extended Data pages
are at most 180 mm wide; `ed_finish(fig)` rescales and clamps line widths.

## 4. Visual rules

- Arial (fallback Helvetica / Liberation Sans), 5-7 pt at final size, nothing below 5 pt; maths via
  `use_arial_math()`; bold only for panel letters.
- Open axes, short outward ticks, no minor ticks, no grid unless the look asks for one; frameless legends
  with short handles; square keys (`square_legend`) for bars and areas.
- Numbers as printed in Nature: thousands separators (`thousands`, `fmt_int`), true minus signs, `n = 428`
  under categories (`n_ticklabels`), exact P values or stars (`sig_bracket`, `p_to_stars`).
- Label lines and groups directly (`end_labels`, `direct_label`, `place_labels`) when there are <= 5 of them.
- Show individual observations when n is small (`bars(..., points=)`, `beeswarm`, `jitter`,
  `paired_lines`); state centre and error (mean +- s.e.m., n = 8) in the panel.
- Colour carries one meaning across the paper: the method of interest one strong hue, baselines grey or a
  lighter tone of the same hue, up / down in `THEMES["updown"]`; pair colour with marker shape for CVD.
- English only inside figures.

## 5. Colour maps, palettes and colour bars

Details: `references/colour-and-colorbars.md`.

- Categorical: `EDITORIAL` (= `HOUSE`, default cycle), `HOUSE_DARK` (thin lines, text), `OKABE_ITO`,
  `PAIRED` (light, dark), `THEMES[...]`: `duo_purple`, `duo_blue`, `duo_teal` (reference vs new), `soft`
  (pastel bars + greys), `fan` (scenarios), `signal` (hollow-marker trio), `earth`, `updown`. Named colours
  in `PALETTE` (`blue`, `ochre`, `teal`, `plum`, `brick`, `sage`, `rose`, `grey`, `sky`, `sand` ...).
- Sequential (monotonic CIE L*): `NS_BLUES`, `NS_REDS`, `NS_GREENS`, `NS_PURPLES`, `NS_GRAYS`, `NS_EMBER`
  (images), `NS_GLACIER`, `NS_SUNSET` (error maps), `NS_DUSK` (scatter / bubbles), `NS_SEAFLOOR` (densities).
- Diverging: `NS_DIV_BR`, `NS_DIV_PG`, `NS_DIV_BO`, `NS_DIV_DARK`; pin the centre with
  `center_norm(vmin, 0, vmax)`. Cyclic: `NS_PHASE`. True visible colour: `NS_VISIBLE`.
- Colour bars (hair-line outline, outward ticks): `cbar_side`, `cbar_below` (under a scatter), `cbar_inset`,
  `cbar_top`, `cbar_span`, `cbar_discrete`, `cbar_endlabels`, `line_mappable`, `spectrum_strip`, `log_ticks`;
  `size_legend` for bubble areas.
- Never rainbow / jet for ordered data; check palettes with `simulate_cvd`.

## 6. Concept diagrams

`nature_schematic.py` draws on a millimetre canvas (`canvas(ax, w_mm, h_mm)`), so diagrams share fonts and
line weights with the data panels and stay vector. Guide: `references/schematics.md`.

- Blocks and frames: `pbox` (pastel box from `PASTEL`), `box`, `group_frame`, `cylinder` (database),
  `circle_node`, `plus_node`, `chevrons`, `cycle_diagram`, `timeline`, `section_header`, `divider`.
- Connectors: `arrow`, `elbow`, `route` (rounded, dashed, labelled loops), `brace`, `zoom_connector`.
- Icons: `icon_graph`, `icon_stack`, `icon_bars`, `icon_person`, `icon_cells`, `matrix_icon`, `mini_plot`,
  `image_icon`, `nn_diagram`, `conv_blocks`.
- Also available: line-art optics (`beam`, `lens`, `objective`, `mirror`, `beamsplitter`, `camera`, `fiber`),
  `layer_stack`, `iso_block`, `dimension`, `concept_axes` (sketch axes without numbers).

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
- Mix looks within one paper, or put the legend over data or text below 5 pt.
- Use bars for distributions with n > 10 without the points, or 3-D charts where a heat map answers.
- Copy a published figure; borrow the layout idea, draw it with your own data.
- Deliver a figure you have not viewed as a rendered PNG.
