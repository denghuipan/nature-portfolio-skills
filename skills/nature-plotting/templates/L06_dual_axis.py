"""L06 -- Two quantities with different units on one panel (left and right y axes).
Use when: a measured quantity and a second quantity that explains it, against the same x.
Nature notes: colour the right axis (spine, ticks, label) like its curve so the pairing is unambiguous;
use a dual axis only when the comparison is the point.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.arange(1, 10, 1.0)
data1 = np.array([0.80, 1.05, 1.04, 0.82, 0.47, 0.42, 0.37, 0.36, 0.30])
xx = np.linspace(0.5, 9.5, 200)
data2 = np.interp(xx, [0.5, 2, 3, 4, 5, 6, 7, 8, 9.5], [72, 74, 74, 66, 55, 45, 34, 25, 10])
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_1col(56))
blue, gray = PALETTE["blue"], "0.45"
ax.plot(x, data1, "-o", color=blue, lw=1.1, ms=3.4, mec="w", mew=0.4, zorder=3)
ax.set_ylim(0, 1.25); ax.set_xlim(0.5, 9.5)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Data 1 (unit 1)", color=blue)
ax.tick_params(axis="y", colors=blue, which="both")
ax.spines["left"].set_color(blue)
ax2 = ax.twinx()
ax2.plot(xx, data2, ls=(0, (3, 1.5)), color=gray, lw=0.9)
ax2.set_ylim(0, 100); ax2.set_ylabel("Data 2 (%)", color=gray)
ax2.tick_params(axis="y", colors=gray, which="both", direction="in")
ax2.spines["right"].set_color(gray); ax2.spines["left"].set_color(blue)
ax.tick_params(axis="y", which="both", right=False)
direct_label(ax, 2.0, data1[1], "Data 1", color=blue, dy=4, va="bottom")
direct_label(ax2, 6.5, data2[np.argmin(abs(xx - 6.5))], "Data 2", color=gray, dy=5, ha="center", va="bottom")
export(fig, "L06_dual_axis")
