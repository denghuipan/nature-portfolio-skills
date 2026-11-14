"""C07 -- Table figure beside a scatter: exact values where they matter, the overall pattern next to them.
Use when: a results table is the main evidence (sizes, best known value, new value) and a companion scatter
shows the improvement across many more cases, with the notable ones labelled.
Look: zebra-striped rows, header between two rules, a double rule between table blocks, improved values in
colour, scatter with plain dots and black-edged, labelled highlights.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(12)
sizes = ["(2, 2, 2)", "(3, 3, 3)", "(4, 4, 4)", "(5, 5, 5)", "(2, 2, 3)", "(2, 3, 4)", "(3, 3, 4)",
         "(3, 4, 5)", "(4, 4, 5)", "(4, 5, 5)"]
known = [7, 23, 49, 98, 11, 20, 29, 48, 64, 80]
new_a = [7, 23, 47, 96, 11, 20, 29, 47, 63, 76]
new_b = [7, 23, 49, 98, 11, 20, 29, 47, 63, 76]
src = ["Ref. 1", "Ref. 2", "Ref. 1", "Ref. 3", "Ref. 4", "Ref. 4", "Ref. 5", "Ref. 5", "Ref. 6", "Ref. 6"]
bx = rng.uniform(80, 900, 70)
by = np.clip(np.round(0.022 * bx * rng.uniform(0.3, 1.4, 70)), 1, None)
hl = np.array([5, 17, 29, 41, 53, 65])                 # a few notable cases, spread along x
bx[hl] = [180, 330, 470, 610, 760, 900]; by[hl] = [9, 16, 13, 24, 20, 30]
hl_lab = [f"({a}, {b}, {c})" for a, b, c in rng.integers(9, 13, (6, 3))]
# -------------------------------------------
better = PALETTE["brick"]
cells, colors = [], []
for s, k, a, b, r in zip(sizes, known, new_a, new_b, src):
    cells.append([s, r, f"{k}", f"{a}", f"{b}"])
    colors.append(["0.1", PALETTE["plum"], "0.1", better if a < k else "0.1", better if b < k else "0.1"])
fig = plt.figure(figsize=figsize_2col(78))
t = fig.add_axes([0.0, 0.03, 0.56, 0.84])
zebra_table(t, cells, ["Size\n(n, m, p)", "Best method\nknown", "Best value\nknown", "New value\nsetting A",
                       "New value\nsetting B"], [0.1, 0.36, 0.6, 0.79, 0.95], colors=colors, group_breaks=[3])
s = fig.add_axes([0.65, 0.12, 0.33, 0.8])
mask = np.zeros(bx.size, bool); mask[hl] = True
highlight_points(s, bx, by, mask, labels=hl_lab, base_color=better, s=6, hl_s=18)
s.set_xlim(0, 1000); s.set_ylim(0, by.max() * 1.15)
thousands(s, "x")
s.set_xlabel("Best value known"); s.set_ylabel("Improvement")
fig.text(0.0, 0.99, "a", fontsize=8, fontweight="bold", va="top")
fig.text(0.59, 0.99, "b", fontsize=8, fontweight="bold", va="top")
export(fig, "C07_table_scatter")
