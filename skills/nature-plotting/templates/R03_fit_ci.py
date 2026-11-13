"""R03 -- Data with error bars, a least-squares fit with its 95 % confidence band, the law written along the
line, and a second y axis in other units.
Use when: a calibration or scaling law is the claim (power law, exponential decay, linear response).
Nature notes: the fit is a thin dashed line, the band light; the equation follows the slope of the line;
when both axes are shown, the secondary axis is a pure unit conversion, never a second data set.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(43)
x = np.array([0.5, 1, 2, 3.2, 5, 7, 9.5])
y = -2.0 * x + 1.5 + rng.normal(0, 0.6, x.size)          # y in dB-like log units
yerr = rng.uniform(0.3, 0.9, x.size)
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(70, 58))
cols = n_colors(truncate_cmap(NS_EMBER, 0.15, 0.85), x.size)
for xi, yi, ei, ci in zip(x, y, yerr, cols):
    ax.errorbar(xi, yi, yerr=ei, fmt="o", color=ci, mec="0.2", mew=0.4, ms=3.5, elinewidth=0.8, capsize=0)
a0, b0 = fit_line(ax, x, y, kind="linear", xfit=np.linspace(-0.5, 10.5, 200), color="0.35",
                  label_fmt="slope = {b:.2f} per unit", label_pos=0.78, label_offset=5)
ax.set_xlim(-0.5, 10.5); ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Response (dB)")
secondary_unit_axis(ax, "y", (lambda d: 10 ** (d / 10), lambda v: 10 * np.log10(np.clip(v, 1e-12, None))),
                    label="Response (linear)", ticks=[0.01, 0.1, 1], ticklabels=["0.01", "0.1", "1"])
style_axes(ax); ax.tick_params(axis="y", which="both", right=False)
export(fig, "R03_fit_ci")
