"""S03 -- Structure concept: isometric view of a patterned layer stack (a), cross-section with dimensions (b),
top-view image of the patterned area with a scale bar (c).
Use when: introducing a fabricated or engineered structure; keeps geometry, layer names and dimensions together.
Nature notes: one colour per material, identical in all views; dimension lines thin and grey; leader lines
for labels instead of a legend.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

W, H = 183, 64
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
MAT = {"Substrate": "#9AA3AD", "Layer": "#CFE3F3", "Feature": "#E84143"}

# (a) isometric stack with an array of features
ox, oy = 10, 12
iso_block(ax, 0, 0, 0, 36, 30, 5, color=MAT["Substrate"], ox=ox, oy=oy)
iso_block(ax, 0, 0, 5, 36, 30, 3, color=MAT["Layer"], ox=ox, oy=oy)
for i in range(3)[::-1]:
    for j in range(3):
        iso_block(ax, 6 + 10 * i, 5 + 9 * j, 8, 4, 4, 4, color=MAT["Feature"], ox=ox, oy=oy)
for name, (px, py, pz), (tx, ty) in [("Substrate", (36, 4, 2), (60, 8)), ("Layer", (36, 26, 6.5), (62, 30)),
                                     ("Feature", (16, 23, 12), (30, 54))]:
    callout(ax, iso(px, py, pz, ox, oy), (tx, ty), name, color="0.2")
label(ax, 2, 62, "a", ha="left", va="top", size=8 / 6, fontweight="bold")

# (b) cross-section with dimensions
top, _ = layer_stack(ax, 84, 14, 40, [dict(name="Substrate", h=10, color=MAT["Substrate"]),
                                      dict(name="Layer", h=6, color=MAT["Layer"])], label_x=126)
for xf in (92, 108):
    ax.add_patch(mpl.patches.Rectangle((xf, top), 6, 7, fc=MAT["Feature"], ec="0.3", lw=0.4))
dimension(ax, (92, top + 7), (98, top + 7), "$w$", offset=2.0)
dimension(ax, (92, top), (92, top + 7), "$h$", offset=2.0)
dimension(ax, (92, top - 1.5), (108, top - 1.5), "$p$", offset=-3.0)
ax.text(126, top + 3.5, "Feature", ha="left", va="center", fontsize=6)
label(ax, 78, 62, "b", ha="left", va="top", size=8 / 6, fontweight="bold")

# (c) top-view image
reg = region_topview(ax, 146, 18, L=32, W=32, image=periodic_field(kx=4, ky=4), cmap=NS_EMBER)
ax.plot([reg.x + 20, reg.x + 30], [reg.y - 5] * 2, color="k", lw=1.2, solid_capstyle="butt")
label(ax, reg.x + 25, reg.y - 6, "1 µm", va="top")
label(ax, 140, 62, "c", ha="left", va="top", size=8 / 6, fontweight="bold")
export(fig, "S03_device_concept", exact=True)
