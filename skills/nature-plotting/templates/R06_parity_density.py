"""R06 -- Parity plot coloured by point density, with an error histogram inset and summary statistics.
Use when: a model's predictions are checked against reference values for thousands of samples (regression
benchmarks, surrogate models, calibration); the inset shows the error distribution directly.
Look: open axes, square panel, hexagonal density in a sequential map on a log scale, y = x as a thin black
line, +-tolerance band as dashed lines, inset histogram of residuals with zero marked, MAE / R2 / n text.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(43)
ref = rng.gamma(3, 0.7, 20000) - 1.5
pred = ref + rng.standard_t(4, ref.size) * 0.12 + 0.03
tol = 0.25
# -------------------------------------------
res = pred - ref
mae = np.mean(np.abs(res)); r2 = 1 - np.sum(res ** 2) / np.sum((ref - ref.mean()) ** 2)
fig, ax = plt.subplots(figsize=figsize_mm(72, 66))
fig.subplots_adjust(left=0.16, right=0.86, bottom=0.15, top=0.97)
lim = (-1.6, 6)
hb = ax.hexbin(ref, pred, gridsize=70, extent=(*lim, *lim), cmap=NS_SEAFLOOR, bins="log", mincnt=1, lw=0)
ax.plot(lim, lim, color="0.1", lw=0.6)
for s in (-tol, tol):
    ax.plot(lim, np.array(lim) + s, color="0.4", lw=0.5, ls=(0, (3, 2)))
ax.set_xlim(lim); ax.set_ylim(lim); ax.set_aspect("equal")
ax.set_xlabel("Reference value (unit)"); ax.set_ylabel("Predicted value (unit)")
stats_text(ax, [f"MAE = {mae:.3f}", f"$R^2$ = {r2:.3f}", f"n = {ref.size:,}"], loc="upper left")
cb = cbar_side(ax, hb, "Count", size="4%", pad=0.06)
ins = ax.inset_axes([0.6, 0.2, 0.36, 0.22])
ins.hist(res, bins=np.linspace(-1, 1, 41), color=PALETTE["blue"], lw=0)
ins.axvline(0, color="0.1", lw=0.5)
ins.set_xticks([-1, 0, 1]); ins.set_yticks([]); ins.spines["left"].set_visible(False)
ins.set_xlabel("Error", labelpad=1); ins.patch.set_alpha(0)
export(fig, "R06_parity_density")
