"""C09 -- Horizontal paired bars with long category names and a percent axis.
Use when: two sets / methods are compared on a rate across a handful of categories whose names are long
(or a category value like '3 components'); horizontal bars keep the labels readable.
Look: open axes (left spine kept short, no y ticks), two tones of one hue, bars of the pair touching,
percent ticks, legend squares in the free corner.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
cats = ["Category 1 (short name)", "Category 2", "Category 3 with a long name", "Category 4", "Category 5"]
ref = np.array([0.10, 0.06, 0.18, 0.02, 0.12])
new = np.array([0.82, 0.51, 0.66, 0.33, 0.74])
# -------------------------------------------
dark, light = THEMES["duo_blue"]
fig, ax = plt.subplots(figsize=figsize_mm(89, 58))
fig.subplots_adjust(left=0.36, right=0.97, bottom=0.17, top=0.88)
y = np.arange(len(cats))[::-1] * 1.0
h = 0.36
gbarh(ax, y + h / 2, ref, light, height=h)
gbarh(ax, y - h / 2, new, dark, height=h, light=0.55)
for yi, v in zip(y - h / 2, new):
    ax.text(v + 0.01, yi, f"{v:.0%}", va="center")
ax.set_yticks(y, cats); ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 0.95); ax.set_xticks([0.1, 0.3, 0.5, 0.7, 0.9]); percent(ax, "x")
ax.set_xlabel("Precision of prediction")
square_legend(ax, ["Reference data", "This study"], [light, dark], loc="lower left", bbox=(0.0, 1.0), ncols=2)
export(fig, "C09_horizontal_pairs")
