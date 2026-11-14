"""C08 -- Part of a whole three ways: donut, 100% stacked bars per group, waffle.
Use when: shares of a total (cohort composition, class balance, sources). Donut for one total with <= 5
parts; 100% bars to compare compositions across groups; waffle when counts out of 100 read better than angles.
Look: white separators, no outlines, direct percentages, the same colours for the same parts in all three.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
parts = ["Part 1", "Part 2", "Part 3", "Part 4"]
whole = [46, 27, 17, 10]
groups = ["Group A", "Group B", "Group C", "Group D"]
comp = np.array([[52, 24, 14, 10], [38, 31, 19, 12], [61, 18, 13, 8], [29, 35, 22, 14]])
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["sky"], PALETTE["ochre"], PALETTE["lightgrey"]]
fig = plt.figure(figsize=figsize_2col(56))
a = fig.add_axes([0.0, 0.08, 0.26, 0.8])
b = fig.add_axes([0.38, 0.2, 0.3, 0.68])
c = fig.add_axes([0.74, 0.12, 0.2, 0.74])
donut(a, whole, cols, labels=parts, center_text="n = 1,240")
y = np.arange(len(groups))[::-1]
left = np.zeros(len(groups))
for k, (p, col) in enumerate(zip(parts, cols)):
    b.barh(y, comp[:, k], left=left, color=col, height=0.62, lw=0.8, edgecolor="white")
    for yi, l, v in zip(y, left, comp[:, k]):
        if v >= 12:
            b.text(l + v / 2, yi, f"{v}", ha="center", va="center", fontsize=6,
                   color="white" if k == 0 else "0.1")
    left += comp[:, k]
b.set_yticks(y, groups); b.tick_params(axis="y", length=0)
b.set_xlim(0, 100); b.set_xlabel("Share (%)"); despine(b, left=True)
square_legend(b, parts, cols, loc="lower left", bbox=(0.0, 1.0), ncols=4, columnspacing=0.8)
waffle(c, whole, cols, labels=None, legend=False)
c.set_title("Each square = 1%", fontsize=6, color="0.35", pad=3)
fig.text(0.0, 0.99, "a", fontsize=8, fontweight="bold", va="top")
fig.text(0.3, 0.99, "b", fontsize=8, fontweight="bold", va="top")
fig.text(0.72, 0.99, "c", fontsize=8, fontweight="bold", va="top")
export(fig, "C08_part_of_whole")
