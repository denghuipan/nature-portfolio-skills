"""D03 -- Overlaid step histograms on a log count axis: two populations of very different size.
Use when: one population is orders of magnitude larger than the other and both tails matter, so filled bars
would hide one of them.
Look: open axes, outlines only (no fill), two tones of one hue, legend as short line keys, a dashed
threshold with its label beside it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(16)
big = -rng.exponential(28, 260000)          # Population 2 (large)
small = -rng.exponential(22, 2600) - rng.exponential(30, 2600) * (rng.random(2600) < 0.3)
thr = -50
# -------------------------------------------
dark, light = THEMES["duo_purple"]
fig, ax = plt.subplots(figsize=figsize_mm(80, 52))
fig.subplots_adjust(left=0.15, right=0.97, bottom=0.2, top=0.95)
bins = np.linspace(-200, 0, 41)
ax.stairs(*np.histogram(big, bins), color=dark, lw=0.9, label="Population 2", baseline=None)
ax.stairs(*np.histogram(small, bins), color=light, lw=0.9, label="Population 1", baseline=None)
ax.set_yscale("log"); ax.set_ylim(0.8, 3e5); ax.set_xlim(-200, 0)
ref_line(ax, thr, "x", label="Threshold", color="0.35", ls=(0, (3, 2)), pos=0.97, side="left")
ax.set_xlabel("Energy relative to reference (unit)"); ax.set_ylabel("Count")
ax.legend(loc="upper left", handlelength=1.2)
export(fig, "D03_step_hist_log")
