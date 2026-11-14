"""M04 -- Confusion matrix (row-normalised) with the class support as bars at the right.
Use when: a classifier is evaluated on imbalanced classes; percentages in the cells, the number of true
items per class beside the rows so a 90% on 12 items is not over-read.
Look: square cells without borders, single-hue sequential map, white text on dark cells, recall on the
diagonal, horizontal support bars sharing the rows, thousands separators.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(73)
classes = ["Class A", "Class B", "Class C", "Class D", "Class E"]
support = np.array([2140, 860, 410, 95, 1320])
acc = np.array([0.93, 0.81, 0.72, 0.58, 0.88])
M = np.zeros((5, 5))
for i in range(5):
    off = rng.dirichlet(np.ones(4)) * (1 - acc[i])
    M[i] = np.insert(off, i, acc[i]) * support[i]
M = np.round(M)
# -------------------------------------------
P = M / M.sum(1, keepdims=True)
fig = plt.figure(figsize=figsize_mm(96, 66))
ax = fig.add_axes([0.2, 0.2, 0.5, 0.72]); bx = fig.add_axes([0.72, 0.2, 0.2, 0.72], sharey=ax)
ax.imshow(P, cmap=NS_BLUES, vmin=0, vmax=1)
for i in range(5):
    for j in range(5):
        ax.text(j, i, f"{100 * P[i, j]:.0f}", ha="center", va="center", fontsize=6,
                color="white" if P[i, j] > 0.55 else "0.15")
ax.set_xticks(range(5), classes, rotation=45, ha="right"); ax.set_yticks(range(5), classes)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xlabel("Predicted class"); ax.set_ylabel("True class")
ax.set_title("Row-normalised (%)", fontsize=6, color="0.35", pad=3)
bx.barh(range(5), support, color=PALETTE["lightgrey"], height=0.6, lw=0)
for i, v in enumerate(support):
    bx.text(v + 40, i, f"{v:,}", va="center", fontsize=6)
bx.set_xlim(0, support.max() * 1.6); bx.set_xticks([]); despine(bx, left=True, bottom=True)
bx.tick_params(labelleft=False)
bx.set_title("Support (n)", fontsize=6, color="0.35", pad=3)
export(fig, "M04_confusion_support")
