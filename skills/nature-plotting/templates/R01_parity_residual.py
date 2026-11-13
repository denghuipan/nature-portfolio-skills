"""R01 -- Parity plot (predicted vs true) with density colouring, and the residuals underneath.
Use when: validating a model / instrument against ground truth over a range.
Nature notes: identity line dashed; +-tolerance band light grey; MAE / RMSE / R^2 / n in the corner;
residual panel shares x and shows the bias trend the parity plot hides.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(41)
y_true = rng.uniform(0, 10, 1500)
y_pred = y_true + rng.normal(0, 0.15 + 0.03 * y_true, y_true.size) + 0.02 * (y_true - 5)
tol = 0.5
# -------------------------------------------

fig = plt.figure(figsize=figsize_mm(62, 78))
gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1], hspace=0.08)
a = fig.add_subplot(gs[0]); r = fig.add_subplot(gs[1], sharex=a)
sc = parity(a, y_true, y_pred, tol=tol, density=True, s=3, units="", cmap=truncate_cmap(NS_GLACIER, 0.0, 0.85))
a.set_ylabel("Predicted (unit)"); a.tick_params(labelbottom=False)
res = y_pred - y_true
r.scatter(y_true, res, s=2, color=mcolors.to_rgba(PALETTE["blue"], 0.25), lw=0)
r.axhline(0, color="0.25", ls=(0, (3, 2)), lw=0.7)
r.fill_between([-1, 11], -tol, tol, color="0.88", lw=0, zorder=0)
bins = np.linspace(0, 10, 11); idx = np.digitize(y_true, bins)
mu = [res[idx == i].mean() for i in range(1, len(bins))]
r.plot((bins[:-1] + bins[1:]) / 2, mu, "-o", color="k", ms=2.4, lw=0.8)
r.set_ylim(-1.6, 1.6); r.set_ylabel("Residual"); r.set_xlabel("True value (unit)")
a.set_aspect("auto")
for ax_ in (a, r):
    style_axes(ax_)
export(fig, "R01_parity_residual")
