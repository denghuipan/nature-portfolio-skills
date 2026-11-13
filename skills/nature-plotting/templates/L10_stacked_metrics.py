"""L10 -- Several metrics vs one shared x, stacked panels.
Use when: one experiment yields 2-4 figures of merit that should be read against the same x.
Nature notes: share x and hide inner tick labels; equal panel heights; tolerance band in light grey with its
value written once; two conditions = hollow vs filled marker, one legend for all panels.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.arange(1, 10, 1.0)
rng = np.random.default_rng(5)
m1_a = rng.normal(0, 1.2, x.size); m1_b = rng.normal(0, 1.6, x.size); m1_b[-1] = -10.5
m2_a = rng.normal(0, 1.2, x.size); m2_b = rng.normal(0, 2.0, x.size); m2_b[-1] = 23
m3_a = 1 - np.abs(rng.normal(0, 0.01, x.size)); m3_b = 1 - np.abs(rng.normal(0, 0.02, x.size)); m3_b[-1] = 0.63
# -------------------------------------------

fig, axes = plt.subplots(3, 1, figsize=figsize_mm(70, 82), sharex=True, gridspec_kw=dict(hspace=0.14))
cols = n_colors(truncate_cmap(NS_EMBER, 0.15, 0.85), x.size)
for ax, ya, yb, lab in zip(axes, (m1_a, m2_a, m3_a), (m1_b, m2_b, m3_b), ("Metric 1 (unit)", "Metric 2 (%)", "Metric 3")):
    ax.plot(x, yb, color="0.75", lw=0.7, zorder=1)
    ax.scatter(x, ya, s=16, facecolors="none", edgecolors=cols, marker="^", lw=0.8, zorder=3)
    ax.scatter(x, yb, s=10, c=cols, edgecolors="k", linewidths=0.3, zorder=4)
    ax.set_ylabel(lab)
    style_axes(ax)
band(axes[0], -2.5, 2.5, label="shaded: ±2.5")
axes[0].set_ylim(-13, 13); axes[1].set_ylim(-35, 35); axes[2].set_ylim(0.4, 1.12)
axes[2].axhline(0.5, color="0.6", ls=":", lw=0.6)
axes[2].legend(handles=[mpl.lines.Line2D([], [], ls="none", marker="^", mfc="none", mec="0.3", ms=3.5, label="Condition A"),
                        mpl.lines.Line2D([], [], ls="none", marker="o", mfc="0.4", mec="k", ms=3, label="Condition B")],
               loc="lower left", bbox_to_anchor=(0.0, 3.42), ncols=2)
axes[-1].set_xlabel("Sample"); axes[-1].set_xticks(x); axes[-1].set_xlim(0.4, 9.6)
for ax in axes:
    ax.tick_params(axis="x", which="minor", bottom=False, top=False)
export(fig, "L10_stacked_metrics")
