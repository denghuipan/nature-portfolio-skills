"""S02 -- Model architecture as a block diagram: inputs on the left, modules with block counts, coloured data
paths, residual junctions, a dashed recycling loop and an output preview.
Use when: describing a deep-learning (or any multi-stage computational) system; colours mark the different
streams, dashed lines the iterative parts, block counts sit inside the boxes.
Look: light grey rounded boxes with dark text, three stream colours used consistently (and named in a key),
circled-plus junctions, rounded orthogonal connectors, small embedded icons for inputs and outputs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
from nature_schematic import *  # noqa: F401,F403  mm-canvas diagram primitives
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
inputs = ["Source 1", "Source 2", "Source 3"]
modules = [("Embedder", "3 blocks"), ("Module A", "2 blocks"), ("Module B", "4 blocks"), ("Core", "48 blocks"),
           ("Decoder", "3 + 24 + 3 blocks"), ("Confidence", "4 blocks")]
# -------------------------------------------
c_a, c_b, c_c = PALETTE["ochre"], PALETTE["plum"], PALETTE["sage"]
W, H = 183, 62
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
rng = np.random.default_rng(5)
srcs = []
for i, nm in enumerate(inputs):
    srcs.append(cylinder(ax, 14, 43 - i * 13, 13, 9.5, nm, fc="#F5F5F5"))
emb = pbox(ax, 40, 17, 14, 24, modules[0][0], sub=modules[0][1])
for s, c in zip(srcs, (c_a, c_a, c_a)):
    route(ax, [s.r, (33, s.r[1]), (33, 29), (40, 29)], color=c, radius=1.5)
matrix_icon(ax, 57, 35.9, 6, 2.2, shape=(1, 10), cmap=NS_GREENS, grid_lw=0.3)
label(ax, 60, 39.5, "Inputs", size=0.9)
matrix_icon(ax, 57, 25.5, 6, 6, shape=(6, 6), cmap=NS_BLUES, grid_lw=0.2)
label(ax, 60, 24.0, "Pair", size=0.9, va="top")
matrix_icon(ax, 57, 10.9, 6, 2.2, shape=(1, 10), cmap=NS_SUNSET, grid_lw=0.3)
label(ax, 60, 9.4, "Single", size=0.9, va="top")
for yy in (37, 28.5, 12):
    route(ax, [(54, min(max(yy, 18), 40)), (56.6, yy)] if 18 <= yy <= 40 else [(54, 18), (55.3, 18), (55.3, yy), (56.6, yy)],
          color=c_a, head=3.5)
ma = pbox(ax, 74, 22, 14, 13, modules[1][0], sub=modules[1][1])
mb = pbox(ax, 94, 22, 14, 13, modules[2][0], sub=modules[2][1])
core = pbox(ax, 114, 14, 22, 29, modules[3][0], sub=modules[3][1])
dec = pbox(ax, 144, 9, 24, 15, modules[4][0], sub=modules[4][1])
conf = pbox(ax, 160, 46, 18, 11, modules[5][0], sub=modules[5][1])
for x in (69, 91, 111):
    plus_node(ax, x, 28.5, 1.0)
route(ax, [(63, 28.5), (68, 28.5)], color=c_b)
arrow(ax, (70, 28.5), ma.l, color=c_b); arrow(ax, ma.r, (90, 28.5), color=c_b)
arrow(ax, (92, 28.5), mb.l, color=c_b); arrow(ax, mb.r, (110, 28.5), color=c_b); arrow(ax, (112, 28.5), core.l, color=c_b)
route(ax, [(63, 37), (81, 37), (81, 35)], color=c_a, radius=1.2)
route(ax, [(63, 37), (101, 37), (101, 35)], color=c_a, radius=1.2)
route(ax, [(63, 12), (120, 12), (120, 14)], color=c_b, radius=1.2)
route(ax, [(136, 36), (156, 36), (156, 24)], color=c_b, radius=1.5)
route(ax, [(136, 36), (169, 36), (169, 46)], color=c_b, radius=1.5)
route(ax, [(136, 20), (144, 20)], color=c_b)
route(ax, [(168, 16.5), (173, 16.5), (173, 46)], color=c_c, radius=1.5)
route(ax, [(130, 14), (130, 4), (69, 4), (69, 27.5)], color=c_b, dashed=True, radius=1.5,
      label_text="Recycling", label_side="below", label_color=c_b)
route(ax, [(151, 9), (151, 5.5), (159, 5.5), (159, 9)], color=c_c, dashed=True, radius=1.2,
      label_text="Iterations", label_side="below", label_color=c_c)
for k, (nm, c) in enumerate((("Stream 1", c_a), ("Stream 2", c_b), ("Stream 3", c_c))):
    ax.plot([118 + k * 21, 123 + k * 21], [59.5, 59.5], color=c, lw=1.0)
    label(ax, 124.5 + k * 21, 59.5, nm, ha="left")
export(fig, "S02_architecture")
