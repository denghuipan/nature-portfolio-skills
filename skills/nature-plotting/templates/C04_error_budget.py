"""C04 -- Budget of contributions: one horizontal stacked bar per configuration, the residual hatched.
Use when: a total (error, loss, cost, energy, time) is broken into named contributions for a few
configurations, and part of it is unexplained or estimated.
Look: open bottom axis only, bars without outlines, a hatched segment for the residual, contribution names
under the first bar, totals written at the bar ends, dots + line for measured totals on top.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
configs = ["Config. 1", "Config. 2", "Config. 3"]
parts = ["Source A", "Source B", "Source C", "Source D", "Unexplained"]
vals = np.array([[0.62, 0.28, 0.14, 0.09, 0.07],
                 [0.41, 0.25, 0.12, 0.07, 0.05],
                 [0.22, 0.19, 0.10, 0.05, 0.04]])        # e.g. error per step (%)
measured = np.array([1.24, 0.92, 0.61]); measured_e = np.array([0.05, 0.04, 0.03])
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["sky"], PALETTE["teal"], PALETTE["mint"], "white"]
fig, ax = plt.subplots(figsize=figsize_mm(89, 46))
fig.subplots_adjust(left=0.17, right=0.95, bottom=0.27, top=0.86)
y = np.arange(len(configs))[::-1]
for r, (yy, row) in enumerate(zip(y, vals)):
    left = 0.0
    for k, (v, c) in enumerate(zip(row, cols)):
        hatch = "////" if parts[k] == "Unexplained" else None
        ax.barh(yy, v, left=left, height=0.52, color=c, lw=0.5 if hatch else 0,
                edgecolor="0.35" if hatch else "none", hatch=hatch)
        left += v
    ax.text(left + 0.03, yy, f"{left:.2f}", va="center", fontsize=6)
from matplotlib.patches import Rectangle as _R
hs = [_R((0, 0), 1, 1, color=c, lw=0) for c in cols[:4]] + [_R((0, 0), 1, 1, fc="white", ec="0.35", hatch="////", lw=0.5)]
ax.legend(hs, parts, loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncols=5, handlelength=0.9, handleheight=0.9,
          columnspacing=0.7, handletextpad=0.3)
ax.errorbar(measured, y - 0.42, xerr=measured_e, fmt="o", ms=2.6, color="k", elinewidth=0.6, zorder=5)
ax.text(measured[-1] + 0.06, y[-1] - 0.42, "Measured", va="center", fontsize=6)
ax.set_yticks(y, configs); ax.tick_params(axis="y", length=0)
despine(ax, left=True)
ax.set_xlim(0, 1.45); ax.set_ylim(-0.75, 2.75)
ax.set_xlabel("Error per step (%)")
export(fig, "C04_error_budget")
