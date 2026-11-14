"""K04 -- The same panel in the five axis looks: boxed (default), grid, framed, open, classic.
Use when: deciding the look of a whole paper (pick one and keep it in every figure):
  boxed   full frame, short inward ticks bottom / left, gradient panel background (house default)
  grid    boxed + faint horizontal grid: dense bars or long time series read off the axis
  framed  full frame, outward ticks, faint grid: log-log physics / benchmark plots
  open    L-shaped axes, outward ticks (when a lighter page is wanted)
  classic full box with inward ticks on four sides and minor ticks, older palette, no gradient
Call set_look(name) once at the top of a script; style_axes(ax, look) restyles a single axes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(139)
x = np.linspace(0, 10, 11)
y1 = 2 + 0.8 * x + rng.normal(0, 0.4, x.size)
y2 = 1 + 0.45 * x + rng.normal(0, 0.4, x.size)
# -------------------------------------------
looks = ["boxed", "grid", "framed", "open", "classic"]
fig, axs = plt.subplots(1, 5, figsize=figsize_2col(46))
fig.subplots_adjust(left=0.05, right=0.99, bottom=0.24, top=0.86, wspace=0.45)
for ax, lk in zip(axs, looks):
    set_look(lk)
    style_axes(ax, lk)
    if lk != "classic":
        bg_gradient(ax)                     # backgrounds are added at save time for the active look only
    else:
        no_background(ax)
    ax.plot(x, y1, "-o", color=CYCLE[0], ms=2.6, label="Data 1")
    ax.plot(x, y2, "-s", color=CYCLE[1], ms=2.6, mfc="white", label="Data 2")
    ax.set_xlim(-0.5, 10.5); ax.set_ylim(0, 12)
    ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Response (unit)")
    subtitle(ax, f'set_look("{lk}")')
    ax.legend(loc="upper left")
set_look("boxed")
export(fig, "K04_axis_looks")
