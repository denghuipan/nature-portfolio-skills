"""D06 -- Joint distribution of two variables: hexbin density with marginal histograms.
Use when: thousands of points where a scatter would saturate.
Nature notes: log colour scale for counts with a slim inset colour bar; marginals share the density hue;
keep the main panel close to square.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(36)
x = rng.gamma(4, 0.25, 20000)
y = 0.8 * x + rng.normal(0, 0.25 + 0.1 * x, x.size)
# -------------------------------------------

fig = plt.figure(figsize=figsize_mm(80, 74))
gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=0.05, hspace=0.05)
ax = fig.add_subplot(gs[1, 0]); axx = fig.add_subplot(gs[0, 0], sharex=ax); axy = fig.add_subplot(gs[1, 1], sharey=ax)
hb = ax.hexbin(x, y, gridsize=40, cmap=NS_GLACIER.reversed(), norm=mpl.colors.LogNorm(), mincnt=1, lw=0)
c = lighten(PALETTE["blue"], 0.4)
axx.hist(x, bins=60, color=c, edgecolor="none"); axy.hist(y, bins=60, orientation="horizontal", color=c, edgecolor="none")
for a_ in (axx, axy):
    for s in ("top", "right"):
        a_.spines[s].set_visible(False)
    a_.tick_params(which="both", top=False, right=False, labelbottom=False, labelleft=False)
axx.tick_params(which="both", left=False, top=False, right=False)
axy.tick_params(which="both", bottom=False, top=False, right=False)
axx.minorticks_off(); axy.minorticks_off()
axx.spines["left"].set_visible(False); axy.spines["bottom"].set_visible(False)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Variable $y$ (unit)")
cb = cbar_inset(ax, hb, "Counts", loc="upper left", width="32%", height="4%", borderpad=1.8)
log_ticks(cb.ax.xaxis, minor=False)
style_axes(ax)
export(fig, "D06_joint_hexbin")
