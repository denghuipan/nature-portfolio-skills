"""S05 -- Qualitative concept plots: trade-off (a), regime map (b) and before/after (c), drawn on sketch axes
(arrow heads, no numbers).
Use when: the point is a direction or a relation, not a value -- intro / perspective figures, graphical
abstracts. Use real axes as soon as numbers are claimed.
Nature notes: one highlight colour for 'this work'; regions shaded lightly and named in the region.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

fig, axes = plt.subplots(1, 3, figsize=figsize_2col(52), gridspec_kw=dict(wspace=0.35))
a, b, c = axes
t = np.linspace(0.08, 1, 200)
for ax_ in axes:
    ax_.set_xlim(0, 1.05); ax_.set_ylim(0, 1.05)
# (a) trade-off frontier
front = 0.12 / t
a.plot(t, np.clip(front, 0, 1.0), color="0.5", lw=1.0)
rng = np.random.default_rng(3)
xs = rng.uniform(0.15, 0.95, 12); ys = 0.12 / xs * rng.uniform(0.55, 0.95, 12)
a.plot(xs, ys, "o", ms=3, mfc="0.75", mec="0.45", mew=0.4)
a.plot(0.75, 0.72, "*", ms=9, mfc=PALETTE["red"], mec="k", mew=0.5)
arrow(a, (0.42, 0.33), (0.70, 0.66), color=PALETTE["red"], lw=1.0)
a.text(0.75, 0.80, "This work", color=PALETTE["red"], ha="center", va="bottom", fontsize=6)
a.text(0.80, 0.21, "previous limit", color="0.45", ha="center", fontsize=5.5, rotation=-6)
concept_axes(a, "Metric 1", "Metric 2")
# (b) regime map
xx = np.linspace(0, 1.05, 200)
b1 = 0.25 + 0.5 * xx ** 2; b2 = 0.7 + 0.1 * xx
b.fill_between(xx, 0, np.minimum(b1, 1.05), color=PALETTE["lightblue"], alpha=0.35, lw=0)
b.fill_between(xx, np.minimum(b1, 1.05), np.minimum(np.maximum(b1, b2), 1.05), color=PALETTE["sand"], alpha=0.5, lw=0)
b.fill_between(xx, np.minimum(np.maximum(b1, b2), 1.05), 1.05, color=PALETTE["rose"], alpha=0.35, lw=0)
b.plot(xx, np.minimum(b1, 1.05), color="0.35", lw=0.8); b.plot(xx, np.maximum(b1, b2).clip(0, 1.05), color="0.35", lw=0.8, ls=(0, (3, 2)))
for txt, (px, py) in {"Regime I": (0.55, 0.15), "Regime II": (0.30, 0.52), "Regime III": (0.35, 0.92)}.items():
    b.text(px, py, txt, ha="center", va="center", fontsize=6)
concept_axes(b, "Parameter 1", "Parameter 2")
# (c) before / after
xc = np.linspace(0, 1.05, 300)
c.plot(xc, 0.55 * np.exp(-((xc - 0.5) / 0.22) ** 2) + 0.05, color="0.55", lw=1.0)
c.fill_between(xc, 0.05, 0.9 * np.exp(-((xc - 0.5) / 0.07) ** 2) + 0.05, color=PALETTE["red"], alpha=0.18, lw=0)
c.plot(xc, 0.9 * np.exp(-((xc - 0.5) / 0.07) ** 2) + 0.05, color=PALETTE["red"], lw=1.0)
c.text(0.15, 0.40, "Before", color="0.45", fontsize=6, ha="center")
c.text(0.68, 0.85, "After", color=PALETTE["red"], fontsize=6, ha="left")
concept_axes(c, "Variable", "Response")
for ax_, l in zip(axes, "abc"):
    panel_label(ax_, l, dx=-0.12, dy=1.08)
export(fig, "S05_concept_sketch")
