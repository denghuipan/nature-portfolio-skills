"""C03 -- Mirrored (butterfly) counts: left vs right, before vs after, group 1 vs group 2, per category.
Use when: the same categories are counted in two matched halves and the symmetry (or its absence) is the
point; categories fall into a few named groups.
Look: no axes at all, labels in a centre column, counts written at the bar ends with thousands separators,
dashed rules between groups, square brackets with group names on the side, one colour per group.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
cats = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9"]
left = [8633, 1111, 39060, 16136, 4016, 265, 646, 52, 40]
right = [8164, 1251, 38476, 16163, 4037, 259, 649, 54, 40]
group = [0, 0, 1, 1, 1, 1, 2, 2, 2]               # three groups of classes
gnames = ["Group I", "Group II", "Group III"]
small = ["Part 1", "Part 2", "Part 3", "Part 4", "Part 5", "Part 6"]
sl = [1767, 1743, 945, 100, 66, 42]
sr = [1912, 1688, 944, 97, 65, 43]
# -------------------------------------------
gcol = [PALETTE["sage"], PALETTE["ochre"], "0.25"]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(150, 62), gridspec_kw=dict(width_ratios=[1.25, 1]))
fig.subplots_adjust(left=0.02, right=0.9, wspace=0.35, top=0.86, bottom=0.04)
butterfly(a, cats, left, right, colors=[gcol[g] for g in group], separators=[1, 5], gap=0.24)
for g, nm in enumerate(gnames):
    rows = [i for i, gg in enumerate(group) if gg == g]
    bracket_label(a, rows[0] - 0.3, rows[-1] + 0.3, nm, x=1.0)
subtitle(a, "Counts per class", pad=8)
butterfly(b, small, sl, sr, colors="0.15", gap=0.2)
subtitle(b, "Counts per part", pad=8)
panel_label(a, "a", dx=0.0, dy=1.13); panel_label(b, "b", dx=0.0, dy=1.13)
export(fig, "C03_butterfly_counts")
