"""M05 -- 2-D map with an extend-triangle colour bar, region labels, and a log-scaled companion map.
Use when: a quantity over two continuous axes (x, y), e.g. response vs position and frequency.
Nature notes: 'extend' triangles show the colour range was clipped; region tags sit in small filled boxes on
the map; a perceptually uniform map (house EMBER, or magma / inferno); a log norm for power-like data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(0, 100, 300); y = np.linspace(0, 30, 90)
X, Y = np.meshgrid(x, y)
Z1 = (0.55 + 0.45 * np.cos(2 * np.pi * Y / (4 + 0.03 * X)) * np.exp(-((Y - 15) / 12) ** 2)) * (1 + 0.3 * (X > 50))
Z2 = np.exp(-((Y - 6 - 0.08 * X) / (3 + 0.03 * X)) ** 2) + 1e-3
# -------------------------------------------

fig, (a, b) = plt.subplots(2, 1, figsize=figsize_mm(89, 66), sharex=True, gridspec_kw=dict(height_ratios=[1.4, 1], hspace=0.22))
m1 = a.pcolormesh(X, Y, Z1, cmap=NS_EMBER, vmin=0, vmax=1.0, shading="auto", rasterized=True)
a.axvline(50, color="w", ls=":", lw=0.7)
for txt, xx, ha, col in [("Region A", 2, "left", PALETTE["blue"]), ("Region B", 98, "right", PALETTE["red"])]:
    a.text(xx, 2, txt, ha=ha, va="bottom", fontsize=5.5, color="w",
           bbox=dict(boxstyle="square,pad=0.25", fc=col, ec="none", alpha=0.85))
a.set_ylabel("$y$ (unit)")
cbar_side(a, m1, "$Z_1$ (norm.)", extend="max", ticks=[0, 0.5, 1.0])
m2 = b.pcolormesh(X, Y, Z2, cmap="magma", norm=mpl.colors.LogNorm(1e-3, 1), shading="auto", rasterized=True)
b.set_ylabel("$y$ (unit)"); b.set_xlabel("$x$ (unit)"); a.tick_params(labelbottom=False)
cb2 = cbar_side(b, m2, "$Z_2$", ticks=[1e-3, 1e-2, 1e-1, 1])
for ax_ in (a, b):
    ax_.tick_params(which="both", colors="k")
    style_axes(ax_)
export(fig, "M05_map_extend")
