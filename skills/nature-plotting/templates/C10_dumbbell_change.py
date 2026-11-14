"""C10 -- Dumbbell chart: the same items under two conditions, sorted by the size of the change.
Use when: 8-25 items each have a 'before' and 'after' (or two methods), and both the levels and the gap
matter; colour encodes whether the change is a gain or a loss.
Look: open bottom axis, faint row guides, grey hollow dot for the first value, filled coloured dot for the
second, connector coloured by direction, difference written at the right margin.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(21)
items = [f"Item {i}" for i in range(1, 15)]
a = rng.uniform(30, 70, len(items))
b = a + rng.normal(6, 9, len(items))
# -------------------------------------------
order = np.argsort(b - a)
up, down = THEMES["updown"][0], THEMES["updown"][1]
fig, ax = plt.subplots(figsize=figsize_mm(80, 74))
fig.subplots_adjust(left=0.2, right=0.86, bottom=0.12, top=0.9)
for yi, i in enumerate(order):
    d = b[i] - a[i]
    c = up if d > 0 else down
    ax.axhline(yi, color="0.94", lw=0.5, zorder=0)
    ax.plot([a[i], b[i]], [yi, yi], color=lighten(c, 0.35), lw=1.4, solid_capstyle="butt", zorder=1)
    ax.plot(a[i], yi, "o", ms=3.4, mfc="white", mec="0.45", mew=0.7, zorder=2)
    ax.plot(b[i], yi, "o", ms=3.4, color=c, zorder=3)
    ax.text(1.02, yi, f"{d:+.1f}", transform=ax.get_yaxis_transform(), va="center", fontsize=6, color=c)
ax.set_yticks(range(len(items)), [items[i] for i in order]); ax.tick_params(axis="y", length=0)
despine(ax, left=True)
ax.set_xlabel("Value (unit)")
ax.plot([], [], "o", ms=3.4, mfc="white", mec="0.45", mew=0.7, label="Condition 1")
ax.plot([], [], "o", ms=3.4, color="0.3", label="Condition 2")
ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncols=2)
ax.text(1.02, 1.0, "Δ", transform=ax.transAxes, fontsize=6, va="bottom", color="0.3")
export(fig, "C10_dumbbell_change")
