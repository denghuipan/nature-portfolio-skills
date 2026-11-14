"""D01 -- Violins with an inner box and all points, significance brackets and n under each group.
Use when: 3-6 groups with tens to hundreds of observations each; the shape (bimodal? skewed?) matters as
much as the median.
Look: open axes, pale violins without outline, slim dark box (IQR) with a white median dot, points as a
light jittered strip, brackets with exact P values, n on the second tick line.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(14)
groups = ["Control", "Group 1", "Group 2", "Group 3"]
data = [rng.normal(1.0, 0.25, 140),
        np.r_[rng.normal(1.1, 0.2, 90), rng.normal(1.8, 0.2, 50)],
        rng.gamma(6, 0.25, 160),
        rng.normal(2.1, 0.35, 120)]
tests = [(0, 1, "P = 3 × 10$^{-6}$"), (0, 2, "P < 10$^{-10}$"), (2, 3, "P = 0.21")]
# -------------------------------------------
cols = [PALETTE["grey"], PALETTE["teal"], PALETTE["blue"], PALETTE["ochre"]]
fig, ax = plt.subplots(figsize=figsize_mm(80, 62))
fig.subplots_adjust(left=0.14, right=0.98, bottom=0.18, top=0.97)
x = np.arange(len(groups))
vp = ax.violinplot(data, positions=x, widths=0.78, showextrema=False)
for b, c in zip(vp["bodies"], cols):
    b.set_facecolor(lighten(c, 0.55)); b.set_edgecolor("none"); b.set_alpha(1)
for xi, d, c in zip(x, data, cols):
    jitter(ax, xi, d, darken(c, 0.1), width=0.06, size=2.5, alpha=0.35, zorder=2)
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    ax.plot([xi, xi], [q1, q3], color="0.15", lw=3.0, solid_capstyle="butt", zorder=3)
    ax.plot([xi, xi], np.percentile(d, [5, 95]), color="0.15", lw=0.6, zorder=3)
    ax.plot(xi, med, "o", ms=2.6, mfc="white", mec="white", zorder=4)
top = max(np.max(d) for d in data)
for k, (i, j, txt) in enumerate(tests):
    sig_bracket(ax, i, j, top + 0.18 + 0.36 * k, txt)
ax.set_xticks(x); n_ticklabels(ax, groups, [len(d) for d in data])
ax.tick_params(axis="x", length=0)
ax.set_ylabel("Measured value (unit)")
ax.set_ylim(0, top + 1.25); ax.set_yticks([0, 1, 2, 3])
export(fig, "D01_violin_box")
