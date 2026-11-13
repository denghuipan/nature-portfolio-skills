"""M08 -- 3-D surface with its contour projected on the floor.
Use when: the *shape* of a 2-D function is the message (saddle, ridge, valley) and a heat map would hide it.
Prefer a heat map or contour plot when values must be read -- 3-D hides some data behind other data and
Nature reviewers often ask for a 2-D version in Extended Data.
Nature notes: light panes, no grid, muted sequential colour, one viewing angle that shows the feature.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(-3, 3, 80); X, Y = np.meshgrid(x, x)
Z = np.exp(-(X ** 2 + Y ** 2) / 3) * np.cos(1.2 * X) + 0.15 * Y
# -------------------------------------------

fig = plt.figure(figsize=figsize_mm(80, 66))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap=NS_GLACIER.reversed(), rstride=2, cstride=2, linewidth=0.1, edgecolor="0.4",
                antialiased=True, alpha=0.95)
ax.contourf(X, Y, Z, zdir="z", offset=Z.min() - 0.6, cmap=NS_GLACIER.reversed(), levels=12, alpha=0.8)
ax.set_zlim(Z.min() - 0.6, Z.max())
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.set_facecolor((1, 1, 1, 0)); axis.pane.set_edgecolor("0.7")
ax.grid(False)
ax.view_init(elev=24, azim=-55)
ax.set_xlabel("$x$ (unit)", labelpad=-6); ax.set_ylabel("$y$ (unit)", labelpad=-6); ax.set_zlabel("$z$", labelpad=-8)
ax.tick_params(pad=-3, labelsize=5.5)
export(fig, "M08_surface3d")
