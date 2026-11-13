"""L03 -- A family of curves coloured by a continuous parameter, with a colour bar and a floor region.
Use when: one curve per level of an ordered parameter and the trend across the family matters.
Nature notes: an ordered parameter gets an ordered map plus a colour bar -- never a 9-entry legend;
the floor ('below detection limit') is a soft gradient, not a hard box.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
p = np.linspace(1, 9, 9)                                    # parameter, one curve each
x = np.array([0, 5, 10, 15, 20.0])
rng = np.random.default_rng(2)
curves = {pi: np.clip((x + 1) * (1.25 - 0.08 * pi) + rng.normal(0, 0.3, x.size), 0.2, None) for pi in p}
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_1col(60))
cmap = truncate_cmap(NS_EMBER, 0.12, 0.85)
sm, col = line_mappable(cmap, p.min(), p.max())
for pi in p:
    ax.plot(x, curves[pi], "-o", color=col(pi), lw=0.9, ms=2.6, mec="k", mew=0.3, zorder=3)
ax.set_xlim(-1, 21); ax.set_ylim(-0.5, 27)
regime(ax, -1, 1.5, color="0.35", fade="out", alpha=(0.0, 0.40), label="Below limit", label_color="0.3",
       label_x=0.0)
ax.axhline(0, color="k", ls=":", lw=0.6, zorder=1)
cb = cbar_side(ax, sm, None, size="4%", pad=0.05, ticks=[1, 5, 9])
cb.ax.set_title("$p$", fontsize=mpl.rcParams["legend.fontsize"], pad=2)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Response (a.u.)")
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5)); ax.set_xticks([0, 5, 10, 15, 20])
style_axes(ax)
export(fig, "L03_hue_lines")
