"""N01 -- Learning curves: training / validation loss over epochs (mean +- s.d. over seeds) and a metric.
Use when: reporting how a model was trained (Methods, Extended Data) and where it was stopped.
Nature notes: log loss axis; band = spread over seeds (say how many); the selected epoch marked once and
referenced in the caption; validation drawn darker than training.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(61)
ep = np.arange(1, 201)
seeds = 5
train = np.array([0.8 * ep ** -0.55 * np.exp(rng.normal(0, 0.03, ep.size)) for _ in range(seeds)])
val = np.array([0.9 * ep ** -0.45 + 2e-4 * (ep - 90).clip(0) + rng.normal(0, 0.004, ep.size) for _ in range(seeds)])
metric = np.array([1 - 0.5 * ep ** -0.6 - 8e-5 * (ep - 90).clip(0) + rng.normal(0, 0.004, ep.size) for _ in range(seeds)])
# -------------------------------------------

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_2col(52), gridspec_kw=dict(wspace=0.3))
for arr, c, name in [(train, PALETTE["lightblue"], "Training"), (val, PALETTE["blue"], "Validation")]:
    m, s = arr.mean(0), arr.std(0)
    ci_band(a, ep, m - s, m + s, c, alpha=0.25)
    a.plot(ep, m, color=c, lw=1.0, label=name)
best = int(ep[np.argmin(val.mean(0))])
ref_line(a, best, "x", f"selected: epoch {best}", side="left", pos=0.30, color="0.4")
a.set_yscale("log"); log_ticks(a.yaxis); a.set_xlim(0, 200)
a.set_xlabel("Epoch"); a.set_ylabel("Loss"); a.legend(loc="upper right")
m, s = metric.mean(0), metric.std(0)
ci_band(b, ep, m - s, m + s, PALETTE["red"], alpha=0.2)
b.plot(ep, m, color=PALETTE["red"], lw=1.0)
b.plot(best, m[best - 1], "o", ms=3.5, mfc="w", mec=PALETTE["red"], mew=0.9, zorder=4)
b.set_xlim(0, 200); b.set_ylim(0.7, 1.0); b.set_xlabel("Epoch"); b.set_ylabel("Validation score")
stats_text(b, [f"mean ± s.d., {seeds} seeds"], loc="lower right")
for ax_, l in ((a, "a"), (b, "b")):
    style_axes(ax_); panel_label(ax_, l, dx=-0.2)
export(fig, "N01_training_curves")
