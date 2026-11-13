"""N02 -- ROC (a) and precision-recall (b) curves for several classifiers.
Use when: binary detection / classification performance; PR is the honest view when positives are rare.
Nature notes: AUC in the legend entries; chance level drawn (diagonal for ROC, prevalence for PR); square
panels with equal axis limits.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(62)
n_pos, n_neg = 300, 2700
models = {"Method A": 0.8, "Method B": 1.4, "Method C (ours)": 2.4}
scores = {k: (rng.normal(d, 1, n_pos), rng.normal(0, 1, n_neg)) for k, d in models.items()}
# -------------------------------------------

def roc_pr(pos, neg):
    s = np.r_[pos, neg]; y = np.r_[np.ones(pos.size), np.zeros(neg.size)]
    o = np.argsort(-s); y = y[o]
    tp = np.cumsum(y); fp = np.cumsum(1 - y)
    tpr, fpr = tp / pos.size, fp / neg.size
    prec = tp / (tp + fp)
    return np.r_[0, fpr], np.r_[0, tpr], np.r_[0, tpr], np.r_[1, prec]

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 58), gridspec_kw=dict(wspace=0.35))
cols = ["0.55", PALETTE["blue"], PALETTE["red"]]
for (name, (pos, neg)), c in zip(scores.items(), cols):
    fpr, tpr, rec, prec = roc_pr(pos, neg)
    auc = np.trapezoid(tpr, fpr)                       # area under ROC
    ap = np.sum(np.diff(rec) * prec[1:])               # average precision
    a.plot(fpr, tpr, color=c, lw=1.0, label=f"{name}, AUC {auc:.2f}")
    b.plot(rec, prec, color=c, lw=1.0)
    k = np.argmin(np.abs(rec - 0.5))
    direct_label(b, 0.5, prec[k], f"AP {ap:.2f}", color=c, dy=2.5, va="bottom")
a.plot([0, 1], [0, 1], color="0.7", ls=(0, (3, 2)), lw=0.6)
prev = n_pos / (n_pos + n_neg)
b.axhline(prev, color="0.7", ls=(0, (3, 2)), lw=0.6)
direct_label(b, 0.02, prev, "chance", color="0.5", dy=1.5, va="bottom")
for ax_ in (a, b):
    ax_.set_xlim(0, 1); ax_.set_ylim(0, 1.02); ax_.set_aspect("equal")
a.set_xlabel("False-positive rate"); a.set_ylabel("True-positive rate"); a.legend(loc="lower right", fontsize=5.5)
b.set_xlabel("Recall"); b.set_ylabel("Precision")
for ax_, l in ((a, "a"), (b, "b")):
    style_axes(ax_); panel_label(ax_, l, dx=-0.3)
export(fig, "N02_roc_pr")
