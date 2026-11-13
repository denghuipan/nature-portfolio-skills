"""C05 -- Benchmark landscape: where this work sits among published results.
Use when: a comparison figure (metric X vs metric Y) with numbered references.
Nature notes: one marker shape per class (shape survives greyscale and colour blindness), reference numbers
next to points without overlaps, target region shaded, 'this work' the only red item. Every point must be
traceable to a reference listed in the caption / Source Data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA (random placeholders) ----------------
rng = np.random.default_rng(13)
styles = {"c1": dict(marker="o", color=PALETTE["blue"], label="Class 1"),
          "c2": dict(marker="h", color=PALETTE["skyblue"], label="Class 2"),
          "c3": dict(marker="D", color=PALETTE["purple"], label="Class 3", ms=4),
          "c4": dict(marker="s", color=PALETTE["green"], label="Class 4"),
          "c5": dict(marker="^", color=PALETTE["sand"], label="Class 5"),
          "c6": dict(marker="v", color="0.35", label="Class 6")}
entries, ref = [], 1
for cat, (n, xr, yr) in {"c1": (5, (20, 300), (0.01, 10)), "c2": (3, (80, 1200), (0.01, 1)),
                          "c3": (2, (40, 60), (0.05, 1)), "c4": (9, (10, 600), (0.005, 5)),
                          "c5": (11, (80, 800), (0.05, 30)), "c6": (3, (20, 1500), (0.3, 8))}.items():
    for _ in range(n):
        entries.append(dict(x=float(np.exp(rng.uniform(*np.log(xr)))), y=float(np.exp(rng.uniform(*np.log(yr)))),
                            cat=cat, ref=ref))
        ref += 1
this = dict(x=440, y=0.05, label="This work", color=PALETTE["red"], marker="*", ms=9)
# -------------------------------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(89, 78))
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(5, 1e4); ax.set_ylim(3e-3, 300)
landscape(ax, entries, styles, this_work=this, target=(440, 1e4, 3e-3, 0.05), legend_loc="lower left", legend_ncols=4)
leg = ax.get_legend(); leg.set_bbox_to_anchor((0, 1.0))
ax.axvline(440, color="0.55", ls=":", lw=0.6); ax.axhline(0.05, color="0.55", ls=":", lw=0.6)
ax.set_xlabel("Metric X (unit)"); ax.set_ylabel("Metric Y (unit)")
log_ticks(ax.xaxis); log_ticks(ax.yaxis)
fmt = mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}")
ax.xaxis.set_major_formatter(fmt); ax.yaxis.set_major_formatter(fmt)
style_axes(ax)
export(fig, "C05_landscape")
