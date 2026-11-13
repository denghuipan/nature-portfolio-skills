"""S04 -- Neural-network sketches: fully connected (a) and convolutional block diagram (b).
Use when: the model architecture must be shown (Methods / Extended Data), not just named.
Nature notes: input and output layers in the colours of the data they represent; layer sizes under the
blocks; arrows only between stages, not between every block.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

W, H = 183, 56
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
label(ax, 2, 54, "a", ha="left", va="top", size=8 / 6, fontweight="bold")
cols = nn_diagram(ax, 10, 8, 56, 38, layers=(6, 9, 9, 7, 4))
for (xk, ys), name in zip(cols, ["Input", "Hidden 1", "Hidden 2", "Hidden 3", "Output"]):
    label(ax, xk, 4, name, va="top", size=0.95)

label(ax, 78, 54, "b", ha="left", va="top", size=8 / 6, fontweight="bold")
specs = [dict(w=2.5, h=30, d=14, color="#D9D9D9", label="Input"),
         dict(w=3.5, h=26, d=12, color="#8EA9CC", label="Conv 1"),
         dict(w=5, h=20, d=10, color="#6E8FC0", label="Conv 2"),
         dict(w=6.5, h=14, d=8, color="#4F72AE", label="Conv 3"),
         dict(w=3, h=22, d=1.5, color="#A99BC8", label="Dense"),
         dict(w=3, h=12, d=1.5, color=PALETTE["red"], label="Output")]
boxes = conv_blocks(ax, 86, 12, specs, gap=6.5)
for b0, b1 in zip(boxes[:-1], boxes[1:]):
    arrow(ax, (b0.x + b0.w + 0.6, 12 + 15), (b1.x - 0.6, 12 + 15), head=4, lw=0.8, color="0.35")
label(ax, 132, 50, "kernel 3 × 3, stride 1; pooling ×2 between blocks", size=0.95, color="0.35")
export(fig, "S04_network", exact=True)
