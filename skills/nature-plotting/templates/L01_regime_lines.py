"""L01 -- Two series vs a control variable, with a failure regime and a threshold.
Use when: one series holds up where another breaks down (error vs noise level, yield vs load ...).
Nature notes: label curves directly (no legend box); shade the regime instead of describing it in the
caption; the threshold label sits beside its line, never across it; a second x axis can give the same
variable in other units.
Replace the MOCK DATA block with your arrays; everything below it is the template.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(0, 10, 15)                                  # control variable
rng = np.random.default_rng(1)
data1 = 5e-4 * (1 + 10 ** ((x - 5.0) / 2.6)) * rng.lognormal(0, 0.04, x.size)
data2 = 7e-4 * (1 + 10 ** ((x - 6.5) / 1.0)) * rng.lognormal(0, 0.04, x.size)
threshold = 7.2                                             # where Data 2 fails
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_1col(58))
c1, c2 = PALETTE["blue"], PALETTE["red"]
ax.plot(x, data1, "-o", color=c1, ms=3.2, mec="w", mew=0.4, zorder=3)
ax.plot(x, data2, "-s", color=c2, ms=3.0, mec="w", mew=0.4, zorder=3)
ax.set_yscale("log"); ax.set_xlim(0, 10); ax.set_ylim(2e-4, 3)
log_ticks(ax.yaxis)

regime(ax, threshold, 10, color=PALETTE["red"], alpha=(0.0, 0.16))
ref_line(ax, threshold, "x", "Threshold", side="left", color="0.25")
direct_label(ax, 2.0, data1[3], "Data 1", color=c1, dy=-3, va="top")
direct_label(ax, 2.0, data2[3], "Data 2", color=c2, dy=3, va="bottom")
direct_label(ax, 8.6, 1.3e-3, "Data 2\nfails", color=darken(c2, 0.25), ha="center")

ax.set_xlabel("Control variable $x$ (unit A)")
ax.set_ylabel("Error (a.u.)")
secondary_unit_axis(ax, "x", (lambda v: v * 10, lambda v: v / 10), label="$x$ (unit B)")
style_axes(ax)
export(fig, "L01_regime_lines")
