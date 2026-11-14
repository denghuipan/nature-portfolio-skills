"""N02 -- ROC and precision-recall curves with operating points and areas in the key.
Use when: binary classifiers / detectors are compared; ROC for ranking quality, PR because the positive class
is rare. The chosen threshold of each model is marked on both.
Look: two square open panels, chance as a thin grey line, method of interest in the strong hue, baselines
in greys with different dash patterns, AUC / AP written in the key, filled dot = operating point.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(103)
n_pos, n_neg = 300, 2700
y = np.r_[np.ones(n_pos), np.zeros(n_neg)]
scores = {"Method A": np.r_[rng.normal(2.2, 1, n_pos), rng.normal(0, 1, n_neg)],
          "Method B": np.r_[rng.normal(1.5, 1, n_pos), rng.normal(0, 1, n_neg)],
          "Method C": np.r_[rng.normal(0.9, 1, n_pos), rng.normal(0, 1, n_neg)]}
thr = 1.5
# -------------------------------------------


def curves(s):
    o = np.argsort(-s); ys = y[o]; tp = np.cumsum(ys); fp = np.cumsum(1 - ys)
    tpr = tp / n_pos; fpr = fp / n_neg; prec = tp / (tp + fp)
    return fpr, tpr, prec, np.trapezoid(tpr, fpr), np.sum(np.diff(np.r_[0, tpr]) * prec)


cols = [PALETTE["blue"], "0.35", "0.6"]; dashes = ["-", (0, (4, 1.5)), (0, (1.5, 1.2))]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(110, 56))
fig.subplots_adjust(left=0.1, right=0.98, bottom=0.18, top=0.95, wspace=0.38)
a.plot([0, 1], [0, 1], color="0.8", lw=0.5)
b.axhline(n_pos / (n_pos + n_neg), color="0.8", lw=0.5)
for (nm, s), c, ls in zip(scores.items(), cols, dashes):
    fpr, tpr, prec, auc, ap = curves(s)
    a.plot(fpr, tpr, color=c, ls=ls, lw=1.0, label=f"{nm} ({auc:.2f})")
    b.plot(tpr, prec, color=c, ls=ls, lw=1.0, label=f"{nm} ({ap:.2f})")
    pos = (s >= thr)
    tp = np.sum(pos & (y == 1)); fp = np.sum(pos & (y == 0))
    a.plot(fp / n_neg, tp / n_pos, "o", color=c, ms=3)
    b.plot(tp / n_pos, tp / max(tp + fp, 1), "o", color=c, ms=3)
for ax in (a, b):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.01); ax.set_aspect("equal")
    ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
a.set_xlabel("False-positive rate"); a.set_ylabel("True-positive rate")
b.set_xlabel("Recall"); b.set_ylabel("Precision")
a.legend(loc="lower right", title="AUC", title_fontsize=6, handlelength=1.8)
b.legend(loc="lower left", bbox_to_anchor=(0.0, 0.13), title="AP", title_fontsize=6, handlelength=1.8,
         frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)
b.text(0.98, n_pos / (n_pos + n_neg) + 0.02, "Chance", fontsize=6, color="0.55", ha="right")
panel_label(a, "a", dx=-0.3, dy=1.06); panel_label(b, "b", dx=-0.3, dy=1.06)
export(fig, "N02_roc_pr")
