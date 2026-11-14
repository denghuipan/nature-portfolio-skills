"""S05 -- Qualitative concept sketches: scaling regimes, an energy landscape and set overlaps.
Use when: an idea needs a picture but no numbers (introduction figures, mechanism panels, extended data
explanations); sketch axes without ticks say 'qualitative'.
Look: arrow-headed sketch axes, smooth curves in two or three hues, short italic labels on the curves,
dashed guides, translucent circles for sets with counts written inside.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
from nature_schematic import *  # noqa: F401,F403  mm-canvas diagram primitives
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
set_counts = {"A": 412, "B": 268, "C": 190, "AB": 88, "AC": 51, "BC": 47, "ABC": 23}
# -------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=figsize_2col(56))
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.14, top=0.9, wspace=0.3)
a, b, c = axs
# a: two scaling regimes and the crossover
x = np.logspace(0, 3, 200)
y1 = x ** 1.0; y2 = 0.02 * x ** 2.0
a.loglog(x, y1, color=PALETTE["blue"], lw=1.1)
a.loglog(x, y2, color=PALETTE["ochre"], lw=1.1)
a.loglog(x, np.maximum(y1, y2), color="0.15", lw=0.6, ls=(0, (3, 2)))
a.text(4, 7, r"$\propto N$", color=PALETTE["blue"], rotation=28)
a.text(250, 2600, r"$\propto N^{2}$", color=PALETTE["ochre"], rotation=45, ha="right")
a.axvline(50, color="0.6", lw=0.5, ls=(0, (1.5, 1.5)))
a.text(50, 0.5, " crossover", color="0.4", va="bottom")
concept_axes(a, "System size", "Cost")
a.set_xlim(1, 1000); a.set_ylim(0.3, 3e4)
# b: double-well landscape with a transition
q = np.linspace(-2.1, 2.1, 300)
E = 0.6 * q ** 4 - 2.0 * q ** 2 + 0.35 * q + 2.2
b.plot(q, E, color="0.15", lw=1.1)
qa, qb, qt = -1.33, 1.24, 0.09
for qq, nm, col in ((qa, "State 1", PALETTE["blue"]), (qb, "State 2", PALETTE["teal"])):
    e = 0.6 * qq ** 4 - 2.0 * qq ** 2 + 0.35 * qq + 2.2
    b.plot(qq, e + 0.12, "o", color=col, ms=5)
    b.text(qq, e - 0.35, nm, ha="center", va="top", color=col)
et = 0.6 * qt ** 4 - 2.0 * qt ** 2 + 0.35 * qt + 2.2
b.annotate("", xy=(qb - 0.2, 1.2), xytext=(qa + 0.2, 0.8),
           arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.55", lw=0.8, color=PALETTE["plum"],
                           mutation_scale=6))
b.plot([qa, qt + 0.45], [et, et], color="0.6", lw=0.5, ls=(0, (2, 1.5)))
eqa = 0.6 * qa ** 4 - 2.0 * qa ** 2 + 0.35 * qa + 2.2
b.annotate("", xy=(qa - 0.35, et), xytext=(qa - 0.35, eqa), arrowprops=dict(arrowstyle="<->", lw=0.6, color="0.35",
                                                                         mutation_scale=4, shrinkA=0, shrinkB=0))
b.text(qa - 0.45, (et + eqa) / 2, r"$\Delta E$", ha="right", va="center")
concept_axes(b, "Reaction coordinate", "Energy")
b.set_xlim(-2.3, 2.3); b.set_ylim(-0.6, 4.6)
# c: three overlapping sets with counts
cent = {"A": (-0.55, 0.32), "B": (0.55, 0.32), "C": (0.0, -0.6)}
setcol = {"A": PALETTE["blue"], "B": PALETTE["ochre"], "C": PALETTE["teal"]}
for k, (cx, cy) in cent.items():
    c.add_patch(plt.Circle((cx, cy), 1.0, fc=mcolors.to_rgba(setcol[k], 0.18), ec=setcol[k], lw=0.9))
    lx, ly = {"A": (-1.45, 1.42), "B": (1.45, 1.42), "C": (0.0, -1.82)}[k]
    c.text(lx, ly, f"Set {k}", ha="center", va="center", color=darken(setcol[k], 0.15))
pos = {"A": (-1.0, 0.6), "B": (1.0, 0.6), "C": (0, -1.15), "AB": (0, 0.85), "AC": (-0.72, -0.4),
       "BC": (0.72, -0.4), "ABC": (0, 0.0)}
for k, (px, py) in pos.items():
    c.text(px, py, f"{set_counts[k]:,}", ha="center", va="center", fontweight="bold" if k == "ABC" else "normal")
c.set_xlim(-2.0, 2.0); c.set_ylim(-2.05, 1.75); c.set_aspect("equal"); c.axis("off")
for ax_, l in zip(axs, "abc"):
    panel_label(ax_, l, dx=-0.08, dy=1.1)
export(fig, "S05_concept_sketches")
