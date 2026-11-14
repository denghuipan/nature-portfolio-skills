"""F06 -- Main figure for a machine-learning paper (10 panels, 183 x 170 mm): architecture, training,
scaling, ROC, PR, confusion, embedding, calibration, results table and ablation.
Use when: the central figure of an ML / AI-for-science paper. Dense but orderly: a four-column row of square-
ish metric panels under the architecture band, then a three-column row, then a table beside an ablation.
Layout: the four- and three-column grids share the outer frame edges (12 and 178.5 mm); inside a row every
frame has the same top and height; letters 10 mm left and 3 mm above every frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
from nature_schematic import *  # noqa: F401,F403  mm-canvas diagram primitives
from nature_layout import Page, columns
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(606)
steps = np.unique(np.round(np.logspace(2, 5, 90)))
off = rng.normal(0, 1, 4)
train = np.array([2.3 * (steps / 100) ** -0.3 + 0.35 + 0.04 * o + rng.normal(0, 0.012, steps.size) for o in off])
val = np.array([2.5 * (steps / 100) ** -0.26 + 0.55 + 0.3 * (steps / 1e5) ** 2 + 0.05 * o
                + rng.normal(0, 0.02, steps.size) for o in off])
sizes = np.array([1e6, 1e7, 1e8, 1e9])
runs = []
for N in sizes:
    D = np.logspace(7, 10.5, 40); runs.append((6 * N * D, 1.7 + 60 / N ** 0.3 + 200 / D ** 0.3))
n_pos, n_neg = 250, 2250
yb = np.r_[np.ones(n_pos), np.zeros(n_neg)]
scores = {"Ours": np.r_[rng.normal(2.1, 1, n_pos), rng.normal(0, 1, n_neg)],
          "Baseline": np.r_[rng.normal(1.2, 1, n_pos), rng.normal(0, 1, n_neg)]}
classes = ["A", "B", "C", "D", "E"]
acc = np.array([0.93, 0.84, 0.76, 0.61, 0.88]); support = np.array([1800, 900, 420, 110, 1300])
M = np.array([np.insert(rng.dirichlet(np.ones(4)) * (1 - a_), i, a_) for i, a_ in enumerate(acc)])
cent = np.array([[0, 0], [3, 1.2], [1.2, 3.4], [-2.6, 2.3], [-1.9, -2.5]])
emb = np.vstack([rng.multivariate_normal(c_, np.eye(2) * 0.33, 300) for c_ in cent]); lab = np.repeat(range(5), 300)
p_pred = rng.beta(2.2, 1.4, 15000); y_cal = rng.random(p_pred.size) < np.clip(p_pred ** 1.15, 0, 1)
table = [["Ours", "310M", "1.2B", "0.874", "0.912"], ["Baseline 1", "350M", "1.2B", "0.811", "0.868"],
         ["Baseline 2", "1.1B", "4.0B", "0.842", "0.889"], ["Baseline 3", "90M", "0.3B", "0.763", "0.802"],
         ["Baseline 4", "650M", "2.5B", "0.829", "0.871"]]
ablation = {"Pretraining": 0.091, "Augmentation": 0.043, "Recycling": 0.027, "Ensembling": 0.012}
# -------------------------------------------
pg = Page(183, 170)
cols3 = columns(12, 178.5, 3, gap=13.5)
cols4 = columns(12, 178.5, 4, gap=12.0)
cO, cB = PALETTE["blue"], "0.55"

# a -- architecture ----------------------------------------------------------------------------------------
a = pg.canvas(0, 1, 183, 28)
icon_stack(a, 8, 8, 10, 12, n=3)
label(a, 14, 5.5, "Inputs", va="top")
blocks = [("Tokenizer", None, "grey", 24, 18), ("Encoder", "× 12", "blue", 50, 20), ("Latent", "dim 512", "purple", 78, 18),
          ("Decoder", "× 12", "blue", 104, 20), ("Heads", "3 tasks", "orange", 132, 18)]
prev = 18.5
for nm, sub_, col, x, w in blocks:
    pbox(a, x, 8, w, 13, nm, sub=sub_, color=col)
    arrow(a, (prev, 14.5), (x, 14.5)); prev = x + w
plus_node(a, 74, 14.5, 1.0)
icon_bars(a, 158, 8, 13, 12, colors=[PASTEL["orange"][1]] * 3 + [cO])
arrow(a, (prev, 14.5), (157, 14.5))
route(a, [(87, 8), (87, 3.5), (60, 3.5), (60, 8)], dashed=True, color=PALETTE["plum"], label_text="Recycling ×3",
      label_side="below", label_color=PALETTE["plum"])
route(a, [(141, 21), (141, 25.5), (33, 25.5), (33, 21)], dashed=True, color="0.4", label_text="Self-supervised pretraining",
      label_side="below")
pg.letter(a, "a")

# row 2 (four columns) ---------------------------------------------------------------------------------------
b, c, d, e = pg.row(38, 29, cols4)
for arr, col, nm in ((train, lighten(cO, 0.45), "Train"), (val, cO, "Validation")):
    for s_ in arr:
        b.plot(steps, s_, color=col, lw=0.3, alpha=0.6)
    b.plot(steps, arr.mean(0), color=col, lw=1.1, label=nm)
b.set_xscale("log"); b.set_xlim(100, 1e5); b.set_ylim(0.4, 2.5)
b.set_xticks([1e2, 1e3, 1e4, 1e5], ["10$^2$", "10$^3$", "10$^4$", "10$^5$"]); b.xaxis.set_minor_locator(mticker.NullLocator())
b.set_xlabel("Step"); b.set_ylabel("Loss"); b.legend(loc="upper right")

sc_cols = n_colors(truncate_cmap(NS_DUSK.reversed(), 0.15, 0.95), len(sizes))
for (C_, L_), col, N in zip(runs, sc_cols, ("1M", "10M", "100M", "1B")):
    c.plot(C_, L_, color=col, lw=0.9, label=N)
c.set_xscale("log"); c.set_yscale("log"); c.set_xlim(3e13, 3e22); c.set_ylim(1.75, 4.4)
c.set_xticks([1e14, 1e17, 1e20]); c.xaxis.set_minor_locator(mticker.NullLocator())
c.set_yticks([2, 3, 4], ["2", "3", "4"]); c.yaxis.set_minor_locator(mticker.NullLocator())
c.set_xlabel("Compute (FLOP)"); c.set_ylabel("Loss")
c.legend(loc="upper right", ncols=2, title="Parameters", columnspacing=0.8, handlelength=1.0)


def curves(s):
    o = np.argsort(-s); ys = yb[o]; tp = np.cumsum(ys); fp = np.cumsum(1 - ys)
    return fp / n_neg, tp / n_pos, tp / (tp + fp)


d.plot([0, 1], [0, 1], color="0.8", lw=0.5); e.axhline(n_pos / (n_pos + n_neg), color="0.8", lw=0.5)
for (nm, s_), col, ls in zip(scores.items(), (cO, cB), ("-", (0, (4, 1.5)))):
    fpr, tpr, prec = curves(s_)
    auc = np.trapezoid(tpr, fpr); ap = np.sum(np.diff(np.r_[0, tpr]) * prec)
    d.plot(fpr, tpr, color=col, ls=ls, lw=1.0, label=f"{nm} {auc:.2f}")
    e.plot(tpr, prec, color=col, ls=ls, lw=1.0, label=f"{nm} {ap:.2f}")
for ax_, xl, yl in ((d, "FPR", "TPR"), (e, "Recall", "Precision")):
    ax_.set_xlim(0, 1); ax_.set_ylim(0, 1.02); ax_.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax_.set_yticks([0.5, 1], ["0.5", "1"])
    ax_.set_xlabel(xl); ax_.set_ylabel(yl)
d.legend(loc="lower right", title="AUC", handlelength=1.4)
e.legend(loc="lower left", title="AP", handlelength=1.4, frameon=True, facecolor="white", edgecolor="none",
         framealpha=0.9, bbox_to_anchor=(0.0, 0.1))

# row 3 (three columns) --------------------------------------------------------------------------------------
f, g, h = pg.row(84, 33, cols3)
f.imshow(M, cmap=NS_BLUES, vmin=0, vmax=1, aspect="auto")
for i in range(5):
    for j in range(5):
        f.text(j, i, f"{100 * M[i, j]:.0f}", ha="center", va="center", color="white" if M[i, j] > 0.55 else "0.15")
f.set_xticks(range(5), classes); f.set_yticks(range(5), classes); f.tick_params(length=0)
f.set_xlabel("Predicted class"); f.set_ylabel("True class")

g.scatter(emb[:, 0], emb[:, 1], s=0.6, c=[EDITORIAL[k] for k in lab], lw=0, rasterized=True)
for k in range(5):
    cx, cy = np.median(emb[lab == k], 0)
    g.text(cx, cy, classes[k], ha="center", va="center",
           bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
g.set_xticks([]); g.set_yticks([]); g.set_xlabel("Dim 1"); g.set_ylabel("Dim 2")
g.set_xlim(-4.4, 4.6); g.set_ylim(-4.2, 5.0)

bins = np.linspace(0, 1, 11); mid = 0.5 * (bins[1:] + bins[:-1])
idx = np.clip(np.digitize(p_pred, bins) - 1, 0, 9)
obs = np.array([y_cal[idx == i].mean() for i in range(10)])
h.plot([0, 1], [0, 1], color="0.7", lw=0.6)
gb = h.bar(mid, obs, width=0.085, color=cO, lw=0)
gradient_patches(h, gb.patches, cO, light=0.8)
h.plot(mid, obs, "o", color="0.1", ms=2.0)
ece = np.sum(np.bincount(idx, minlength=10) * np.abs(obs - mid)) / idx.size
h.set_xlim(0, 1); h.set_ylim(0, 1.02); h.set_xticks([0, 0.5, 1], ["0", "0.5", "1"]); h.set_yticks([0.5, 1], ["0.5", "1"])
h.set_xlabel("Predicted probability"); h.set_ylabel("Observed frequency")
stats_text(h, [f"ECE = {ece:.3f}"], loc="upper left")

# row 4 -------------------------------------------------------------------------------------------------------
tw = cols3[1][0] + cols3[1][1] - cols3[0][0]
it = pg.ax(cols3[0][0] - 10, 131, cols3[2][0] - 22 - (cols3[0][0] - 10), 29, frame=False)
colors_t = [[PALETTE["blue"]] * 3 + [PALETTE["blue"]] * 2] + [["0.1"] * 5] * 4
zebra_table(it, table, ["Model", "Parameters", "Training data", "Score 1", "Score 2"],
            [0.13, 0.36, 0.56, 0.76, 0.93], colors=colors_t)
j = pg.ax(cols3[2][0], 133, cols3[2][1], 27)
names = list(ablation)
gbarh(j, np.arange(4)[::-1], [ablation[k] for k in names], PALETTE["brick"], height=0.6)
for yi, k in zip(np.arange(4)[::-1], names):
    j.text(ablation[k] + 0.003, yi, f"−{ablation[k]:.3f}", va="center")
j.set_yticks(np.arange(4)[::-1], names); j.tick_params(axis="y", length=0)
j.set_xlim(0, 0.13); j.set_ylim(-0.6, 3.6); j.set_xlabel("Drop in score when removed")
j.set_xticks([0, 0.05, 0.1])

pg.letters([b, c, d, e, f, g, h, j], "bcdefghj")
pg.letter(it, "i", dx=0.0, dy=-2.2)
pg.save("F06_machine_learning")
