"""M06 -- Parameter sweep as filled contours with labelled contour lines, a constraint and the optimum.
Use when: a figure of merit over two design parameters; the claim is where the optimum / feasible region is.
Nature notes: a few labelled contour lines carry the numbers; the infeasible side of a constraint is hatched or
greyed; the chosen design point is the only coloured marker.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
p1 = np.linspace(0, 10, 200); p2 = np.linspace(0, 6, 150)
P1, P2 = np.meshgrid(p1, p2)
F = np.exp(-((P1 - 6.2) / 2.6) ** 2 - ((P2 - 3.4) / 1.6) ** 2) + 0.25 * np.exp(-((P1 - 2) / 1.5) ** 2 - ((P2 - 1) / 1) ** 2)
constraint = 0.5 * p1 + 0.6                                  # feasible below this line
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(80, 60))
lv = np.linspace(0, 1, 11)
cf = ax.contourf(P1, P2, F, levels=lv, cmap=NS_GLACIER.reversed())
cs = ax.contour(P1, P2, F, levels=[0.2, 0.5, 0.8], colors="k", linewidths=0.5)
ax.clabel(cs, fmt="%.1f", fontsize=5.5, inline_spacing=2)
ax.fill_between(p1, constraint, 6, color="w", alpha=0.55, lw=0, hatch="////", edgecolor="0.5")
ax.plot(p1, constraint, color="0.25", lw=0.8)
direct_label(ax, 9.6, 5.25, "infeasible", color="0.25", ha="right", va="bottom")
i, j = np.unravel_index(np.argmax(np.where(P2 < 0.5 * P1 + 0.6, F, -1)), F.shape)
ax.plot(P1[i, j], P2[i, j], "*", ms=8, mfc=PALETTE["red"], mec="k", mew=0.5, zorder=5)
direct_label(ax, P1[i, j], P2[i, j], "optimum", color=PALETTE["red"], dx=-5, dy=4, ha="right", va="bottom")
ax.set_xlabel("Parameter 1 (unit)"); ax.set_ylabel("Parameter 2 (unit)")
cbar_side(ax, cf, "Figure of merit", ticks=[0, 0.5, 1])
style_axes(ax)
export(fig, "M06_contour_sweep")
