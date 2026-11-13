# Concept diagrams with nature_schematic

Draw diagrams in matplotlib when they must match the data panels (fonts, line weights, colours) and stay
vector. For photo-real renders use a 3-D tool and add labels/arrows with this module on top.

## Canvas
```python
fig = plt.figure(figsize=figsize_mm(183, 60))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, 183, 60)     # 1 data unit = 1 mm on paper
```
Inside a composite figure, size the canvas to the axes: `p = ax.get_position(); canvas(ax, p.width * W_mm,
p.height * H_mm)` (see `F01_composite_figure.py`).

## Primitives
| Group | Functions |
|---|---|
| Boxes, arrows, text | `box` (returns anchors `.l .r .t .b .c`), `arrow`, `elbow`, `label`, `section_header`, `divider`, `brace`, `callout` (from nature_charts) |
| Optics | `beam`, `cone`, `lens`, `objective`, `beamsplitter`, `mirror`, `nd_filter`, `fiber`, `fiber_coil`, `camera` |
| Structures | `layer_stack`, `dimension`, `iso`, `iso_block`, `region_topview`, `random_field`, `periodic_field` |
| Data icons | `mini_plot`, `matrix_icon`, `image_icon` |
| Models | `nn_diagram`, `conv_blocks` |
| Sketch plots | `concept_axes` (arrow-headed axes, no numbers) |
| Composite | `zoom_connector` (dashed lines from a region to an inset panel) |

## Style
- Neutral grey components (`FILL`, `EDGE`), one coloured beam / flow, black signal arrows, dashed feedback.
- Arrows inside a stage grey; arrows that cross a stage boundary coloured.
- Label every component once, above or below it; never on top of a beam or arrow.
- One colour per material, identical in every view of the same structure.
- Use concept axes only when no numbers are claimed.

## Templates
`S01_flowchart`, `S02_optical_setup`, `S03_device_concept`, `S04_network`, `S05_concept_sketch`,
`S06_process_flow`, and the schematic band of `F01_composite_figure`.
