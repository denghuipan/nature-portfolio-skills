"""C01 -- Bars with error bars AND the individual measurements.
Use when: a few groups, each with a small number of repeats. Nature asks to show the data points whenever
n is small; a bar alone hides the distribution.
Nature notes: state centre and error definition (mean +- s.d., n = 5) in the panel or legend.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
groups = ["Group A", "Group B", "Group C", "Group D"]
rng = np.random.default_rng(21)
obs = [rng.normal(m, s, 5) for m, s in [(3.1, 0.25), (4.8, 0.35), (5.8, 0.3), (4.4, 0.5)]]
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(60, 52))
x = np.arange(len(groups))
bars(ax, x, [o.mean() for o in obs], colors=[PALETTE["lightblue"]] * 3 + [PALETTE["rose"]],
     err=[o.std(ddof=1) for o in obs], points=obs, point_color="0.15", width=0.6)
ax.set_xticks(x, groups); ax.set_ylim(0, 7.5); ax.set_ylabel("Value (unit)")
stats_text(ax, ["mean ± s.d., n = 5"], loc="upper left")
style_axes(ax); ax.tick_params(axis="x", which="both", bottom=False, top=False)
export(fig, "C01_bar_points")
