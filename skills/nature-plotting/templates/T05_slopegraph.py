"""T05 -- Slopegraph: each item measured at two time points (or under two conditions), joined by a line.
Use when: 6-20 named items and the direction and size of each change matters more than the exact values;
a few items are called out in colour, the rest stay grey for context.
Look: no y axis line (values written at both ends), two labelled columns, highlighted rises / falls in the
up / down pair, everything else light grey.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(8)
items = [f"Item {c}" for c in "ABCDEFGHIJKL"]
before = np.round(rng.uniform(20, 80, len(items)), 0)
after = np.round(before + rng.normal(0, 8, len(items)), 0)
after[2] = before[2] + 26; after[7] = before[7] - 24; after[10] = before[10] + 18
highlight = {2: "up", 10: "up", 7: "down"}
# -------------------------------------------
up, down, base = THEMES["updown"][0], THEMES["updown"][1], "0.78"
fig, ax = plt.subplots(figsize=figsize_mm(70, 80))
for i, (b, a) in enumerate(zip(before, after)):
    c = {"up": up, "down": down}.get(highlight.get(i), base)
    z = 3 if i in highlight else 1
    ax.plot([0, 1], [b, a], "-o", color=c, lw=1.0 if i in highlight else 0.6, ms=2.5, zorder=z)
    if i in highlight:
        ax.text(1.06, a, f"{items[i]}  {a:.0f}", va="center", ha="left", fontsize=6, color=c)
        ax.text(-0.06, b, f"{b:.0f}", va="center", ha="right", fontsize=6, color=c)
ax.set_xlim(-0.35, 1.6); ax.set_ylim(min(before.min(), after.min()) - 4, max(before.max(), after.max()) + 4)
ax.set_xticks([0, 1], ["Time 1", "Time 2"])
despine(ax, left=True); ax.set_yticks([])
ax.spines["bottom"].set_bounds(0, 1)
ax.text(0.5, 1.0, "Value (unit), highlighted items labelled", transform=ax.transAxes, ha="center", va="bottom",
        fontsize=6, color="0.35")
export(fig, "T05_slopegraph")
