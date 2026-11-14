"""C02 -- Overlaid bars: a reference set drawn inside a larger set, on log and on linear axes.
Use when: counts by category where a new collection contains (and dwarfs) an older one; the log panel shows
both, the linear panel shows the absolute gain.
Look: open axes, one hue in two tones (dark = total, light = reference subset in front), thin white edge
between them, square legend keys, comma separators on the linear axis, decade ticks on the log axis.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
k = np.array([2, 3, 4, 5, 6])                         # category (e.g. number of components)
total_a = np.array([7.2e3, 7.6e4, 2.3e5, 8.6e4, 3.0e3])
ref_a = np.array([4.9e3, 1.9e4, 7.0e3, 1.3e3, 0])
total_b = np.array([2600, 12900, 23100, 13800, 450])
ref_b = np.array([1100, 4200, 2300, 120, 0])
# -------------------------------------------
dark, light = THEMES["duo_purple"]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 52))
fig.subplots_adjust(wspace=0.42, left=0.11, right=0.98, bottom=0.2, top=0.93)
overlay_bars(a, k, ref_a + 1, total_a, [dark, light], labels=["Collection 2", "Collection 1"], width=0.78, log=True)
a.set_ylim(1e3, 4e5); a.set_ylabel("Count")
overlay_bars(b, k, ref_b, total_b, [dark, light], labels=["Collection 2", "Collection 1"], width=0.78)
b.set_ylim(0, 25000); thousands(b); b.set_ylabel("Distinct types")
for ax in (a, b):
    ax.set_xticks(k); ax.set_xlabel("Number of components"); ax.tick_params(axis="x", length=0)
    square_legend(ax, ["Collection 2", "Collection 1"], [dark, light], loc="upper right")
panel_label(a, "a", dx=-0.3, dy=1.06); panel_label(b, "b", dx=-0.32, dy=1.06)
export(fig, "C02_overlay_bars")
