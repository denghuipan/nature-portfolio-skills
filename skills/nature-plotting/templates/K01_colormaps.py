"""K01 -- The house colour maps with their lightness profiles.
Use when: choosing a map. Sequential maps must get monotonically darker (or lighter); diverging maps are
symmetric in lightness about a neutral centre; cyclic maps start and end on the same colour.
Look: thin swatches labelled at the left, grouped by kind; right: CIE L* along each map.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
groups = [("Sequential", SEQUENTIAL), ("Diverging", DIVERGING), ("Cyclic", CYCLIC), ("True colour", SPECIAL)]
# -------------------------------------------
names = [(g, k, c) for g, d in groups for k, c in d.items()]
fig = plt.figure(figsize=figsize_2col(100))
gs = fig.add_gridspec(len(names), 2, width_ratios=[1.5, 1], hspace=0.9, wspace=0.3,
                      left=0.13, right=0.98, top=0.97, bottom=0.09)
grad = np.linspace(0, 1, 512)[None, :]
for i, (g, k, c) in enumerate(names):
    ax = fig.add_subplot(gs[i, 0])
    ax.imshow(grad, aspect="auto", cmap=c)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(-0.015, 0.5, k, transform=ax.transAxes, ha="right", va="center", fontsize=6)
    if i == 0 or names[i - 1][0] != g:
        ax.text(1.0, 1.25, g, transform=ax.transAxes, ha="right", va="bottom", fontsize=6, color="0.4")
axL = fig.add_subplot(gs[:, 1])
for g, d in groups[:3]:
    for k, c in d.items():
        L = lightness(c)
        axL.plot(np.linspace(0, 1, L.size), L, color=c(0.62 if g == "Sequential" else 0.15), lw=0.9,
                 ls="-" if g == "Sequential" else (0, (3, 1.5)) if g == "Diverging" else (0, (1, 1)))
axL.set_xlim(0, 1); axL.set_ylim(0, 100)
axL.set_xlabel("Position along map"); axL.set_ylabel("Lightness $L^*$")
axL.text(0.5, 1.01, "solid: sequential; dashed: diverging; dotted: cyclic", transform=axL.transAxes,
         ha="center", va="bottom", fontsize=6, color="0.4")
export(fig, "K01_colormaps")
