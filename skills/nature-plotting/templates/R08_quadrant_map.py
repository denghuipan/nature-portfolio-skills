"""R08 -- Quadrant map: two scores per item, split at reference values into four named regions.
Use when: items are classified by two criteria at once (fast & accurate, cheap & robust ...) and readers
should see which items land in the desirable corner, with a few of them named.
Look: open axes, reference lines at the split values, the target quadrant lightly tinted, region names in
the corners in grey, points sized by a third quantity, a few labelled points with short leader lines.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(53)
n = 60
s1 = rng.beta(4, 3, n) * 100
s2 = np.clip(0.4 * s1 + rng.normal(30, 15, n), 3, 90)
w = rng.lognormal(1, 0.6, n)
split = (60, 60)
named = np.argsort(-(s1 + s2))[:4].tolist() + [int(np.argmin(s2))]
# -------------------------------------------
fig, ax = plt.subplots(figsize=figsize_mm(80, 72))
fig.subplots_adjust(left=0.13, right=0.97, bottom=0.13, top=0.97)
gradient_image(ax, (split[0], 100, split[1], 100), [mcolors.to_rgba(PALETTE["teal"], 0.04), mcolors.to_rgba(PALETTE["teal"], 0.32)],
               direction="right", zorder=0)
for v, f in ((split[0], ax.axvline), (split[1], ax.axhline)):
    f(v, color="0.45", lw=0.5, ls=(0, (3, 2)), zorder=1)
inside = (s1 >= split[0]) & (s2 >= split[1])
ax.scatter(s1[~inside], s2[~inside], s=6 + 10 * w[~inside], color="0.7", lw=0, zorder=2)
ax.scatter(s1[inside], s2[inside], s=6 + 10 * w[inside], color=PALETTE["teal"], lw=0, zorder=3)
for t, (x, y, ha, va) in {"High 1 / high 2": (99, 99, "right", "top"), "Low 1 / high 2": (1, 99, "left", "top"),
                          "Low 1 / low 2": (1, 1, "left", "bottom"), "High 1 / low 2": (99, 1, "right", "bottom")}.items():
    ax.text(x, y, t, ha=ha, va=va, color="0.45")
for k, i in enumerate(named):
    ax.annotate(f"Item {i + 1}", (s1[i], s2[i]), xytext=(8, -8 + 5 * (k % 3)), textcoords="offset points", va="center", arrowprops=dict(arrowstyle="-", lw=0.4, color="0.3", shrinkA=0, shrinkB=2))
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.set_xlabel("Score 1"); ax.set_ylabel("Score 2")
export(fig, "R08_quadrant_map")
