"""T06 -- Composition over time: stacked areas with direct labels, and the same data as shares.
Use when: a total is split into 3-6 parts that change over time (sources, classes, sectors) and readers need
both the total and how the mix shifts.
Look: open axes, thin white separators between layers, labels written inside the layers (no legend),
right panel as lines of percentage share with end labels.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
t = np.arange(2000, 2031)
u = (t - 2000) / 30
parts = {
    "Part 1": 40 - 18 * u,
    "Part 2": 22 + 4 * np.sin(u * 4),
    "Part 3": 6 + 30 / (1 + np.exp(-(u - 0.6) * 10)),
    "Part 4": 10 + 8 * u,
    "Part 5": 4 + 2 * u,
}
# -------------------------------------------
names = list(parts)
cols = [PALETTE["blue"], PALETTE["sky"], PALETTE["ochre"], PALETTE["teal"], PALETTE["lightgrey"]]
Y = np.array([parts[k] for k in names])
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_2col(58), gridspec_kw=dict(width_ratios=[1.25, 1]))
fig.subplots_adjust(wspace=0.32, left=0.07, right=0.93, bottom=0.17, top=0.92)
area_stack(a, t, Y, cols, labels=names, label_x=2024)
a.set_xlim(2000, 2030); a.set_ylim(0, 110); a.set_ylabel("Amount (unit)"); a.set_xlabel("Year")
share = Y / Y.sum(0) * 100
for k, (nm, c) in enumerate(zip(names, cols)):
    b.plot(t, share[k], color=darken(c, 0.15) if c != PALETTE["lightgrey"] else "0.55", lw=1.0)
end_labels(b, t[-1], share[:, -1], names,
           colors=[darken(c, 0.15) if c != PALETTE["lightgrey"] else "0.45" for c in cols])
b.set_xlim(2000, 2030); b.set_ylim(0, 50); b.set_ylabel("Share of total (%)"); b.set_xlabel("Year")
panel_label(a, "a", dx=-0.13, dy=1.06); panel_label(b, "b", dx=-0.16, dy=1.06)
export(fig, "T06_stacked_area")
