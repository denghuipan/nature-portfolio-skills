"""L08 -- Overview curve with an inset zoom and width arrows.
Use when: the full range gives context but the claim is in one narrow feature.
Nature notes: a dashed box on the parent marks the zoomed region and is lettered if the inset is cited;
two widths compared with two double arrows in the two curve colours, value written once.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(0, 100, 3000)
data1 = make_spectrum(x, [(12, 1.0, 0.8), (35, 0.45, 0.9), (75, 0.3, 4.0), (55, 0.8, 0.75)])
data2 = make_spectrum(x, [(12, 0.97, 0.83), (35, 0.47, 0.95), (75, 0.31, 4.1), (55.01, 0.79, 0.77)])
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_1col(58))
ax.fill_between(x, data1, color="0.82", lw=0, label="Data 1")
ax.plot(x, data2, color=PALETTE["red"], lw=0.9, label="Data 2")
ax.set_xlim(0, 100); ax.set_ylim(0, 1.25)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Signal (norm.)")
ax.legend(loc="upper left")
axins = inset_zoom(ax, [0.60, 0.50, 0.37, 0.45], (52.5, 57.5), (0, 0.95), label="b")
m = (x > 52.5) & (x < 57.5)
axins.fill_between(x[m], data1[m], color="0.82", lw=0)
axins.plot(x[m], data2[m], color=PALETTE["red"], lw=0.9)
for y, c, w in [(0.40, "k", 0.75), (0.34, PALETTE["red"], 0.77)]:
    hw = w * 1.1774
    double_arrow(axins, (55 - hw, y), (55 + hw, y), None, color=c, mutation_scale=4)
axins.text(0.04, 0.95, "FWHM", transform=axins.transAxes, va="top", fontsize=5.5)
axins.set_xticks([53, 55, 57]); axins.set_yticks([])
style_axes(ax)
export(fig, "L08_inset_zoom")
