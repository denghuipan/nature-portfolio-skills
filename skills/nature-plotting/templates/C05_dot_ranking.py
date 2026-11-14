"""C05 -- Ranked dot plot with intervals (Cleveland style): many methods / sites / models on one score.
Use when: 10-40 entries are ranked by an estimate with an uncertainty, and bars would waste ink; one or two
entries are of special interest.
Look: open bottom axis, faint row guides instead of a y axis, grey dots and thin interval lines, the entries
of interest in the main colour, a dashed reference value with its label above the plot.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(9)
names = [f"Entry {i}" for i in range(1, 19)]
est = np.sort(rng.normal(0.62, 0.1, len(names)))
half = rng.uniform(0.02, 0.07, len(names))
focus = {names[-1]: "Entry 18 (proposed)", names[9]: "Entry 10 (previous)"}
ref = 0.6
# -------------------------------------------
fig, ax = plt.subplots(figsize=figsize_mm(70, 82))
fig.subplots_adjust(left=0.27, right=0.96, bottom=0.11, top=0.93)
y = np.arange(len(names))
for yi in y:
    ax.axhline(yi, color="0.93", lw=0.5, zorder=0)
for yi, n, e, h in zip(y, names, est, half):
    c = PALETTE["blue"] if n == names[-1] else PALETTE["ochre"] if n in focus else "0.55"
    ax.plot([e - h, e + h], [yi, yi], color=c, lw=0.8, solid_capstyle="butt")
    ax.plot(e, yi, "o", color=c, ms=3.2 if n in focus else 2.6)
ax.axvline(ref, color="0.3", ls=(0, (3, 2)), lw=0.6)
ax.text(ref, len(names) - 0.2, "Reference", ha="center", va="bottom", fontsize=6, color="0.3")
ax.set_yticks(y, [focus.get(n, n) for n in names])
for t, n in zip(ax.get_yticklabels(), names):
    if n in focus:
        t.set_color(PALETTE["blue"] if n == names[-1] else PALETTE["ochre"])
despine(ax, left=True)
ax.set_ylim(-0.8, len(names) + 0.4)
ax.set_xlabel("Score (95% CI)")
export(fig, "C05_dot_ranking")
