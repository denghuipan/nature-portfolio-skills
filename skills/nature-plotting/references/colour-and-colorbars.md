# Colour maps, palettes and colour bars

All maps live in `assets/nature_cmaps.py` and are registered with matplotlib (`cmap="ns_ember"`, reversed
`"ns_ember_r"`). Previews: `gallery/K01_colormaps.png`, `K02_colorbar_styles.png`, `K03_palettes_cvd.png`,
`K04_axis_looks.png`.

## Which map

| Data | Map | Notes |
|---|---|---|
| Magnitude, light = low (errors, counts on white) | `NS_BLUES`, `NS_REDS`, `NS_GREENS`, `NS_PURPLES`, `NS_SUNSET` | single hue; SUNSET for error maps |
| Intensity images, camera frames, spectrograms | `NS_EMBER` (or `magma` / `inferno`) | dark = low |
| Densities, hexbins, maps on white pages | `NS_SEAFLOOR`, `NS_GLACIER` (reversed: light = low) | |
| Third variable on a scatter / bubble plot, ordered classes | `NS_DUSK` | light yellow = low, indigo = high |
| Signed values around a reference | `NS_DIV_BR`, `NS_DIV_PG`, `NS_DIV_BO` + `center_norm` | PG and BO avoid red-blue if those mean something else |
| Signed values on a black image plate | `NS_DIV_DARK` | dark centre |
| Angle, phase, orientation | `NS_PHASE` (or `twilight`) | ends match |
| True visible colour of a wavelength | `NS_VISIBLE`, `wavelength_rgb(nm)` | 380-780 nm |
| Binned or categorical field | `discrete_cmap(cmap, n)` / `cbar_discrete` | |

Checks: `lightness(cmap)` returns CIE L*; `is_monotonic(cmap)` must be True for sequential maps.
`truncate_cmap(cmap, lo, hi)` drops the near-white end when the map colours lines.

## Palettes for series
| Palette | Use |
|---|---|
| `EDITORIAL` (= `HOUSE` = `CYCLE`) | default series colours: blue, ochre, teal, plum, brick, sage, rose, grey |
| `HOUSE_DARK` | thin lines and coloured text on white |
| `OKABE_ITO` | > 4 categories that must be separable by colour alone |
| `PAIRED` | light/dark pairs: raw vs processed, train vs test, reference vs new |
| `THEMES["duo_purple" / "duo_blue" / "duo_teal"]` | two tones of one hue: reference set vs new set (bars, step histograms) |
| `THEMES["soft"]` | pastel blue for the method of interest + greys for baselines (benchmark bars) |
| `THEMES["fan"]` | scenario fans (low / mid / high) |
| `THEMES["signal"]` | hollow-marker trio for measurement variants vs a black model line |
| `THEMES["updown"]` | up / down / not significant (volcano, gains vs losses, slopegraphs) |
| `THEMES["earth"]` | field and ecology categories |
| `METHOD_COLORS` | fixed roles: method of interest blue, baselines grey, reference black |
| `PASTEL` (schematic) | fill / edge pairs for diagram boxes and frames |

`set_look("classic")` switches `PALETTE` / `CYCLE` to the older bright set (blue #2C6AB4, red #E84143 ...)
for papers already drawn in that style.

`simulate_cvd(rgb, "deutan" | "protan" | "tritan")` shows what readers with colour-vision deficiency see.

## Colour-bar styles (K02)
| Style | Helper | When |
|---|---|---|
| Slim side bar, extend triangles | `cbar_side(ax, im, label, extend="max")` | default; clipped ranges get triangles |
| Inset horizontal bar, label above | `cbar_inset(ax, im, label, loc=...)` | key would waste a column |
| Bar on top | `cbar_top(ax, im, label)` | wide, short maps |
| One bar for several panels | `cbar_span(fig, axes, im, label)` | shared norm across panels |
| Binned | `cbar_discrete(ax, cmap, bounds=[...])` | thresholds / classes of a continuous value |
| Categorical | `cbar_discrete(ax, cmap, categories=[...])` | named classes |
| Logarithmic | `LogNorm` + `cbar_side` (+ `log_ticks`) | values over decades |
| Diverging, centre pinned | `center_norm(vmin, 0, vmax)` + `cbar_side` | asymmetric signed ranges |
| End labels | `cbar_endlabels(cb, "0", "max")` | per-image normalised displays |
| Line family | `sm, col = line_mappable(cmap, lo, hi)` + `cbar_side(ax, sm)` | curves coloured by a parameter |
| Under a scatter | `cbar_below(ax, sc, label)` | third variable coloured on a scatter / bubble plot |
| Bubble sizes | `size_legend(ax, values, sizes, title)` | marker area encodes a quantity |
| Wavelength strip | `spectrum_strip(ax)` (true colour) | colour key along a wavelength axis |

Rules: label = quantity (unit); short outward ticks; hair-line outline (`style_cbar`); no more than 3-5
tick labels; a side bar is as tall as its panel, a horizontal bar is shorter than the panel width.
