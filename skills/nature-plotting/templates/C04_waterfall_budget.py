"""C04 -- Waterfall / budget chart.
Use when: a final number is the sum of signed contributions (loss budget, error budget, ablation) and the
reader must see where it goes.
Nature notes: losses red, gains green, totals blue -- keep that meaning fixed across the paper; write the
signed value on each step; dotted connectors make the running level readable.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
steps = ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"]
delta = [-1.2, -1.8, +2.5, -6.4, -4.2, -2.6]
start = -60.0
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(89, 56))
waterfall(ax, steps, delta, start=start, start_label="Input", end_label="Output",
          total_color=PALETTE["blue"], loss_color=PALETTE["red"], gain_color=PALETTE["green"], base=-90)
ax.set_ylim(-90, -52); ax.set_ylabel("Level (dB)")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")
style_axes(ax); ax.tick_params(axis="x", which="both", bottom=False, top=False)
export(fig, "C04_waterfall_budget")
