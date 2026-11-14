"""N01 -- Training curves: every seed as a thin line, the mean on top, best checkpoint marked.
Use when: loss and a validation metric are reported over training steps for several seeds / runs; showing
all runs is more honest than a single smoothed line.
Look: open axes, log step axis with plain tick labels (1,000 / 10,000 ...), light thin per-seed lines, bold
mean, training vs validation in two tones of one hue, a dot and dashed drop line at the best step.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(101)
steps = np.unique(np.round(np.logspace(2, 5, 120)))
seeds = 5
off = rng.normal(0, 1, seeds)                                          # seed-to-seed offsets
train = np.array([2.4 * (steps / 100) ** -0.32 + 0.35 + 0.05 * o + rng.normal(0, 0.012, steps.size) for o in off])
val = np.array([2.6 * (steps / 100) ** -0.27 + 0.55 + 0.36 * (steps / 1e5) ** 2 + 0.06 * o
                + rng.normal(0, 0.02, steps.size) for o in off])
acc = np.array([0.92 - 0.6 * (steps / 100) ** -0.45 - 0.08 * (steps / 1e5) ** 2 - 0.008 * o
                + rng.normal(0, 0.005, steps.size) for o in off])
# -------------------------------------------
dark, light = PAIRED[0][1], PAIRED[0][0]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 50))
fig.subplots_adjust(left=0.08, right=0.98, bottom=0.22, top=0.92, wspace=0.32)
for arr, c, lab in ((train, light, "Training"), (val, dark, "Validation")):
    for s in arr:
        a.plot(steps, s, color=c, lw=0.35, alpha=0.6)
    a.plot(steps, arr.mean(0), color=c, lw=1.2, label=lab)
for s in acc:
    b.plot(steps, s, color=PALETTE["ochre"], lw=0.35, alpha=0.6)
m = acc.mean(0); k = int(np.argmax(m))
b.plot(steps, m, color=PALETTE["ochre"], lw=1.2)
gradient_fill(b, steps, m, PALETTE["ochre"], alpha=0.3, ymin=0.5)
b.plot(steps[k], m[k], "o", color="0.1", ms=3)
b.plot([steps[k]] * 2, [0.5, m[k]], color="0.3", lw=0.5, ls=(0, (3, 2)))
b.annotate(f"Best: {m[k]:.3f}\nat step {int(steps[k]):,}", (steps[k], 0.52), xytext=(-3, 0),
           textcoords="offset points", ha="right", va="bottom")
for ax in (a, b):
    ax.set_xscale("log"); ax.set_xlim(100, 1e5)
    ax.set_xticks([100, 1000, 10000, 100000], ["100", "1,000", "10,000", "100,000"])
    ax.xaxis.set_minor_locator(mticker.NullLocator())
    ax.set_xlabel("Training step")
a.set_ylabel("Loss"); a.set_ylim(0.4, 2.6); a.legend(loc="upper right")
b.set_ylabel("Validation accuracy"); b.set_ylim(0.5, 0.95)
b.text(0.02, 0.98, f"{seeds} seeds (thin); mean (bold)", transform=b.transAxes, va="top", color="0.4")
panel_label(a, "a", dx=-0.2, dy=1.08); panel_label(b, "b", dx=-0.2, dy=1.08)
export(fig, "N01_training_curves")
