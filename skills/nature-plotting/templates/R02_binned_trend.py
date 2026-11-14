"""R02 -- Binned trend: mean (+- s.e.m.) of y in bins of x, with the number of observations per bin below.
Use when: y depends on x but the raw cloud is too noisy or too large to read; showing bin counts tells the
reader where the trend is well supported.
Look: open axes, dots with thin error bars (no caps), a light count histogram in a short strip underneath
sharing x, the axis of the strip on the left with comma separators.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(13)
x = np.clip(100 - rng.gamma(2.2, 11, 40000), 15, 100)
p = 0.55 + 0.4 / (1 + np.exp(-(x - 88) / 4.5))
y = (rng.random(x.size) < p).astype(float)            # a 0/1 outcome per observation
# -------------------------------------------
c = "#4B6CB7"
fig = plt.figure(figsize=figsize_mm(80, 66))
gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1], hspace=0.08, left=0.17, right=0.97, top=0.97, bottom=0.15)
ax = fig.add_subplot(gs[0]); hx = fig.add_subplot(gs[1], sharex=ax)
bins = np.arange(20, 102, 4)
binned_stat(ax, x, y, bins, color=c, err="sem", ms=2.8)
ax.set_ylim(0.45, 1.0); ax.set_ylabel("Fraction correct")
ax.tick_params(labelbottom=False)
hx.hist(x, bins=bins, color=lighten(c, 0.6), lw=0)
hx.set_ylabel("n", rotation=0, ha="right", va="center"); thousands(hx); hx.set_yticks([0, 5000])
hx.set_xlim(20, 100); hx.set_xlabel("Predicted confidence")
export(fig, "R02_binned_trend")
