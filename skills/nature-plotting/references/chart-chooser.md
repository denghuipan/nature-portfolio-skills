# Chart chooser

Choose by the question the panel answers. Each row names the template (in `templates/`), the main
builder functions it uses, and the usual alternative.

## Trends and time series (T)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Measurements vs a model over a size parameter, then extrapolation | T01 | `legend_box`, `dashed_frame`, `arrow_note`, `set_look("framed")` | R01 if residuals matter |
| Projections under scenarios with ensemble spread | T02 | `fan`, `share_labels` | T03 for two methods |
| Score vs budget / samples / dose for two methods | T03 | `fill_between`, `sig_bracket(vertical=True)` | N03 for many sizes |
| Count growing over time, sources change | T04 | `thousands`, `square_legend` | T06 for >2 sources |
| Each item changes between two times | T05 | `despine` | C10 dumbbell |
| Composition of a total over time | T06 | `area_stack`, `end_labels` | C08 for one time |
| Noisy series, events, intervention window | T07 | `set_look("grid")`, annotate | small multiples (T02 b) |
| Continuous trace with discrete events and states | T08 | `vlines`, scale bars | M08 for spectra |

## Comparisons (C)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| One method vs baselines on several benchmark families | C01 | `bars`, `sig_bracket`, `n_ticklabels`, `square_legend` | C05 for many entries |
| A subset inside a larger set, by category | C02 | `overlay_bars`, `thousands` | stacked bars |
| Matched halves (left/right, before/after) per category | C03 | `butterfly`, `bracket_label` | C10 |
| Contributions to a total, some unexplained | C04 | `barh` with hatch | waterfall (`waterfall`) |
| 10-40 entries ranked by an estimate with CI | C05 | dots + interval lines | C01 bars when few |
| Subgroup effects, numbers needed | C06 | squares by weight, pooled diamond | `forest` (no table) |
| Exact values plus the overall pattern | C07 | `zebra_table`, `highlight_points` | table in Extended Data |
| Part of a whole | C08 | `donut`, `waffle`, 100% bars | T06 over time |
| Two sets across long-named categories | C09 | `barh`, `percent` | C01 |
| Two conditions per item, size of change | C10 | dumbbells sorted by change | T05 |
| Ranking with lollipops, grouped / stacked bars, radar | -- | `lollipop`, `grouped_bars`, `stacked_barh`, `radar` | -- |

## Distributions (D)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Shape per group, with tests | D01 | `violinplot`, `jitter`, `sig_bracket` | D06 beeswarm |
| Fit a model to a distribution | D02 | `hist` + scipy fit, `stats_text` | D04 |
| Two populations of very different size | D03 | `stairs` (no fill), log y | density ratio |
| Compare error distributions without binning | D04 | `ecdf`, quantile dots | box plot |
| Distribution drift over ordered conditions | D05 | KDE ridges, sequential colours | D01 |
| Show every observation (n 15-300) | D06 | `beeswarm` | D01 |
| Paired measurements | D07 | `paired_lines`, `beeswarm` | C10 |
| Overlapping 2-D clouds | D08 | probability-mass contours, marginals | hexbin |

## Relationships (R)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Agreement of thousands of points, detail in one corner | R01 | `zoom_to` | R06 |
| Trend of a noisy / binary outcome | R02 | `binned_stat` | logistic fit |
| Units of different size vs two drivers | R03 | `cbar_below`, `size_legend`, `stats_text` | R07 |
| Many features tested at once | R04 | `volcano` | M01 |
| Embedding with clusters and a property | R05 | `cbar_inset`, centroid labels | -- |
| Prediction vs reference | R06 | `hexbin(bins="log")`, inset histogram | `parity` |
| Relationship fitted per group | R07 | OLS + CI, `end_labels` | interaction plot |
| Two criteria, target region | R08 | quadrant lines, `annotate` | `landscape` |

## Matrices, fields, images (M)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Two quantities per cell (fraction + level) | M01 | `dot_matrix`, `size_legend` | heat map |
| Clustered samples x features with known groups | M02 | scipy dendrogram, group strip | `heatmap` |
| Pairwise correlations | M03 | circles + numbers | `corr_triangle` |
| Classifier on imbalanced classes | M04 | row-normalised matrix + support bars | per-class bars |
| Gridded change with significance | M05 | `pcolormesh`, stipple, `cbar_below` | contour map |
| Micrographs by condition and channel | M06 | `scale_bar`, merge, zoom | -- |
| Angles, directions, phases, hours | M07 | polar bars, resultant vector | linear histogram (avoid) |
| Spectral content over time | M08 | `spectrogram`, `cbar_side` | wavelet map |

## Machine learning (N)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Training history over seeds | N01 | thin seeds + bold mean | `ci_band` |
| Detection with rare positives | N02 | ROC + PR, operating points | N04 |
| Loss vs compute across model sizes | N03 | discrete colour bar, frontier fit | T03 |
| Calibration of probabilities | N04 | reliability bars + counts | -- |

## Biomedical (B)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Time-to-event between arms | B01 | `km_curve`, `at_risk_table` | cumulative incidence |
| Potency of compounds | B02 | `mean_sem`, `hill`, `fit_hill` | -- |
| Repeated measures over time + summary | B03 | `mean_sem`, `p_to_stars`, `bars(points=)` | mixed-model estimates |

## Flows and networks (G)
| Question | Template | Builders | Alternative |
|---|---|---|---|
| Movement between categories across stages | G01 | `alluvial` | transition matrix (M02) |
| Small weighted network | G02 | `node_link`, `bracket_label` | adjacency heat map |

## Colour and looks (K)
K01 colour maps and L*, K02 colour-bar layouts, K03 palettes under CVD, K04 the four axis looks.

## Diagrams (S) and composite (F)
| Question | Template | Builders |
|---|---|---|
| Method overview with branches, store and loop | S01 | `group_frame`, `pbox`, `cylinder`, `circle_node`, `route` |
| Model / system architecture | S02 | `pbox`, `plus_node`, `matrix_icon`, `route(radius=)` |
| Iterative loop and its stages | S03 | `cycle_diagram`, `chevrons`, icons |
| Study design and visit schedule | S04 | `icon_person`, `timeline` |
| Qualitative concept sketches | S05 | `concept_axes`, translucent sets |
| Visual abstract workflow | S06 | icons, `brace` |
| Full page | F01 | one gridspec + mm canvas |
