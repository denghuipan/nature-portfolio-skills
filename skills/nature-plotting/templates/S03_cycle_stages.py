"""S03 -- An iterative loop drawn as a cycle, next to the same work as ordered stages with icons.
Use when: the method is a closed loop (design-build-test-learn, active learning, closed-loop control) and
also has a one-pass reading for the reader who wants the order of operations.
Look: a ring of pastel nodes joined by curved arrows with step numbers inside and names outside, a short
note in the middle; right: chevron stages in the same colours with small icons and captions underneath.
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
steps = ["Design", "Prepare", "Measure", "Analyse", "Select"]
captions = ["Propose\nvariants", "Make\nsamples", "Collect\ndata", "Fit\nmodel", "Rank and\nchoose"]
centre_note = "5 rounds\n× 96 samples"
# -------------------------------------------
cols = ["blue", "teal", "green", "orange", "purple"]
W, H = 183, 62
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
cycle_diagram(ax, 32, 31, 17, steps, colors=[PASTEL[c][1] for c in cols], node_text=[str(i + 1) for i in range(5)],
              node_r=4.0)
label(ax, 32, 31, centre_note, size=1.0, color="0.3", linespacing=1.2)
label(ax, 2, 59, "a", ha="left", va="top", size=1.33, fontweight="bold")
label(ax, 74, 59, "b", ha="left", va="top", size=1.33, fontweight="bold")
ch = chevrons(ax, 80, 40, 100, 9, steps, colors=[PASTEL[c][0] for c in cols], tip=2.5, gap=0.8)
for b, c in zip(ch, cols):
    ax.add_patch(plt.Polygon([(b.x, b.y), (b.x + b.w - 2.5, b.y)], closed=False, ec=PASTEL[c][1], lw=0.8))
icx = [b.x + (b.w - 2.5) / 2 for b in ch]
icon_stack(ax, icx[0] - 4.5, 22, 7, 9, n=3)
icon_cells(ax, icx[1] - 5.5, 22, 11, 9, n=10, color=PASTEL["teal"][1])
icon_bars(ax, icx[2] - 5, 22, 10, 9, colors=[PASTEL["green"][1]] * 4)
mini_plot(ax, icx[3] - 5, 22, 10, 9, np.linspace(0, 1, 50), 1 - np.exp(-4 * np.linspace(0, 1, 50)),
          color=PASTEL["orange"][1], frame=True, ticks=0)
icon_graph(ax, icx[4] - 4.5, 22, 9, color=PASTEL["purple"][1], seed=7)
for x, cap in zip(icx, captions):
    label(ax, x, 18.5, cap, va="top", size=1.0, linespacing=1.15)
brace(ax, 80, 180, 7.5, "One round", height=1.6, up=False)
export(fig, "S03_cycle_stages")
