"""L05 -- Metric vs condition for several methods, with percentile bands, an extrapolated segment and a
special marker.
Use when: comparing methods across conditions with uncertainty from resampling (5-95 % of subsets).
Nature notes: say what the band is in the legend; dashed segment = beyond the measured / validated range;
one distinct marker for a special condition.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.array([1, 2, 3, 4, 5.0])
methods = {"Method A": (np.array([1.6e-2, 1.9e-2, 3.5e-2, 7e-2, 2.0e-1]), "0.45", "s"),
           "Method B": (np.array([8e-2, 8.5e-2, 1.1e-1, 2e-1, 5e-1]), "#B08850", "v"),
           "Method C": (np.array([1.2e-4, 1.3e-4, 1.6e-4, 4.5e-4, 4.0e-3]), "#5B2C91", "o")}
special = {"Method A": 1.8e-1, "Method B": 4.6e-1, "Method C": 3.0e-3}      # e.g. averaged repeat at x = 5
# -------------------------------------------

from matplotlib.lines import Line2D
fig, ax = plt.subplots(figsize=figsize_1col(60))
handles = []
for name, (y, c, m) in methods.items():
    lo, hi = y / 1.8, y * 1.8
    ci_band(ax, x[:-1], lo[:-1], hi[:-1], c, alpha=0.18)
    ci_band(ax, x[-2:], lo[-2:], hi[-2:], c, alpha=0.10)
    ax.plot(x[:-1], y[:-1], "-" + m, color=c, ms=2.8, lw=1.0, zorder=3)
    ax.plot(x[-2:], y[-2:], "--", color=c, lw=1.0, zorder=3)
    ax.plot(x[-1], special[name], "D", ms=4.2, mfc=c, mec="k", mew=0.5, zorder=5)
    handles.append(Line2D([], [], color=c, marker=m, ms=2.8, lw=1.0, label=name))
handles.append(Line2D([], [], ls="none", marker="D", ms=4, mfc="0.6", mec="k", mew=0.5, label="Averaged"))
handles.append(mpl.patches.Patch(color="0.6", alpha=0.25, lw=0, label="5–95 % of subsets"))
ax.set_yscale("log"); ax.set_ylim(5e-5, 30); log_ticks(ax.yaxis)
ax.set_xlim(0.6, 5.6); ax.set_xticks(x, [f"C{int(v)}" for v in x])
regime(ax, 4.2, 5.6, color="0.3", alpha=(0.0, 0.45))
ax.legend(handles=handles, loc="upper left", ncols=2, handlelength=1.6, columnspacing=0.8)
ax.set_xlabel("Condition"); ax.set_ylabel("Error (a.u.)")
style_axes(ax); ax.tick_params(axis="x", which="minor", bottom=False, top=False)
export(fig, "L05_ci_band")
