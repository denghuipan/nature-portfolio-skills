"""C08 -- Radar chart for a multi-metric profile of 2-4 methods.
Use when: 4-8 normalised figures of merit and the *profile* (trade-off) matters. Prefer a table or dot plot
when exact values matter; radar areas exaggerate differences.
Nature notes: normalise every axis to [0, 1] with 'larger = better' and say so; thin lines, light fills.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
metrics = [f"Metric {i}" for i in range(1, 7)]
series = {"Method A": [0.35, 0.95, 0.80, 0.55, 0.10, 0.85],
          "Method B": [0.45, 0.80, 0.35, 0.90, 0.85, 0.50],
          "Method C (ours)": [0.95, 0.70, 0.85, 0.75, 0.80, 0.70]}
# -------------------------------------------

fig = plt.figure(figsize=figsize_mm(70, 62))
ax = fig.add_subplot(111, projection="polar")
radar(ax, metrics, series, colors=["0.45", PALETTE["blue"], PALETTE["red"]])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncols=1, handlelength=1.4)
export(fig, "C08_radar")
