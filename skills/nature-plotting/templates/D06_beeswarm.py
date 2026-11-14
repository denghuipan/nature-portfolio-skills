"""D06 -- Beeswarm per group with median and interquartile range: every observation visible, no overlap.
Use when: n per group is between ~15 and ~300 and reviewers expect to see each data point (biology,
clinical measurements, per-sample metrics).
Look: open axes, swarms in muted group colours, a black median bar with IQR whiskers drawn beside the swarm,
n on the second tick line, a dashed reference level.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(31)
groups = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5"]
data = [rng.lognormal(np.log(m), 0.35, n) for m, n in [(1.0, 60), (1.4, 45), (2.2, 80), (1.1, 30), (3.1, 52)]]
# -------------------------------------------
cols = [PALETTE["grey"], PALETTE["sky"], PALETTE["blue"], PALETTE["peach"], PALETTE["brick"]]
fig, ax = plt.subplots(figsize=figsize_mm(89, 58))
fig.subplots_adjust(left=0.12, right=0.98, bottom=0.2, top=0.96)
for i, (d, c) in enumerate(zip(data, cols)):
    beeswarm(ax, i, d, c, width=0.3, s=5)
    q1, m, q3 = np.percentile(d, [25, 50, 75])
    ax.plot([i - 0.3, i + 0.3], [m, m], color="0.1", lw=1.2, zorder=5, solid_capstyle="butt")
    ax.plot([i + 0.36, i + 0.36], [q1, q3], color="0.1", lw=0.7, zorder=5)
ax.axhline(1.0, color="0.45", lw=0.5, ls=(0, (3, 2)), zorder=0)
ax.set_xticks(range(len(groups))); n_ticklabels(ax, groups, [len(d) for d in data])
ax.tick_params(axis="x", length=0)
ax.set_yscale("log"); ax.set_ylim(0.3, 10)
ax.set_yticks([0.3, 1, 3, 10], ["0.3", "1", "3", "10"]); ax.yaxis.set_minor_locator(mticker.NullLocator())
ax.set_ylabel("Fold change")
export(fig, "D06_beeswarm")
