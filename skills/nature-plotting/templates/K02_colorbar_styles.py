"""K02 -- Nine colour-bar styles in Nature figures, each built with one helper from nature_cmaps.
a slim side bar with extend triangles      cbar_side(..., extend="both")
b inset horizontal bar, label above        cbar_inset(...)
c bar on top of a wide map                  cbar_top(...)
d binned (discrete levels)                  cbar_discrete(bounds=...)
e categorical (named classes)               cbar_discrete(categories=...)
f logarithmic (decades)                     LogNorm + cbar_side
g diverging, centre pinned, asymmetric      center_norm + cbar_side
h normalised image, end labels              cbar_endlabels
i line family coloured by a parameter       line_mappable + cbar_side
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

x = np.linspace(-2, 2, 160); X, Y = np.meshgrid(x, x)
Z = np.exp(-(X ** 2 + Y ** 2)) + 0.4 * np.exp(-((X - 1) ** 2 + (Y + 1) ** 2) / 0.3)

fig, axes = plt.subplots(3, 3, figsize=figsize_2col(150), gridspec_kw=dict(wspace=0.75, hspace=0.62))
ax = axes[0, 0]
im = ax.imshow(Z, cmap=NS_EMBER, vmin=0.1, vmax=1.0, origin="lower")
cbar_side(ax, im, "Intensity (a.u.)", extend="both", ticks=[0.1, 0.5, 1.0])
ax = axes[0, 1]
im = ax.imshow(Z, cmap=NS_GLACIER.reversed(), origin="lower")
cbar_inset(ax, im, "Density", loc="upper right", width="45%", height="5%", ticks=[0, 0.5, 1.0])
ax = axes[0, 2]
im = ax.imshow(Z[40:120], cmap="magma", origin="lower", aspect="auto")
cbar_top(ax, im, "Amplitude (a.u.)", ticks=[0, 0.5, 1.0])
ax = axes[1, 0]
norm, cm_, cb = cbar_discrete(ax, NS_SUNSET, bounds=[0, 0.1, 0.2, 0.4, 0.7, 1.2], label="Level")
ax.imshow(Z, cmap=cm_, norm=norm, origin="lower")
ax = axes[1, 1]
cls = (Z > 0.25).astype(int) + (Z > 0.6).astype(int) + (X > 0.8).astype(int)
norm, cm_, cb = cbar_discrete(ax, mpl.colors.ListedColormap(OKABE_ITO[1:5]), categories=["Class 1", "Class 2", "Class 3", "Class 4"])
ax.imshow(cls, cmap=cm_, norm=norm, origin="lower", interpolation="nearest")
ax = axes[1, 2]
im = ax.imshow(10 ** (3 * Z - 3), cmap=NS_REDS, norm=mpl.colors.LogNorm(1e-3, 1), origin="lower")
cbar_side(ax, im, "Value", ticks=[1e-3, 1e-2, 1e-1, 1])
ax = axes[2, 0]
D = (X * np.exp(-(X ** 2 + Y ** 2) / 2)) * 3 + 0.4
im = ax.imshow(D, cmap=NS_DIV_BR, norm=center_norm(D.min(), 0, D.max()), origin="lower")
cbar_side(ax, im, "Change (a.u.)", ticks=[-1, 0, 1, 2])
ax = axes[2, 1]
im = ax.imshow(Z / Z.max(), cmap="gray", origin="lower")
cb = cbar_inset(ax, im, None, loc="lower center", width="60%", height="5%", bbox=(0, -0.22, 1, 1))
cbar_endlabels(cb, "0", "max")
ax = axes[2, 2]
sm, col = line_mappable(truncate_cmap(NS_PURPLES, 0.3, 1.0), 1, 8)
t = np.linspace(0, 1, 100)
for p in range(1, 9):
    ax.plot(t, np.sin(2 * np.pi * t) * np.exp(-t * p / 3), color=col(p), lw=0.9)
cbar_side(ax, sm, "Parameter $p$", ticks=[1, 4, 8])
for ax, l in zip(axes.flat, "abcdefghi"):
    if ax.images:
        ax.set_xticks([]); ax.set_yticks([])
    else:
        style_axes(ax); ax.set_xlabel("$t$ (unit)"); ax.set_ylabel("$y$")
    panel_label(ax, l, dx=-0.12, dy=1.12)
export(fig, "K02_colorbar_styles")
