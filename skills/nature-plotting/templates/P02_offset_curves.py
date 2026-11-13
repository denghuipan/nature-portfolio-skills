"""P02 -- Offset (stacked) curves ordered by a parameter, with shared feature markers.
Use when: a sequence of curves (profiles, traces, spectra) whose common features should line up.
Nature notes: order by the parameter; colour from an ordered map that also colours the labels; feature
markers as thin dotted verticals with names above the frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(0, 100, 900)
rng = np.random.default_rng(8)
features = {"F1": 18.0, "F2": 52.0, "F3": 81.0}
curves = []
for i in range(6):
    base = np.exp(-x / (25 + 18 * i)) * 0.6 + 0.4 * np.exp(-((x - 10) / 60) ** 2)
    for j, (k, f) in enumerate(features.items()):
        base *= 1 - (0.10 + 0.04 * ((i + j) % 3)) * np.exp(-0.5 * ((x - f) / 1.2) ** 2)
    base *= 1 / (1 + np.exp(-(x - 4) / 1.5))
    curves.append(base / base.max() * 0.8 + rng.normal(0, 0.004, x.size))
params = [1, 2, 3, 4, 5, 6]
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(89, 74))
cols = n_colors(truncate_cmap(NS_EMBER, 0.15, 0.80), len(curves))
ridgeline(ax, x, curves, cols, offset=0.55, fill="gradient", fill_alpha=0.55,
          labels_left=[f"Data {i + 1}" for i in range(len(curves))],
          labels_right=[f"$p$ = {p}" for p in params])
for k, f in features.items():
    ax.axvline(f, color="0.6", ls=":", lw=0.6, zorder=0.5)
    ax.annotate(k, (f, 1.0), xycoords=("data", "axes fraction"), xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=5.5, color="0.4")
ax.set_xlim(0, 100); ax.set_ylim(-0.05, 0.55 * len(curves) + 0.45)
ax.set_yticks([]); ax.set_xlabel("Variable $x$ (unit)")
style_axes(ax); ax.tick_params(axis="y", which="both", left=False, right=False)
export(fig, "P02_offset_curves")
