"""C06 -- Range / dot-whisker plot on a log axis: rows = sets, colour = a continuous parameter.
Use when: comparing the span of a quantity across sets and items that differ by many decades.
Nature notes: rows instead of a legend; colour from an ordered map with a small inset colour bar (label above,
ticks below); the inaccessible range shaded as a gradient.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(14)
set1 = [(10 ** e, 10 ** (e - 0.15), 10 ** (e + 0.2)) for e in (2.0, 2.3, 2.45, 2.8, 3.4, 3.95, 4.3, 4.95)]
set2 = [10 ** e for e in (6.1, 6.4, 6.6, 6.8, 7.2, 7.3)]
set3 = [(10 ** e, 10 ** (e - 0.1), 10 ** (e + 0.15), p) for e, p in
        [(2.7, 3), (3.9, 5), (4.3, 8), (5.1, 2), (5.9, 1), (6.0, 2), (6.75, 8), (4.2, 3), (4.75, 10), (5.95, 1)]]
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(89, 56))
for m, lo, hi in set1:
    ax.plot([lo, hi], [2, 2], color="0.55", lw=0.8); ax.plot(m, 2, "s", ms=3.2, mfc="0.6", mec="0.25", mew=0.5)
ax.plot(set2, [1] * len(set2), "D", ms=3.2, mfc=PALETTE["purple"], mec="0.25", mew=0.5)
cmap = truncate_cmap(NS_EMBER, 0.15, 0.85)
sm, col = line_mappable(cmap, 1, 10)
for k, (m, lo, hi, p) in enumerate(set3):
    y = -0.15 if k % 2 else 0.15
    ax.plot([lo, hi], [y, y], color=col(p), lw=0.9); ax.plot(m, y, "o", ms=3.4, mfc=col(p), mec="0.2", mew=0.5)
ax.set_xscale("log"); ax.set_xlim(30, 5e7); ax.set_ylim(-0.7, 2.7); log_ticks(ax.xaxis)
regime(ax, 30, 90, color="0.3", fade="out", alpha=(0.0, 0.45))
ax.set_yticks([2, 1, 0], ["Set 1", "Set 2", "Set 3"])
ax.set_xlabel("Quantity (unit)")
cbar_inset(ax, sm, "Parameter $p$", loc="upper right", width="27%", height="4%", ticks=[1, 5, 10], borderpad=2.4)
style_axes(ax); ax.tick_params(axis="y", which="both", left=False, right=False)
export(fig, "C06_range_rows")
