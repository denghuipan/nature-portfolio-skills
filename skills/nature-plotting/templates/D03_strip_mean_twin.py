"""D03 -- Ordered steps: strip plot with mean +- s.d. and n per step, plus a second metric on a twin axis.
Use when: an ordered pipeline (step 1 -> step 4) improves one metric while a second metric tracks it.
Nature notes: the step order is the x axis; n and mean written above each strip; the twin-axis metric,
its spine, ticks and label share one colour.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(33)
steps = ["Step 1", "Step 2", "Step 3", "Step 4"]
vals = [np.clip(rng.beta(0.5, 5, 600), 0, 1), np.clip(rng.beta(1.6, 1.3, 600), 0, 1),
        np.clip(1 - rng.gamma(0.7, 0.04, 30), 0, 1), np.clip(1 - rng.gamma(0.5, 0.01, 30), 0, 1)]
m2 = np.array([0.14, 0.40, 0.62, 0.74])
m2_lo, m2_hi = m2 - [0.10, 0.12, 0.13, 0.10], m2 + [0.10, 0.12, 0.10, 0.08]
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(89, 58))
x = np.arange(len(steps))
for xi, v in zip(x, vals):
    jitter(ax, xi, v, "0.35", width=0.16, size=2.5 if v.size > 100 else 5, alpha=0.35)
    m, lo, hi = mean_sd(ax, xi, v, color="k", capw=0.22)
    ax.text(xi, 1.12, f"{m:.3f}\nn = {v.size}", ha="center", va="bottom", fontsize=5.5, color="0.2")
ax.set_ylim(0, 1.35); ax.set_yticks([0, 0.5, 1.0]); ax.set_ylabel("Metric 1")
ax.set_xticks(x, steps); ax.set_xlim(-0.5, len(steps) - 0.2)
blue = PALETTE["blue"]
ax2 = ax.twinx()
ci_band(ax2, x + 0.25, m2_lo, m2_hi, blue, alpha=0.15)
ax2.plot(x + 0.25, m2, "-D", color=blue, ms=3, lw=1.0)
for xi, c in zip(x, m2):
    direct_label(ax2, xi + 0.25, c, f"{c:.2f}", color=blue, dx=3, dy=-3, ha="left", va="top")
ax2.set_ylim(0, 1.35); ax2.set_yticks([0, 0.5, 1.0]); ax2.set_ylabel("Metric 2", color=blue)
ax2.tick_params(axis="y", which="both", colors=blue, direction="in"); ax2.spines["right"].set_color(blue)
ax.tick_params(axis="y", which="both", right=False)
ax.tick_params(axis="x", which="both", bottom=False, top=False)
export(fig, "D03_strip_mean_twin")
