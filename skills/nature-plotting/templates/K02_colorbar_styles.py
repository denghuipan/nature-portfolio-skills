"""K02 -- Six colour-bar layouts and when to use each.
a  slim bar glued to the right of a map (default)
b  short horizontal bar inside the panel, label above (saves a column)
c  bar under the panel (scatter coloured by a third variable)
d  binned bar for a quantity with meaningful classes
e  categorical key for a labelled map (ticks centred on blocks)
f  diverging map centred on 0 with extend arrows for clipped values; a log bar
Look: hair-line outline, short outward ticks, the quantity and unit always in the label.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(137)
x = np.linspace(-3, 3, 160); X, Y = np.meshgrid(x, x)
Z = np.exp(-((X - 0.6) ** 2 + (Y - 0.3) ** 2) / 1.6) + 0.5 * np.exp(-((X + 1.2) ** 2 + (Y + 1.0) ** 2) / 0.7)
D = np.sin(X) * np.cos(Y) * 1.3
cat = (np.hypot(X, Y) > 1.0).astype(int) + (X > 1.2) + (Y < -1.4)
px, py = rng.uniform(0, 1, 140), rng.uniform(0, 1, 140); pz = 10 ** (px * 3)
# -------------------------------------------
fig, axs = plt.subplots(2, 3, figsize=figsize_2col(112))
fig.subplots_adjust(left=0.04, right=0.94, top=0.95, bottom=0.12, wspace=0.42, hspace=0.42)
a, b, c, d, e, f = axs.ravel()
for ax in (a, b, d, e, f):
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(False)
im = a.imshow(Z, cmap=NS_SEAFLOOR, origin="lower"); cbar_side(a, im, "Intensity (norm.)", ticks=[0, 0.5, 1])
im = b.imshow(Z, cmap=NS_PURPLES, origin="lower")
cbar_inset(b, im, "Density (a.u.)", loc="upper right", width="38%", height="4%", ticks=[0, 0.5, 1])
sc = c.scatter(px, py, c=pz, s=6, cmap=NS_DUSK, norm=mcolors.LogNorm(1, 1000), lw=0)
c.set_xlabel("Variable $x$"); c.set_ylabel("Variable $y$")
cbar_below(c, sc, "Third variable (unit)", pad=0.32)
norm_b, cm_b, cb = cbar_discrete(d, NS_SUNSET, bounds=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], label="Level (unit)")
d.imshow(Z, cmap=cm_b, norm=norm_b, origin="lower")
norm_c, cm_c, cb = cbar_discrete(e, mcolors.ListedColormap([PALETTE["sky"], PALETTE["sage"], PALETTE["ochre"],
                                                            PALETTE["plum"]]),
                                 categories=["Class 1", "Class 2", "Class 3", "Class 4"])
e.imshow(cat, cmap=cm_c, norm=norm_c, origin="lower")
im = f.imshow(D, cmap=NS_DIV_BR, origin="lower", norm=center_norm(-1, 0, 1))
cbar_side(f, im, "Change (unit)", extend="both", ticks=[-1, 0, 1])
for ax, l in zip(axs.ravel(), "abcdef"):
    panel_label(ax, l, dx=-0.08 if l != "c" else -0.3, dy=1.1)
export(fig, "K02_colorbar_styles")
