"""R05 -- Two-dimensional embedding (UMAP / t-SNE / PCA): clusters labelled in place, and one variable overlaid.
Use when: thousands of items are embedded in 2-D and readers should see cluster identity (left) and how a
continuous property varies across the map (right).
Look: no axes, a small L-shaped arrow key 'Dim 1 / Dim 2' in the corner, cluster names at the cluster
centres (no legend), small rasterised points, right panel coloured by a sequential map with an inset bar.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(37)
centres = np.array([[0, 0], [3.2, 1.0], [1.4, 3.4], [-2.6, 2.6], [-2.0, -2.6], [2.4, -2.4], [5.2, 3.6]])
sizes = [900, 700, 500, 650, 420, 380, 160]
pts, lab = [], []
for k, (c, nk) in enumerate(zip(centres, sizes)):
    cov = np.diag(rng.uniform(0.25, 0.6, 2)); cov[0, 1] = cov[1, 0] = rng.uniform(-0.15, 0.15)
    pts.append(rng.multivariate_normal(c, cov, nk)); lab += [k] * nk
P = np.vstack(pts); lab = np.array(lab)
score = np.tanh(0.45 * P[:, 0] + 0.25 * P[:, 1]) + rng.normal(0, 0.15, len(P))
names = [f"Cluster {i + 1}" for i in range(len(centres))]
# -------------------------------------------
cols = EDITORIAL[:7]
fig, axs = plt.subplots(1, 2, figsize=figsize_mm(140, 64))
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.08, top=0.93, wspace=0.1)
for ax in axs:                      # framed, no ticks: embedding coordinates carry no units
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("Dim 1"); ax.set_ylabel("Dim 2")
    ax.set_xlim(-4.2, 7.2); ax.set_ylim(-4.6, 5.6)
a, b = axs
a.scatter(P[:, 0], P[:, 1], s=1.2, c=[cols[k] for k in lab], lw=0, rasterized=True)
for k, nm in enumerate(names):
    cx, cy = np.median(P[lab == k], 0)
    a.text(cx, cy, nm, ha="center", va="center", color="0.05",
           bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
sc = b.scatter(P[:, 0], P[:, 1], s=1.2, c=score, cmap=NS_DUSK.reversed(), vmin=-1, vmax=1, lw=0, rasterized=True)
cbar_inset(b, sc, "Score", loc="lower right", width="26%", height="3%", ticks=[-1, 0, 1], borderpad=1.0)
panel_label(a, "a", dx=-0.07, dy=1.07); panel_label(b, "b", dx=-0.07, dy=1.07)
export(fig, "R05_embedding_clusters")
