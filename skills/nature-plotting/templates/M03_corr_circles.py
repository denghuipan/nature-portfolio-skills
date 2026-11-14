"""M03 -- Correlation matrix: circles below the diagonal (size and colour = r), numbers above it.
Use when: 6-15 variables are correlated pairwise; circles give the pattern at a glance, the upper triangle
gives exact values, the diagonal carries the variable names.
Look: no frame, faint cell grid, diverging map with the neutral colour at 0, names on the diagonal,
significance marked by bold numbers, slim colour bar.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(71)
names = [f"Var {i}" for i in range(1, 9)]
L = rng.normal(0, 1, (8, 3))
C = L @ L.T + np.diag(rng.uniform(0.5, 1.5, 8))
d = np.sqrt(np.diag(C)); R = C / np.outer(d, d)
n_obs = 60
# -------------------------------------------
k = len(names)
fig, ax = plt.subplots(figsize=figsize_mm(80, 72))
fig.subplots_adjust(left=0.03, right=0.84, bottom=0.03, top=0.97)
norm = mcolors.Normalize(-1, 1)
for i in range(k):
    for j in range(k):
        ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec="0.92", lw=0.4))
        if i > j:
            ax.add_patch(plt.Circle((j, i), 0.46 * np.sqrt(abs(R[i, j])), color=NS_DIV_BR(norm(R[i, j])), lw=0))
        elif i < j:
            sig = abs(R[i, j]) * np.sqrt((n_obs - 2) / (1 - R[i, j] ** 2)) > 2.0
            ax.text(j, i, f"{R[i, j]:.2f}".replace("-", "−"), ha="center", va="center",
                    color=darken(NS_DIV_BR(norm(R[i, j])), 0.2) if sig else "0.55",
                    fontweight="bold" if sig else "normal")
        else:
            ax.text(j, i, names[i], ha="center", va="center")
ax.set_xlim(-0.5, k - 0.5); ax.set_ylim(k - 0.5, -0.5); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([]); no_background(ax)
sm = mpl.cm.ScalarMappable(norm=norm, cmap=NS_DIV_BR)
cax = fig.add_axes([0.87, 0.25, 0.025, 0.5])
cb = fig.colorbar(sm, cax=cax, ticks=[-1, -0.5, 0, 0.5, 1]); style_cbar(cb, "Pearson $r$")
ax.text(k - 0.5, k - 0.3, f"Bold: P < 0.05 (n = {n_obs})", ha="right", va="top", color="0.4")
export(fig, "M03_corr_circles")
