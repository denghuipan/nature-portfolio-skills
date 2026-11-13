"""D01 -- Box plot with every observation overlaid (jittered strip).
Use when: comparing distributions of a metric across a few groups, n >= ~10 per group.
Nature notes: say what the box and whiskers are (median, IQR, 5-95 %) in the panel; never show a box alone
when the points fit; use a log axis when the spread covers decades.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(31)
groups = ["Group 1", "Group 2", "Group 3"]
data = [np.abs(rng.normal(0.10, 0.045, 300)), np.abs(rng.normal(0.11, 0.05, 300)),
        np.abs(rng.normal(0.135, 0.055, 300))]
colors = [PALETTE["blue"], PALETTE["green"], PALETTE["red"]]
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(60, 56))
pos = np.arange(1, 4)
boxplot(ax, data, pos, colors, width=0.55, alpha=0.45)
for p, d, c in zip(pos, data, colors):
    jitter(ax, p, d, c, width=0.17, size=4, alpha=0.35, hollow=True)
ax.set_xticks(pos, groups); ax.set_ylim(0, 0.34); ax.set_ylabel("Value (unit)")
stats_text(ax, ["box: median, IQR", "whiskers: 5–95 %", "n = 300 per group"], loc="upper left")
style_axes(ax); ax.tick_params(axis="x", which="both", bottom=False, top=False)
export(fig, "D01_box_jitter")
