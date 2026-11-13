"""P03 -- Model mean +- sigma across conditions (ensembles, bootstraps, Monte-Carlo dropout).
Use when: showing how predictive uncertainty grows as the input degrades.
Nature notes: one colour per regime (blue = reliable, red = degraded); reference dashed black on top;
say what the band is (+-1 sigma over N runs) once, in a shared legend.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(-12, 12, 300)
ref = gauss(x, 0, 1.0, 2.0)
conds = [("Condition 1", 1.00, 0.03, 0.00, PALETTE["blue"]),
         ("Condition 2", 0.55, 0.15, 0.03, PALETTE["salmon"]),
         ("Condition 3", 0.18, 0.39, 0.09, PALETTE["red"])]
# -------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=figsize_2col(52), gridspec_kw=dict(wspace=0.28))
for ax, (title, amp, s_peak, s_bg, c) in zip(axes, conds):
    mean = gauss(x, 0, amp, 2.0)
    sig = s_bg + s_peak * gauss(x, 0, 1.0, 2.6)
    ci_band(ax, x, mean - sig, mean + sig, c, alpha=0.30)
    ax.plot(x, mean, color=c, lw=1.1, label="Model mean")
    ax.plot(x, ref, "k--", lw=0.8, label="Reference")
    ax.set_title(title, fontsize=6, pad=3)
    ax.set_xlim(x[0], x[-1]); ax.set_ylim(-0.25, 1.1); ax.set_xlabel("Variable $x$ (unit)")
    style_axes(ax)
axes[0].set_ylabel("Signal (norm.)")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h + [mpl.patches.Patch(color=PALETTE["blue"], alpha=0.3, lw=0)], l + ["±1σ (50 runs)"],
           loc="lower center", bbox_to_anchor=(0.5, 0.97), ncols=3, handlelength=1.6)
for ax, k in zip(axes, "abc"):
    panel_label(ax, k, dx=-0.24, dy=1.12)
export(fig, "P03_uncertainty_bands")
