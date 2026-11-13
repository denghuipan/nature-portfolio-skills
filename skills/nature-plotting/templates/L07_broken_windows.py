"""L07 -- Narrow x windows of one long axis side by side (broken axis).
Use when: features are narrow and far apart, so a continuous axis would leave them as hairlines.
Nature notes: mark every break with // on the frame; share the y axis; tint each window by its own colour
so colour identifies the window without a legend; say the window width in the axis label.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
centres = np.arange(10, 91, 10)
rng = np.random.default_rng(3)
def peak(x, c, w):
    return np.sinc((x - c) / w) ** 2
windows = []
for i, c in enumerate(centres):
    x = np.linspace(c - 3, c + 3, 400)
    w = 0.7 + 0.04 * i
    windows.append((x, peak(x, c, w), peak(x, c + rng.normal(0, 0.02), w * 1.02) * (1 - 0.02 * i)))
# -------------------------------------------

fig = plt.figure(figsize=figsize_2col(44))
gs = fig.add_gridspec(1, 1, left=0.07, right=0.99, bottom=0.22, top=0.84)
axes = broken_windows(fig, gs[0], [(c - 3, c + 3) for c in centres], wspace=0.06)
cols = n_colors(truncate_cmap(NS_GLACIER, 0.1, 0.75), len(centres))
for ax, c, colr, (x, d1, d2) in zip(axes, centres, cols, windows):
    tint_axes(ax, colr, a_bottom=0.10, a_top=0.0)
    gradient_fill(ax, x, d1, color=colr, alpha=0.95)
    ax.plot(x, d1, color=colr, lw=0.5)
    ax.plot(x, d2, color="k", ls=(0, (2.2, 1.2)), lw=0.8)
    ax.set_xticks([c]); ax.set_xticklabels([f"{c}"])
    ax.tick_params(axis="x", which="minor", bottom=False, top=False)
    ax.set_ylim(0, 1.15)
axes[0].set_ylabel("Signal (norm.)"); axes[0].set_yticks([0, 0.5, 1])
fig.text(0.53, 0.02, "Position (unit; each window ±3)", ha="center", va="bottom",
         fontsize=mpl.rcParams["axes.labelsize"])
fig.legend(handles=[mpl.patches.Patch(color="0.6", label="Data 1 (fill)"),
                    mpl.lines.Line2D([], [], color="k", ls=(0, (2.2, 1.2)), lw=0.8, label="Data 2")],
           loc="upper right", bbox_to_anchor=(0.99, 1.0), ncols=2, handlelength=1.6)
export(fig, "L07_broken_windows")
