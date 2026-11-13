"""K01 -- The house colour maps, with their CIE L* (lightness) profiles.
Use when: choosing a map. Sequential maps must have monotonic L*; diverging maps a light neutral centre and
matched arms; cyclic maps equal ends. The wavelength and visible maps are for wavelength keys only.
Nature notes: no rainbow / jet for ordered data; avoid red-green as the only contrast.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

groups = [("Sequential", SEQUENTIAL), ("Diverging", DIVERGING), ("Cyclic", CYCLIC), ("Special", SPECIAL)]
names = [(g, k, c) for g, d in groups for k, c in d.items()]
fig = plt.figure(figsize=figsize_2col(120))
gs = fig.add_gridspec(len(names), 2, width_ratios=[1.6, 1], hspace=1.0, wspace=0.28,
                      left=0.17, right=0.98, top=0.97, bottom=0.07)
grad = np.linspace(0, 1, 512)[None, :]
for i, (g, k, c) in enumerate(names):
    ax = fig.add_subplot(gs[i, 0])
    ax.imshow(grad, aspect="auto", cmap=c)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(0.4)
    ax.text(-0.02, 0.5, k, transform=ax.transAxes, ha="right", va="center", fontsize=5.5)
    if i == 0 or names[i - 1][0] != g:
        ax.text(-0.02, 1.15, g, transform=ax.transAxes, ha="right", va="bottom", fontsize=6, fontweight="bold")
axL = fig.add_subplot(gs[:, 1])
for g, d in groups[:2]:
    for k, c in d.items():
        L = lightness(c)
        axL.plot(np.linspace(0, 1, L.size), L, color=c(0.55 if g == "Sequential" else 0.15), lw=0.9,
                 ls="-" if g == "Sequential" else (0, (3, 1.5)))
axL.set_xlim(0, 1); axL.set_ylim(0, 100)
axL.set_xlabel("Position along map"); axL.set_ylabel("Lightness $L^*$")
axL.set_title("solid: sequential; dashed: diverging", fontsize=5.5, pad=3)
style_axes(axL)
export(fig, "K01_colormaps")
