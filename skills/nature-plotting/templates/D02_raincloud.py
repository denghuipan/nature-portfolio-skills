"""D02 -- Raincloud: half density + IQR bar with median + raw points.
Use when: distributions with structure (skew, two modes) that a box plot would hide.
Nature notes: horizontal layout reads well with long group names; one hue per group for density, bar and
points; mark the reference value with a dashed line; write the mean next to each row.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(32)
groups = ["Group 1", "Group 2", "Group 3", "Group 4"]
data = [np.clip(rng.beta(0.6, 4, 400), 0, 1), np.clip(np.r_[rng.beta(2, 2, 250), rng.beta(8, 1.5, 150)], 0, 1),
        np.clip(1 - rng.gamma(1.0, 0.03, 300), 0, 1), np.clip(1 - rng.gamma(0.8, 0.01, 300), 0, 1)]
colors = ["0.45", PALETTE["skyblue"], PALETTE["blue"], "#5B2C91"]
# -------------------------------------------

from scipy.stats import gaussian_kde
fig, ax = plt.subplots(figsize=figsize_mm(89, 58))
pos = np.arange(len(groups))[::-1] * 1.0
rng2 = np.random.default_rng(1)
for p, d, c in zip(pos, data, colors):
    yy = np.linspace(d.min(), d.max(), 200)
    dens = gaussian_kde(d)(yy); dens = dens / dens.max() * 0.38
    ax.fill_between(yy, p + 0.08, p + 0.08 + dens, color=c, alpha=0.40, lw=0)
    ax.plot(yy, p + 0.08 + dens, color=c, lw=0.6)
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    ax.plot([q1, q3], [p, p], color=c, lw=2.6, solid_capstyle="butt")
    ax.plot(med, p, "o", ms=2.6, mfc="w", mec=c, mew=0.8, zorder=4)
    ax.scatter(d, p - 0.18 + rng2.uniform(-0.07, 0.07, d.size), s=2.0, color=c, alpha=0.35, lw=0)
    direct_label(ax, 1.0, p, f"{np.mean(d):.3f}", color=c, dx=3, ha="left")
ax.axvline(1.0, color="0.5", ls=(0, (3, 2)), lw=0.6)
ax.set_yticks(pos, groups); ax.set_ylim(-0.5, pos.max() + 0.6)
ax.set_xlim(-0.02, 1.12); ax.set_xlabel("Score")
style_axes(ax); ax.tick_params(axis="y", which="both", left=False, right=False)
export(fig, "D02_raincloud")
