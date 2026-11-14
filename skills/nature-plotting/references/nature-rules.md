# Nature-family artwork rules (checklist)

Sources (re-check before submission; journals update their pages):
- Nature research figure guide, *Building and exporting figure panels*:
  <https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/>
- Nature Photonics, *Formatting guide / artwork*:
  <https://www.nature.com/nphoton/submission-guidelines/aip-and-formatting>
- Crameri, Shephard & Heron, *The misuse of colour in science communication*, Nat. Commun. 11, 5444 (2020).

## Size
| Item | Rule | Helper |
|---|---|---|
| Single column | 89 mm wide | `figsize_1col()` |
| Double column | 183 mm wide (Nature Photonics states 180 mm max) | `figsize_2col()` |
| Height | <= 170 mm so the legend fits under the figure | `figsize_mm(w, h)` |
| Exact page size | save without tight bbox | `export(fig, name, exact=True)` |

## Type
- Sans serif (Arial), **5-7 pt** at final size; panel letters 8 pt bold lowercase (a, b, c). House rule:
  one size for all text (7 pt, `fs()`), so labels, ticks, legends and annotations match across panels.
- No text below 5 pt, including super/subscripts (`nature_style` floors mathtext at 5 pt).
- Symbol / Greek letters in the same face: `use_arial_math()`.
- Panel subtitles regular weight, short; do not repeat the axis label.
- Units in parentheses: `Time (s)`, `Intensity (a.u.)`.

## Colour and accessibility
- Avoid red/green combinations and rainbow scales; Nature asks for this explicitly.
- Keys and labels in the figure, not colour words in the caption ("open red triangles" only as a backup).
- Ordered data: sequential map with monotonic lightness; signed data: diverging map with a neutral centre.
- Check palettes with `simulate_cvd` (deutan / protan / tritan) or by printing in greyscale.

## Lines, markers, images
- Lines 0.25-1 pt in Extended Data (`ed_finish` clamps), data lines 1-1.5 pt in main figures.
- Error bars wherever appropriate; say what they are (s.d., s.e.m., 95 % CI) and n.
- Show individual data points when n is small.
- Images: >= 300 dpi at final size, scale bars (not magnifications), labels and scale bars as vector
  text, never flattened into the image; disclose any processing.

## Files
- Vector PDF for charts (editable text: `pdf.fonttype = 42`), PNG 600 dpi for preview.
- Extended Data: max 10 figures (Nature Photonics), one page each; `ed_tiff()` writes a TIFF <= 10 MB.
- Every quantitative panel traceable to a source-data table.

## Pre-submission QA
1. `export()` prints text outside 5-8 pt.
2. Look at the rendered PNG of every figure at 100 % zoom.
3. `python scripts/audit_layout.py figure.pdf` -- page size, fonts, sizes, panel letters, frame alignment,
   raster dpi, hairlines, text outside the page.
