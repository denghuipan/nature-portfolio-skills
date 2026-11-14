"""M07 -- Polar (rose) histograms of directions for two groups, with the mean resultant vector.
Use when: the variable is an angle or a time of day / year (headings, orientations, phases, hours);
a linear histogram would split the data at an arbitrary cut.
Look: light polar grid, wedges without outlines, radial ticks at the edge only, mean direction as an arrow
whose length = resultant length R, Rayleigh-test P under the title, compass or clock labels.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(89)
g1 = rng.vonmises(np.deg2rad(40), 2.5, 220) % (2 * np.pi)       # angles (rad)
g2 = rng.vonmises(np.deg2rad(200), 0.6, 220) % (2 * np.pi)
pvals = ["P < 10$^{-10}$", "P = 0.003"]
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["ochre"]]
fig, axs = plt.subplots(1, 2, figsize=figsize_mm(110, 56), subplot_kw=dict(projection="polar"))
fig.subplots_adjust(left=0.05, right=0.95, top=0.82, bottom=0.06, wspace=0.45)
bins = np.linspace(0, 2 * np.pi, 25)
for ax, g, c, t, p in zip(axs, (g1, g2), cols, ("Group 1", "Group 2"), pvals):
    h, _ = np.histogram(g, bins)
    ax.bar(bins[:-1], h, width=np.diff(bins), align="edge", color=lighten(c, 0.25), lw=0.3, edgecolor="white")
    C, S = np.cos(g).mean(), np.sin(g).mean(); R = np.hypot(C, S); mu = np.arctan2(S, C)
    rmax = h.max() * 1.1
    ax.annotate("", xy=(mu, R * rmax), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="0.1", lw=1.0, mutation_scale=6, shrinkA=0, shrinkB=0))
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_xticks(np.deg2rad([0, 90, 180, 270]), ["N", "E", "S", "W"])
    ax.set_ylim(0, rmax); ax.set_yticks([int(rmax / 2), int(rmax * 0.95)])
    ax.set_rlabel_position(135); ax.tick_params(axis="y", labelsize=5.5, colors="0.45")
    ax.grid(color="0.88", lw=0.4); ax.spines["polar"].set_linewidth(0.5); ax.spines["polar"].set_color("0.6")
    ax.set_title(f"{t}\nR = {R:.2f}, {p}", fontsize=6.5, pad=10, linespacing=1.3)
panel_label(axs[0], "a", dx=-0.15, dy=1.32); panel_label(axs[1], "b", dx=-0.15, dy=1.32)
export(fig, "M07_polar_rose")
