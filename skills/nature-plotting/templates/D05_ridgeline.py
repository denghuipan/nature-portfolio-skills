"""D05 -- Ridgeline (joy) plot: one density per level of an ordered factor.
Use when: a distribution shifts or broadens with a parameter (dose, temperature, time point).
Nature notes: colour encodes the ordered factor (sequential map); labels on the left replace a legend;
keep the overlap modest so tails stay readable.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(35)
levels = [f"Level {i}" for i in range(1, 7)]
samples = [rng.normal(0, 0.02 + 0.012 * i ** 1.6, 800) for i in range(len(levels))]
grid = np.linspace(-0.5, 0.5, 400)
# -------------------------------------------

from scipy.stats import gaussian_kde
dens = [gaussian_kde(s)(grid) for s in samples]
dens = [d / d.max() for d in dens]
fig, ax = plt.subplots(figsize=figsize_mm(70, 62))
cols = n_colors(truncate_cmap(NS_REDS, 0.35, 1.0), len(levels))
ridgeline(ax, grid, dens[::-1], cols[::-1], offset=0.55, fill="solid", baseline=True,
          labels_left=levels[::-1], label_colors=["0.2"] * len(levels))
ax.set_xlim(-0.5, 0.5); ax.set_yticks([]); ax.set_xlabel("Value (unit)")
ax.axvline(0, color="0.6", lw=0.5, ls=":")
style_axes(ax); ax.tick_params(axis="y", which="both", left=False, right=False)
export(fig, "D05_ridgeline")
