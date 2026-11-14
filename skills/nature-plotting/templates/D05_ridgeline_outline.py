"""D05 -- Ridgeline of densities: one row per condition, outlines over white so rows overlap cleanly.
Use when: 6-15 ordered conditions (time points, doses, depths) each have a distribution and the drift of
its location and width is the message.
Look: no frame, sequential colours by condition, white fill hides the row behind, a short median tick on
each ridge, labels on the left, one bottom axis.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.stats import gaussian_kde

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(23)
levels = [f"Day {d}" for d in (0, 1, 2, 4, 7, 10, 14, 21, 28)]
samples = [rng.normal(0.1 * k ** 1.2, 0.35 + 0.05 * k, 400) for k in range(len(levels))]
# -------------------------------------------
cols = n_colors(NS_SEAFLOOR, len(levels), 0.35, 0.95)
grid = np.linspace(-1.5, 4.5, 400)
fig, ax = plt.subplots(figsize=figsize_mm(70, 78))
fig.subplots_adjust(left=0.2, right=0.96, bottom=0.12, top=0.97)
off = 0.55
for i, (s, c) in enumerate(zip(samples, cols)):
    d = gaussian_kde(s)(grid)
    d = d / d.max()
    y0 = (len(levels) - 1 - i) * off
    z = 10 + i
    ax.fill_between(grid, y0, y0 + d, color="white", lw=0, zorder=z)
    gradient_fill(ax, grid, y0 + d, c, alpha=0.55, ymin=y0, zorder=z + 0.1)
    ax.plot(grid, y0 + d, color=c, lw=0.9, zorder=z + 0.2)
    ax.plot([grid[0], grid[-1]], [y0, y0], color=c, lw=0.4, zorder=z + 0.2)
    m = np.median(s)
    ax.plot([m, m], [y0, y0 + np.interp(m, grid, d)], color=darken(c, 0.2), lw=0.6, zorder=z + 0.3)
    ax.text(-1.6, y0 + 0.12, levels[i], ha="right", va="bottom", color=darken(c, 0.25))
ax.set_xlim(-1.5, 4.5); ax.set_ylim(-0.1, (len(levels) - 1) * off + 1.1)
ax.set_yticks([])
ax.set_xlabel("Value (unit)")
no_background(ax)                 # the ridges carry their own gradients; a panel gradient would show through
export(fig, "D05_ridgeline_outline")
