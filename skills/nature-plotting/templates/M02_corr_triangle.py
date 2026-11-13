"""M02 -- Correlation matrix as a lower triangle with a centred diverging map and values in the cells.
Use when: pairwise correlation / similarity between 4-12 variables.
Nature notes: show each pair once; the neutral colour is pinned to 0; text flips to white on dark cells;
the colour bar spans the full [-1, 1] range so colours are comparable across figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(52)
names = [f"V{i}" for i in range(1, 8)]
A = rng.normal(size=(200, 7)); A[:, 1] += 0.8 * A[:, 0]; A[:, 3] -= 0.7 * A[:, 2]; A[:, 6] += 0.5 * A[:, 4]
C = np.corrcoef(A.T)
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(70, 60))
m = corr_triangle(ax, C, names, cmap=NS_DIV_BR, fmt="{:.2f}")
cb = cbar_side(ax, m, "Pearson $r$", size="4%", ticks=[-1, -0.5, 0, 0.5, 1])
export(fig, "M02_corr_triangle")
