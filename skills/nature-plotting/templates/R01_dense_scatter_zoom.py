"""R01 -- Dense agreement scatter with a magnified corner: predicted confidence vs measured accuracy.
Use when: tens of thousands of points pile up in one corner (most predictions are good) and the agreement
there is the interesting part; the zoom panel sits beside the main one with connector lines.
Look: open main axes with equal scales, tiny rasterised points, grey y = x, regression line in a dark
hue, framed zoom panel joined by thin lines to the marked region.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(3)
n = 12000
x = 100 - rng.gamma(1.6, 7.5, n)
x = x[x > 25]
y = np.clip(x + rng.normal(0, 4.5, x.size) - 0.08 * (100 - x) ** 1.1 + 2.0, 0, 100)
# -------------------------------------------
c = "#4B6CB7"
fig = plt.figure(figsize=figsize_mm(120, 62))
ax = fig.add_axes([0.09, 0.15, 0.4, 0.78]); zx = fig.add_axes([0.6, 0.15, 0.38, 0.78])
for a, s in ((ax, 0.4), (zx, 0.8)):
    a.scatter(x, y, s=s, color=c, alpha=0.35, lw=0, rasterized=True)
    a.plot([0, 100], [0, 100], color="0.55", lw=0.6)
    p = np.polyfit(x, y, 1)
    xx = np.array([x.min(), 100])
    a.plot(xx, np.polyval(p, xx), color="#2B1E7A", lw=1.0)
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal")
zoom_to(ax, zx, (80, 100), (80, 100))
zx.set_xticks([80, 90, 100]); zx.set_yticks([80, 90, 100])
ax.set_xlabel("Predicted confidence"); ax.set_ylabel("Measured accuracy")
stats_text(ax, [f"n = {x.size:,}", f"slope = {p[0]:.2f}"], loc="upper left")
panel_label(ax, "a", dx=-0.24, dy=1.06)
export(fig, "R01_dense_scatter_zoom")
