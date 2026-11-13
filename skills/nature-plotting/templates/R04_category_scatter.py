"""R04 -- Scatter of several categories, one marker shape + colour each, with a graded region.
Use when: individual results of several sample types plotted against a common axis.
Nature notes: shape AND colour per category (survives greyscale / colour blindness); legend with the n of
each category; the region beyond a limit shaded as a gradient and labelled once.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(44)
cats = {"Type 1": ("o", PALETTE["blue"]), "Type 2": ("s", PALETTE["red"]), "Type 3": ("D", PALETTE["green"]),
        "Type 4": ("^", "#5B2C91")}
pts = {k: (rng.uniform(1, 9, 9), np.clip(1 - np.abs(rng.normal(0, 0.03 + 0.02 * i, 9)), 0.5, 1))
       for i, k in enumerate(cats)}
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(70, 52))
regime(ax, 7.5, 10, color="0.3", alpha=(0.0, 0.45), label="beyond\nlimit", label_rot=0, label_x=8.8)
for k, (m, c) in cats.items():
    xs, ys = pts[k]
    ax.plot(xs, ys, m, color=c, ms=3.4, mec="w", mew=0.4, ls="none", label=f"{k} ({xs.size})", zorder=3)
ax.set_xlim(0, 10); ax.set_ylim(0.5, 1.05)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Score")
ax.legend(loc="lower left", ncols=2, handletextpad=0.2, columnspacing=0.8)
style_axes(ax)
export(fig, "R04_category_scatter")
