"""C07 -- Forest plot: estimates with confidence intervals per subgroup, against a reference value.
Use when: effect sizes, offsets or residuals for many subgroups, plus a pooled estimate.
Nature notes: reference line dashed; marker size encodes weight / n; separate the pooled row with a rule;
the interval definition (95 % CI) goes in the axis label.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
labels = [f"Subgroup {i}" for i in range(1, 10)] + ["Pooled"]
rng = np.random.default_rng(15)
est = np.r_[rng.normal(0.0, 0.03, 5), rng.normal(0.05, 0.05, 4), 0.02]
half = np.r_[rng.uniform(0.02, 0.05, 5), rng.uniform(0.06, 0.12, 4), 0.018]
n = np.r_[rng.integers(20, 60, 9), 300]
# -------------------------------------------

fig, ax = plt.subplots(figsize=figsize_mm(70, 62))
cols = ["0.2"] * 5 + [PALETTE["red"]] * 4 + ["k"]
sizes = 2.5 + 3 * np.sqrt(n / n.max())
y = forest(ax, labels, est, est - half, est + half, ref=0.0, colors=cols, sizes=sizes)
ax.plot(est[-1], y[-1], "D", ms=4.5, color="k", zorder=4)
ax.axhline(y[-1] + 0.5, color="0.8", lw=0.5)
ax.set_xlabel("Effect (unit), 95 % CI"); ax.set_xlim(-0.2, 0.3)
stats_text(ax, ["Set 1: grey", "Set 2: red"], loc="upper right")
style_axes(ax); ax.tick_params(axis="y", which="both", left=False, right=False)
export(fig, "C07_forest")
