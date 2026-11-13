"""M09 -- Clustered heat map with dendrograms (rows and columns re-ordered by similarity).
Use when: many samples x many features where groups should emerge (expression, spectra features, sensors).
Nature notes: z-score per row with a centred diverging map; thin dendrogram lines; say the linkage and the
distance in the legend or caption.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(59)
n_r, n_c = 24, 14
base = rng.normal(0, 1, (n_r, n_c))
base[:8, :5] += 2.0; base[8:16, 5:10] += 2.0; base[16:, 10:] -= 1.8
rows = [f"F{i}" for i in range(1, n_r + 1)]; cols = [f"S{j}" for j in range(1, n_c + 1)]
# -------------------------------------------

from scipy.cluster.hierarchy import linkage, dendrogram
Zs = (base - base.mean(1, keepdims=True)) / base.std(1, keepdims=True)
lr = linkage(Zs, "average", metric="correlation"); lc = linkage(Zs.T, "average", metric="correlation")
fig = plt.figure(figsize=figsize_mm(89, 90))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 5], height_ratios=[1, 5], wspace=0.02, hspace=0.02,
                      left=0.06, right=0.84, bottom=0.08, top=0.97)
axr = fig.add_subplot(gs[1, 0]); axc = fig.add_subplot(gs[0, 1]); ax = fig.add_subplot(gs[1, 1])
with mpl.rc_context({"lines.linewidth": 0.5}):
    dr = dendrogram(lr, orientation="left", ax=axr, color_threshold=0, above_threshold_color="0.3", no_labels=True)
    dc = dendrogram(lc, ax=axc, color_threshold=0, above_threshold_color="0.3", no_labels=True)
for a_ in (axr, axc):
    a_.axis("off")
ro, co = dr["leaves"], dc["leaves"]
m = heatmap(ax, Zs[ro][:, co], [cols[i] for i in co], [rows[i] for i in ro], cmap=NS_DIV_BR,
            norm=center_norm(-2.5, 0, 2.5), grid_lw=0.3)
ax.invert_yaxis(); ax.yaxis.tick_right()
ax.tick_params(labelsize=5); plt.setp(ax.get_xticklabels(), rotation=90)
cax = fig.add_axes([0.93, 0.55, 0.02, 0.25])
cb = fig.colorbar(m, cax=cax, ticks=[-2, 0, 2]); style_cbar(cb, "Row z-score")
export(fig, "M09_cluster_heatmap")
