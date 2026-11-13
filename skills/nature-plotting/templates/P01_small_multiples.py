"""P01 -- Small multiples: the same comparison repeated for many samples, one panel each.
Use when: showing 6-12 examples (samples, conditions, channels) with identical axis logic.
Nature notes: in-panel labels (sample at left, score at right) replace titles; one x and one y label for the
block; reference = colour gradient fill, Data 2 = black dashed, Data 3 = grey dotted, band = light grey.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(11)
centres = np.linspace(10, 90, 9)
def peak(x, c, w):
    return np.sinc((x - c) / w) ** 2
panels = []
for i, c in enumerate(centres):
    x = np.linspace(c - 6, c + 6, 300)
    w = 0.9 + 0.12 * i
    ref = peak(x, c, w)
    d2 = peak(x, c + rng.normal(0, 0.03), w * (1 + rng.normal(0, 0.02))) * (0.65 if i == 8 else 1)
    d3 = peak(x, c, w * 1.3) * (0.5 + 0.1 * rng.random()) + 0.04 * rng.random(x.size)
    score = 1 - abs(rng.normal(0, 0.006)) - (0.42 if i == 8 else 0)
    panels.append((x, ref, d2, d3, d2 * 0.93 - 0.02, d2 * 1.05 + 0.02, score))
# -------------------------------------------

fig, axes = plt.subplots(3, 3, figsize=figsize_mm(89, 72), sharey=True, gridspec_kw=dict(hspace=0.42, wspace=0.10))
cols = n_colors(truncate_cmap(NS_GLACIER, 0.1, 0.8), 9)
for k, (ax, c, (x, ref, d2, d3, lo, hi, score)) in enumerate(zip(axes.flat, cols, panels)):
    gradient_fill(ax, x, ref, color=c, alpha=0.85)
    ci_band(ax, x, lo, hi, "0.6", alpha=0.35)
    ax.plot(x, d3, color="0.55", ls=":", lw=0.8)
    ax.plot(x, d2, color="k", ls=(0, (2.5, 1.2)), lw=0.8)
    ax.set_xlim(x[0], x[-1]); ax.set_ylim(0, 1.25)
    ax.set_xticks([round(x[0]) + 1, round(x[-1]) - 1]); ax.set_yticks([0, 1])
    ax.text(0.04, 0.95, f"S{k + 1}", transform=ax.transAxes, ha="left", va="top", fontweight="bold", fontsize=5.5)
    ax.text(0.96, 0.95, f"{score:.2f}", transform=ax.transAxes, ha="right", va="top", fontsize=5.5, color="0.4")
    style_axes(ax)
from matplotlib.lines import Line2D
fig.legend(handles=[mpl.patches.Patch(color=cols[3], alpha=0.6, lw=0, label="Data 1"),
                    Line2D([], [], color="k", ls=(0, (2.5, 1.2)), lw=0.8, label="Data 2"),
                    Line2D([], [], color="0.55", ls=":", lw=0.8, label="Data 3"),
                    mpl.patches.Patch(color="0.6", alpha=0.35, lw=0, label="5–95 %")],
           loc="lower center", bbox_to_anchor=(0.5, 0.93), ncols=4, handlelength=1.6, columnspacing=0.9)
share_labels(fig, axes, "Variable $x$ (unit)", "Signal (norm.)")
export(fig, "P01_small_multiples")
