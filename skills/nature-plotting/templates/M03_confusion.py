"""M03 -- Confusion matrix, row-normalised, with counts.
Use when: classifier / assignment performance across K classes.
Nature notes: row-normalise so each row reads as recall; print both % and n; single-hue sequential map;
the diagonal is the story, so keep off-diagonal colours light.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(53)
classes = [f"Class {c}" for c in "ABCDE"]
K = len(classes)
counts = rng.integers(0, 12, (K, K)) + np.diag(rng.integers(70, 120, K))
# -------------------------------------------

frac = counts / counts.sum(axis=1, keepdims=True)
fig, ax = plt.subplots(figsize=figsize_mm(70, 62))
m = heatmap(ax, frac, classes, classes, cmap=NS_BLUES, norm=mpl.colors.Normalize(0, 1), annotate=False)
for i in range(K):
    for j in range(K):
        dark = frac[i, j] > 0.55
        ax.text(j, i - 0.12, f"{100 * frac[i, j]:.0f}%", ha="center", va="center", fontsize=5.5,
                color="w" if dark else "k")
        ax.text(j, i + 0.22, f"n = {counts[i, j]}", ha="center", va="center", fontsize=5,
                color="w" if dark else "0.35")
ax.invert_yaxis()
ax.set_xlabel("Predicted class"); ax.set_ylabel("True class")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")
cbar_side(ax, m, "Fraction of true class", size="4%", ticks=[0, 0.5, 1])
export(fig, "M03_confusion")
