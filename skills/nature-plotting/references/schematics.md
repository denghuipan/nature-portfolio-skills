# Concept diagrams with nature_schematic

Draw diagrams in matplotlib when they must match the data panels (fonts, line weights, colours) and stay
vector. For photo-real renders use a 3-D tool and add labels/arrows with this module on top.

## Canvas
```python
fig = plt.figure(figsize=figsize_mm(183, 60))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, 183, 60)     # 1 data unit = 1 mm on paper
```
Inside a composite figure, give the diagram its own axes with the same mm size as its share of the page
(see `F01_composite_figure.py`: `fig.add_axes([0, 0.79, 1, 0.21])` with `canvas(ax, 183, 31.5)`).

## Primitives
| Group | Functions |
|---|---|
| Blocks | `pbox` (pastel fill + edge from `PASTEL`), `box` (anchors `.l .r .t .b .c`), `group_frame` (rounded coloured frame with a title), `cylinder` (database / store), `circle_node`, `plus_node` (residual sum) |
| Connectors | `arrow`, `elbow`, `route` (orthogonal, rounded corners, dashed loops, labels), `brace`, `zoom_connector` |
| Sequences | `chevrons` (ordered stages), `cycle_diagram` (closed loop), `timeline` (visits, schedule) |
| Icons | `icon_graph`, `icon_stack`, `icon_bars`, `icon_person`, `icon_cells`, `matrix_icon`, `mini_plot`, `image_icon` |
| Models | `nn_diagram`, `conv_blocks` |
| Text | `label`, `section_header`, `divider` |
| Sketch plots | `concept_axes` (arrow-headed axes, no numbers) |
| Line art | `beam`, `cone`, `lens`, `objective`, `beamsplitter`, `mirror`, `nd_filter`, `fiber`, `fiber_coil`, `camera`, `layer_stack`, `dimension`, `iso_block` |

## Style
- Light pastel boxes with a slightly darker edge of the same hue, dark text, block counts or details as a
  grey second line; at most four box colours, one per module family.
- Stream colours (data paths) are separate from box colours and named in a small key.
- Feedback, recycling and repetition are dashed, with a short label on the longest segment.
- Group frames are white with a coloured rounded edge and the group title centred above.
- Label every component once, above or below it; never on top of an arrow.
- Use concept axes only when no numbers are claimed.

## Templates
`S01_pipeline_loop`, `S02_architecture`, `S03_cycle_stages`, `S04_study_design`, `S05_concept_sketches`,
`S06_icon_workflow`, and the schematic band of `F01_composite_figure`.
