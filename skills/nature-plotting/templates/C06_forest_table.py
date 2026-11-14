"""C06 -- Forest plot with the numbers as a table: subgroups, effect estimates, intervals, weights, pooled diamond.
Use when: an effect is estimated in several subgroups / studies / cohorts and pooled; readers need the
values written out next to the graphic (clinical and meta-analysis papers).
Look: text columns left and right of the plot, squares sized by weight, thin CI lines, a diamond for the
pooled estimate, a solid null line and a dashed line at the pooled value, 'favours' labels under the axis.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from matplotlib.patches import Polygon as _Poly

# ---------------- MOCK DATA ----------------
rows = [("Subgroup 1", 412, 0.78, 0.62, 0.98), ("Subgroup 2", 388, 0.85, 0.66, 1.09),
        ("Subgroup 3", 145, 0.64, 0.42, 0.97), ("Subgroup 4", 221, 1.04, 0.76, 1.42),
        ("Subgroup 5", 503, 0.72, 0.59, 0.88), ("Subgroup 6", 96, 0.91, 0.55, 1.50)]
pooled = (1765, 0.79, 0.71, 0.88)
# -------------------------------------------
c = PALETTE["blue"]
n = len(rows)
fig = plt.figure(figsize=figsize_mm(140, 60))
ax = fig.add_axes([0.36, 0.2, 0.34, 0.68])
tab = fig.add_axes([0.0, 0.2, 0.36, 0.68], sharey=ax); tab.axis("off")
tab2 = fig.add_axes([0.71, 0.2, 0.29, 0.68], sharey=ax); tab2.axis("off")
w = np.array([r[1] for r in rows], float); w = w / w.max()
for i, (nm, nn, e, lo, hi) in enumerate(rows):
    ax.plot([lo, hi], [i, i], color="0.2", lw=0.7, solid_capstyle="butt")
    ax.plot(e, i, "s", color=c, ms=2.5 + 3.5 * w[i], mec="none")
    tab.text(0.04, i, nm, va="center", fontsize=6)
    tab.text(0.86, i, f"{nn:,}", va="center", ha="right", fontsize=6)
    tab2.text(0.05, i, f"{e:.2f} ({lo:.2f}–{hi:.2f})", va="center", fontsize=6)
yp = n + 0.6
_, pe, plo, phi = pooled
ax.add_patch(_Poly([(plo, yp), (pe, yp - 0.35), (phi, yp), (pe, yp + 0.35)], closed=True, color="0.15"))
tab.text(0.04, yp, "Pooled", va="center", fontsize=6, fontweight="bold")
tab.text(0.86, yp, f"{pooled[0]:,}", va="center", ha="right", fontsize=6, fontweight="bold")
tab2.text(0.05, yp, f"{pe:.2f} ({plo:.2f}–{phi:.2f})", va="center", fontsize=6, fontweight="bold")
for t_ax, xs, labs, has in ((tab, (0.04, 0.86), ("Subgroup", "n"), ("left", "right")),
                            (tab2, (0.05,), ("Hazard ratio (95% CI)",), ("left",))):
    for x, l, h in zip(xs, labs, has):
        t_ax.text(x, -1.1, l, va="center", ha=h, fontsize=6, color="0.3")
ax.axvline(1.0, color="0.2", lw=0.6)
ax.axvline(pe, color="0.4", lw=0.5, ls=(0, (3, 2)))
ax.set_xscale("log"); ax.set_xlim(0.4, 1.8)
ax.set_xticks([0.5, 0.75, 1, 1.5], ["0.5", "0.75", "1", "1.5"]); ax.xaxis.set_minor_locator(mticker.NullLocator())
ax.set_ylim(yp + 0.9, -1.6)
despine(ax, left=True); ax.set_yticks([])
ax.set_xlabel("Hazard ratio")
ax.text(1.0, -0.28, "← Favours treatment  ", transform=ax.get_xaxis_transform(), ha="right", fontsize=6,
        color="0.35")
ax.text(1.0, -0.28, "  Favours control →", transform=ax.get_xaxis_transform(), ha="left", fontsize=6,
        color="0.35")
export(fig, "C06_forest_table")
