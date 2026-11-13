"""R02 -- Scatter with a third variable as colour (colour bar) and a fourth as marker size (size key).
Use when: exploring how two outcomes co-vary across parameters (design sweeps, cohort features).
Nature notes: sequential map for an ordered colour variable; area (not radius) proportional to the size
variable, with a 3-step size key; edge lines keep overlapping markers readable.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(42)
n = 60
x = rng.uniform(0, 1, n); y = 0.6 * x + rng.normal(0, 0.12, n)
c = x * 40 + rng.normal(0, 4, n)                  # colour variable
s = rng.uniform(5, 50, n)                          # size variable
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(80, 62))
area = lambda v: 4 + v * 1.1
sc = ax.scatter(x, y, c=c, s=area(s), cmap=truncate_cmap(NS_SUNSET, 0.1, 0.95), edgecolors="k", linewidths=0.35,
                alpha=0.9, zorder=3)
cb = cbar_side(ax, sc, "Variable $c$ (unit)", size="3.5%")
for v in (10, 30, 50):
    ax.scatter([], [], s=area(v), facecolors="none", edgecolors="0.3", lw=0.5, label=f"{v}")
ax.legend(title="Variable $s$", loc="upper left", labelspacing=0.9, borderpad=0.6, handletextpad=0.6,
          title_fontsize=5.5)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Variable $y$ (unit)")
style_axes(ax)
export(fig, "R02_scatter_color_size")
