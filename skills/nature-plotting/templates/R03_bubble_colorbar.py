"""R03 -- Bubble scatter: x vs y, bubble area = weight (size of unit), colour = a third variable, two views.
Use when: units of very different size (countries, sites, species, labs) are compared on two quantities and
a third explains the pattern; the same data are shown against two candidate drivers side by side.
Look: open axes, log x, sequential multi-hue colour (light = low), horizontal colour bar under each panel,
rank correlation and P in the top-left corner, dashed zero line, a bubble-size key.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(19)
n = 150
driver1 = 10 ** rng.uniform(-0.5, 2.5, n)                  # e.g. cumulative quantity per unit
driver2 = 10 ** (2.6 + 0.6 * np.log10(driver1) + rng.normal(0, 0.35, n))
yv = -22 + 6 * np.clip(np.log10(driver2) - 3.4, 0, None) ** 1.6 + rng.normal(0, 4, n)
weight = rng.lognormal(2.0, 1.1, n)                         # e.g. population
stats = [("$\\rho$ = 0.20, P = 0.0061", "Weighted $\\rho$ = 0.30"),
         ("$\\rho$ = 0.49, P = 2.9 × 10$^{-13}$", "Weighted $\\rho$ = 0.66")]
# -------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=figsize_2col(80))
fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08, wspace=0.28)
size = 4 + 60 * (weight / weight.max()) ** 0.6
for ax, (xv, cv, xl, cl), st in zip(
        axs, ((driver1, driver2, "Driver 1 (unit per capita)", "Driver 2 (unit)"),
              (driver2, driver1, "Driver 2 (unit)", "Driver 1 (unit per capita)")), stats):
    norm = mcolors.LogNorm(cv.min(), cv.max())
    sc = ax.scatter(xv, yv, s=size, c=cv, cmap=NS_DUSK, norm=norm, alpha=0.9, lw=0)
    ax.axhline(0, color="0.1", lw=0.8, ls=(0, (4, 2)))
    ax.set_xscale("log"); ax.set_ylim(-35, 12)
    ax.set_xlabel(xl); ax.set_ylabel("Change relative to baseline (%)")
    stats_text(ax, list(st), loc="upper left")
    cb = cbar_below(ax, sc, cl, size="4.5%", pad=0.45)
size_legend(axs[1], [1, 10, 100], [4 + 60 * (v / weight.max()) ** 0.6 for v in (1, 10, 100)], title="Weight",
            loc="lower right", color="0.7", labelspacing=0.4)
panel_label(axs[0], "a", dx=-0.13, dy=1.04); panel_label(axs[1], "b", dx=-0.13, dy=1.04)
export(fig, "R03_bubble_colorbar")
