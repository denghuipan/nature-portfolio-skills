"""C03 -- Ranked lollipop (a) and dumbbell / paired-change (b) charts.
Use when: (a) ranking many categories by one value; (b) before/after or baseline/new per category.
Nature notes: sort by the value that carries the message; highlight only the item the paper is about;
the dumbbell shows the change itself, which two bar series cannot.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
items = [f"Item {c}" for c in "ABCDEFG"] + ["Ours"]
score = [1.2, 2.1, 2.6, 3.4, 3.9, 2.9, 3.1, 6.2]
cats = [f"Category {i}" for i in range(1, 9)]
before = [0.21, 0.35, 0.18, 0.62, 0.55, 0.48, 0.71, 0.66]
after = [0.05, 0.08, 0.04, 0.12, 0.15, 0.10, 0.09, 0.11]
# -------------------------------------------

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_2col(58), gridspec_kw=dict(wspace=0.6))
lollipop(a, items, score, highlight="Ours", value_fmt="{:.1f}")
a.set_xlim(0, 7.5); a.set_xlabel("Score (a.u.)")
style_axes(a); a.tick_params(axis="y", which="both", left=False, right=False)
h1, h2 = dumbbell(b, cats, before, after, names=("Before", "After"))
b.set_xlim(0, 0.8); b.set_xlabel("Error (unit)")
b.legend(handles=[h1, h2], loc="lower left", bbox_to_anchor=(0, 1.0), ncols=2)
style_axes(b); b.tick_params(axis="y", which="both", left=False, right=False)
panel_label(a, "a", dx=-0.42, dy=1.12); panel_label(b, "b", dx=-0.48, dy=1.12)
export(fig, "C03_lollipop_dumbbell")
