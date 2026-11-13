# Chart chooser

Choose by the question the panel answers. Each row names the template (in `templates/`), the main
builder functions it uses, and the usual alternative.

## Trends and curves (L, P)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Which series holds up, where does the other fail? | L01 | `regime`, `ref_line`, `direct_label`, `secondary_unit_axis` | L05 if uncertainty matters |
| Threshold crossing / shift of a saturating response | L02 | `gradient_fill`, `double_arrow` | R03 if a law is fitted |
| Trend across a family of curves | L03 | `line_mappable`, `cbar_side`, `regime` | P02 if shapes matter more than values |
| Scaling law / cut-off rank | L04 | `log_ticks`, `callout` | R03 |
| Methods across conditions with spread | L05 | `ci_band` | C02 grouped bars |
| Measured quantity + its cause, different units | L06 | twin axis, coloured spine | two stacked panels (L10) |
| Narrow features far apart | L07 | `broken_windows`, `tint_axes` | P01 small multiples |
| Feature detail inside an overview | L08 | `inset_zoom`, `double_arrow` | separate zoom panel |
| Control / search history | L09 | `step_series` | -- |
| Several metrics vs the same x | L10 | shared x, `band` | table in Extended Data |
| Many examples of the same comparison | P01 | `share_labels`, `gradient_fill` | P02 |
| Ordered sequence of curves | P02 | `ridgeline` | L03 |
| Model uncertainty vs input quality | P03 | `ci_band` | D05 ridgeline of errors |
| Contrast recovery (A - B) | P04 | zero line, shaded low-confidence region | -- |

## Comparisons (C)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Few groups, small n | C01 | `bars(points=...)` | D01 when n >= 10 |
| Two factors | C02a | `grouped_bars` | heat map (M01) for many cells |
| Composition | C02b | `stacked_barh` | -- |
| Ranking many items | C03a | `lollipop` | sorted bars |
| Paired change | C03b | `dumbbell` | slope graph |
| Signed contributions | C04 | `waterfall` | stacked bars |
| Benchmark vs literature | C05 | `landscape`, `place_labels` | table |
| Spans over decades | C06 | log axis, `cbar_inset` | -- |
| Effect sizes | C07 | `forest` | -- |
| Profile of normalised metrics | C08 | `radar` | dot plot (exact values) |

## Distributions (D)
| Question | Template | Builders |
|---|---|---|
| Compare a few distributions | D01 | `boxplot`, `jitter` |
| Skewed / bimodal distributions | D02 | half density + IQR bar + points |
| Ordered steps, two metrics | D03 | `jitter`, `mean_sd`, twin axis |
| Tails, fraction below X | D04 | `hist_step`, `kde_line`, `ecdf` |
| Distribution vs ordered factor | D05 | `ridgeline` |
| Dense 2-D data | D06 | `hexbin` + marginals + `cbar_inset` |

## Relationships (R), matrices and fields (M), ML (N)
| Question | Template |
|---|---|
| Prediction vs ground truth | R01 (`parity`) |
| Four variables | R02 (colour + size) |
| Fitted law with CI | R03 (`fit_line`) |
| Results by sample type | R04 |
| Metric over two categorical factors | M01 (`heatmap`) |
| Pairwise correlation | M02 (`corr_triangle`) |
| Classification | M03 |
| Images side by side | M04 (`scale_bar`) |
| 2-D maps, clipped / log range | M05 (`cbar_side(extend=...)`) |
| Design sweep | M06 (contours) |
| Phase, vector fields | M07 (`NS_PHASE`, streamlines) |
| Shape of a surface | M08 (3-D; give a 2-D version too) |
| Clusters in samples x features | M09 (dendrograms) |
| Training history | N01 |
| Detection performance | N02 |

## Colour, diagrams, layout (K, S, F)
K01 colour maps + lightness, K02 nine colour-bar styles, K03 palettes under colour-vision deficiency;
S01-S06 concept diagrams (see `schematics.md`); F01 complete 183 mm composite figure.
