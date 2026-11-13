"""C02 -- Grouped bars (two factors) and 100 % stacked bars (composition).
Use when: (a) a metric for several methods across several datasets; (b) how a total splits into parts.
Nature notes: <= 4 series per group; legend in one row above the bars; stacked segments carry their value
inside when there is room.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
datasets = ["Dataset 1", "Dataset 2", "Dataset 3", "Dataset 4"]
methods = ["Method A", "Method B", "Method C (ours)"]
vals = np.array([[0.62, 0.41, 0.35, 0.30], [0.80, 0.66, 0.58, 0.55], [0.99, 0.97, 0.98, 0.95]])
errs = np.array([[0.05, 0.06, 0.05, 0.07], [0.04, 0.05, 0.06, 0.06], [0.01, 0.02, 0.01, 0.02]])
cats = ["Condition 1", "Condition 2", "Condition 3", "Condition 4"]
parts = {"Part 1": [52, 38, 61, 20], "Part 2": [30, 22, 18, 10], "Part 3": [8, 6, 9, 5], "Part 4": [10, 34, 12, 65]}
# -------------------------------------------

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_2col(56), gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.55))
colors = ["#BDBDBD", PALETTE["lightblue"], PALETTE["red"]]
grouped_bars(a, datasets, methods, vals, err=errs, colors=colors, width=0.78, legend=False)
a.legend([mpl.patches.Patch(fc=c, ec=darken(c, 0.25), lw=0.5) for c in colors], methods, loc="lower left",
         bbox_to_anchor=(0, 1.0), ncols=3, handlelength=1.0, columnspacing=0.8)
a.set_ylim(0, 1.08); a.set_ylabel("Score")
style_axes(a); a.tick_params(axis="x", which="both", bottom=False, top=False)
stacked_barh(b, cats, parts, colors=[PALETTE["blue"], PALETTE["skyblue"], PALETTE["mint"], PALETTE["salmon"]])
b.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncols=4, handlelength=1.0, columnspacing=0.8)
b.set_xlabel("Share (%)")
style_axes(b); b.tick_params(axis="y", which="both", left=False, right=False)
panel_label(a, "a", dx=-0.2, dy=1.2); panel_label(b, "b", dx=-0.38, dy=1.2)
export(fig, "C02_grouped_stacked")
