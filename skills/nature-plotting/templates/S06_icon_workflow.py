"""S06 -- Visual-abstract workflow: samples -> measurements -> data matrix -> model -> results, as icons.
Use when: a one-line overview at the top of a figure or a graphical abstract; each step is one small
picture with a two-word caption, the experimental and computational halves are bracketed.
Look: no boxes, icons of equal height on one baseline, thin grey arrows, captions under icons, two braces
below naming the halves, a single accent colour for the result.
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
steps = ["Samples\n(n = 96)", "Measurements", "Data matrix", "Model", "Prediction"]
# -------------------------------------------
W, H = 183, 40
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
y0, h = 17, 15
xs = [8, 44, 80, 113, 150]
icon_cells(ax, xs[0], y0, 22, h, n=16, color=PASTEL["teal"][1], seed=6)
icon_stack(ax, xs[1], y0, 17, h - 2, n=4)
matrix_icon(ax, xs[2], y0, 20, h, shape=(9, 12), cmap=NS_SEAFLOOR, grid_lw=0.25)
nn_diagram(ax, xs[3], y0, 24, h, layers=(5, 7, 7, 3), edge_lw=0.2)
mini_plot(ax, xs[4], y0, 24, h, np.linspace(0, 1, 60), np.exp(-((np.linspace(0, 1, 60) - 0.6) / 0.15) ** 2),
          color=PALETTE["blue"], frame=True, ticks=3)
rights = [xs[0] + 22, xs[1] + 20, xs[2] + 20, xs[3] + 24]
for r, nxt in zip(rights, xs[1:]):
    arrow(ax, (r + 2, y0 + h / 2), (nxt - 2.5, y0 + h / 2), color="0.45")
centres = [xs[0] + 11, xs[1] + 10, xs[2] + 10, xs[3] + 12, xs[4] + 12]
for x, t in zip(centres, steps):
    label(ax, x, y0 - 1.5, t, va="top", size=1.0, linespacing=1.1)
brace(ax, xs[0], xs[1] + 20, 7.0, "Experiment", up=False, height=1.6)
brace(ax, xs[2], xs[4] + 24, 7.0, "Computation", up=False, height=1.6)
export(fig, "S06_icon_workflow")
