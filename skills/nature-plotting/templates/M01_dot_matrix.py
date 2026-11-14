"""M01 -- Dot matrix: features x groups, dot size = fraction of items with the feature, colour = mean level.
Use when: a marker / feature panel is summarised across groups (cell types, sites, conditions); two
quantities per cell are needed, which a plain heat map cannot show.
Look: no frame, light row/column guides, sequential colour with a slim colour bar, a size key with three
reference dots, group names rotated at the bottom, block brackets for feature sets on top.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(61)
groups = [f"Group {i}" for i in range(1, 9)]
features = [f"Feature {i}" for i in range(1, 15)]
frac = rng.beta(1.2, 3, (len(groups), len(features)))
mean = rng.uniform(0, 0.6, frac.shape)
for g in range(len(groups)):                          # each group has a block of characteristic features
    cols_ = slice(min(13, g * 2 - 1 if g else 0), min(14, g * 2 + 2))
    frac[g, cols_] = rng.uniform(0.6, 0.95, frac[g, cols_].shape)
    mean[g, cols_] = rng.uniform(0.7, 1.0, mean[g, cols_].shape)
blocks = [(0, 4, "Set A"), (5, 9, "Set B"), (10, 13, "Set C")]
# -------------------------------------------
fig, ax = plt.subplots(figsize=figsize_mm(100, 66))
fig.subplots_adjust(left=0.13, right=0.8, bottom=0.18, top=0.86)
for i in range(len(groups)):
    ax.axhline(i, color="0.93", lw=0.5, zorder=0)
sc = dot_matrix(ax, frac, mean, features, groups, cmap=NS_PURPLES, smax=42, vmin=0, vmax=1, rotate=90, edge="none")
ax.xaxis.tick_top(); ax.tick_params(axis="x", labeltop=False, labelbottom=True, rotation=90)
for a, b, nm in blocks:
    ax.plot([a - 0.3, b + 0.3], [-0.9, -0.9], color="0.2", lw=0.6, clip_on=False)
    ax.text((a + b) / 2, -1.1, nm, ha="center", va="bottom")
cax = fig.add_axes([0.85, 0.5, 0.025, 0.3])
cb = fig.colorbar(sc, cax=cax, ticks=[0, 0.5, 1]); style_cbar(cb, "Mean level")
key = fig.add_axes([0.83, 0.12, 0.15, 0.3]); key.axis("off")
size_legend(key, [0.25, 0.5, 1.0], [42 * v for v in (0.25, 0.5, 1.0)], title="Fraction", fmt="{:.0%}",
            loc="upper left", color="0.45", edge="none")
export(fig, "M01_dot_matrix")
