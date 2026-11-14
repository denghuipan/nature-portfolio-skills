"""M02 -- Clustered heat map with a column dendrogram, a row-group colour strip and a short colour bar.
Use when: samples x features (or items x conditions) are z-scored and ordered by hierarchical clustering;
known row groups are shown as a strip so readers can see whether the clustering recovers them.
Look: no cell borders, diverging map centred at 0, thin dendrogram above, categorical strip at the left with
a small key, colour bar placed top-right, sample labels only when there are few columns.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(67)
n_rows, n_cols = 36, 16
row_group = np.repeat([0, 1, 2], [14, 12, 10])
Z = rng.normal(0, 0.6, (n_rows, n_cols))
Z[row_group == 0, :6] += 1.4; Z[row_group == 1, 6:11] += 1.5; Z[row_group == 2, 11:] += 1.3
Z[row_group == 0, 11:] -= 1.0
Z = (Z - Z.mean(1, keepdims=True)) / Z.std(1, keepdims=True)
samples = [f"S{i}" for i in range(1, n_cols + 1)]
gnames = ["Type 1", "Type 2", "Type 3"]
# -------------------------------------------
gcols = [PALETTE["ochre"], PALETTE["teal"], PALETTE["plum"]]
col_link = linkage(Z.T, "average", metric="correlation")
row_order = leaves_list(linkage(Z, "average", metric="correlation"))
fig = plt.figure(figsize=figsize_mm(89, 86))
dn_ax = fig.add_axes([0.16, 0.8, 0.66, 0.1])
strip = fig.add_axes([0.125, 0.12, 0.025, 0.67])
hm = fig.add_axes([0.16, 0.12, 0.66, 0.67])
d = dendrogram(col_link, ax=dn_ax, color_threshold=0, above_threshold_color="0.3", no_labels=True)
for coll in dn_ax.collections:
    coll.set_linewidth(0.5)
dn_ax.axis("off")
col_order = d["leaves"]
im = hm.imshow(Z[row_order][:, col_order], aspect="auto", cmap=NS_DIV_BR, vmin=-2.5, vmax=2.5, interpolation="nearest")
hm.set_xticks(range(n_cols), [samples[i] for i in col_order], rotation=90)
hm.set_yticks([]); hm.tick_params(axis="x", length=0)
for s in hm.spines.values():
    s.set_visible(False)
strip.imshow(row_group[row_order][:, None], aspect="auto", cmap=mcolors.ListedColormap(gcols),
             interpolation="nearest")
strip.axis("off")
strip.text(-0.6, 0.5, "Features", transform=strip.transAxes, rotation=90, ha="right", va="center", fontsize=7)
cax = fig.add_axes([0.85, 0.83, 0.12, 0.022])
cb = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=[-2, 0, 2]); style_cbar(cb)
cax.set_title("z-score", fontsize=6, pad=2)
key = fig.add_axes([0.84, 0.45, 0.15, 0.3]); key.axis("off")
square_legend(key, gnames, gcols, loc="upper left", title="Row group", title_fontsize=6)
export(fig, "M02_cluster_heatmap")
