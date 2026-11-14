"""T04 -- Growth over time as narrow bars, coloured by source, with comma-separated counts.
Use when: a cumulative count (records, discoveries, users, samples) grows by period and one source takes
over from another; the hand-over is the story.
Look: open axes, two tones of one hue (light = earlier source, dark = new source), bars almost touching,
year ticks only, square legend keys, thousands separators on the y axis.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
q = np.arange(2018.0, 2023.0, 0.25)                                   # quarterly bins
src = np.where(q < 2021.0, 0, 1)                                     # 0 = Source 1, 1 = Source 2
total = np.where(q < 2021.5, 24000 + 4000 * (q - 2018),
                 36000 + 360000 / (1 + np.exp(-(q - 2022.0) * 5.5)))
total = np.round(total, -2)
# -------------------------------------------
dark, light = THEMES["duo_purple"]
fig, ax = plt.subplots(figsize=figsize_mm(89, 58))
bb = ax.bar(q, total, width=0.23, color=[light if s == 0 else dark for s in src], lw=0, align="edge")
for p_, s_ in zip(bb.patches, src):
    gradient_patch(ax, p_, light if s_ == 0 else dark, light=0.55)
ax.set_xlim(2018, 2023); ax.set_ylim(0, 420000)
ax.set_xticks([2019, 2020, 2021, 2022], ["2019", "2020", "2021", "2022"])
thousands(ax, "y")
ax.set_xlabel("Year"); ax.set_ylabel("Number of entries")
square_legend(ax, ["Source 1 (reference)", "Source 2 (this study)"], [light, dark], loc="upper left")
export(fig, "T04_growth_bars")
