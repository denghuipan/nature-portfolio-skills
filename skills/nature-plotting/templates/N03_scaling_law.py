"""N03 -- Scaling law: loss against compute for several model sizes, the compute-optimal frontier and its fit.
Use when: a family of runs differing in one size parameter is plotted on log-log axes and a power law is
fitted to the lower envelope.
Look: open axes, log-log with decade labels, one sequential colour per size (keyed by a discrete colour
bar), a dashed black frontier fit with its equation written along it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
sizes = np.array([1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9])
runs = []
E0 = 1.7                                                     # irreducible loss
for N in sizes:
    D = np.logspace(7, 10.5, 60)                             # tokens seen
    C = 6 * N * D
    L = E0 + 60 / N ** 0.3 + 200 / D ** 0.3
    runs.append((C, L))
# -------------------------------------------
cmap = truncate_cmap(NS_DUSK.reversed(), 0.1, 0.95)
cols = n_colors(cmap, len(sizes))
fig, ax = plt.subplots(figsize=figsize_mm(89, 64))
fig.subplots_adjust(left=0.13, right=0.84, bottom=0.15, top=0.96)
allC, allL = [], []
for (C, L), c in zip(runs, cols):
    ax.plot(C, L, color=c, lw=0.9)
    allC.append(C); allL.append(L)
allC = np.concatenate(allC); allL = np.concatenate(allL)
grid = np.logspace(np.log10(allC.min()), np.log10(allC.max()), 30)
front = np.array([allL[(allC >= g / 1.4) & (allC <= g * 1.4)].min() for g in grid])
p = np.polyfit(np.log10(grid[2:-2]), np.log10(front[2:-2] - E0), 1)
ax.plot(grid, E0 + 10 ** np.polyval(p, np.log10(grid)), color="0.05", lw=0.9, ls=(0, (4, 2)))
xm = 1e16
ax.text(xm, (E0 + 10 ** np.polyval(p, np.log10(xm))) * 0.95,
        f"$L = {E0} + {10 ** p[1]:.0f}\\,C^{{{p[0]:.3f}}}$", rotation=-17, ha="center", va="top")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(3e13, 3e20); ax.set_ylim(1.9, 4.6)
ax.set_yticks([2, 2.5, 3, 4], ["2", "2.5", "3", "4"]); ax.yaxis.set_minor_locator(mticker.NullLocator())
ax.set_xlabel("Compute (FLOP)"); ax.set_ylabel("Validation loss")
norm = mcolors.BoundaryNorm(np.arange(len(sizes) + 1) - 0.5, len(sizes))
sm = mpl.cm.ScalarMappable(norm=norm, cmap=mcolors.ListedColormap(cols))
cax = fig.add_axes([0.87, 0.2, 0.025, 0.7])
cb = fig.colorbar(sm, cax=cax, ticks=range(len(sizes)))
cb.ax.set_yticklabels(["1M", "3M", "10M", "30M", "100M", "300M", "1B"]); style_cbar(cb, "Parameters")
cb.ax.tick_params(length=0)
export(fig, "N03_scaling_law")
