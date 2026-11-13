"""P04 -- Difference curves (A - B) for reference and model, with a low-confidence region.
Use when: the claim is about recovering a *contrast* between two curves, not the curves themselves.
Nature notes: zero line in light grey; reference grey solid, model dashed in the pair colour; shade the
region where the measurement is unreliable and say why in one line.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
x = np.linspace(0, 100, 700)
rng = np.random.default_rng(12)
def smooth(y, n=9):
    return np.convolve(y, np.ones(n) / n, mode="same")
pairs = [("Data 1 − Data 2", PALETTE["blue"]), ("Data 3 − Data 4", "#C99A1E")]
diffs = []
for k in range(2):
    base = -0.18 * np.exp(-((x - 35) / 22) ** 2) if k == 0 else 0.15 * np.exp(-((x - 50) / 28) ** 2)
    feats = -0.12 * np.exp(-0.5 * ((x - 16) / 0.6) ** 2) + 0.08 * np.exp(-0.5 * ((x - 49) / 0.8) ** 2)
    ref = base + feats + smooth(rng.normal(0, 0.01, x.size))
    diffs.append((ref, ref + smooth(rng.normal(0, 0.025, x.size), 15) + (0.02 if k else -0.02) * (x > 62)))
# -------------------------------------------

fig, axes = plt.subplots(2, 1, figsize=figsize_mm(70, 64), sharex=True, gridspec_kw=dict(hspace=0.35))
for ax, (name, c), (ref, mod) in zip(axes, pairs, diffs):
    ax.axvspan(62, 100, color="0.92", lw=0, zorder=0)
    ax.axhline(0, color="0.7", lw=0.6)
    ax.plot(x, ref, color="0.45", lw=0.9)
    ax.plot(x, mod, color=c, lw=0.9, ls=(0, (3, 1.2)))
    ax.text(0.0, 1.03, name, transform=ax.transAxes, color=c, fontsize=6, ha="left", va="bottom")
    ax.set_ylabel("Δ signal"); ax.set_xlim(0, 100)
    style_axes(ax)
axes[0].text(0.99, 1.03, "grey: reference; dashed: model", transform=axes[0].transAxes, ha="right",
             va="bottom", fontsize=5.5, color="0.4")
axes[1].text(0.99, 1.03, "grey band: low confidence", transform=axes[1].transAxes, ha="right", va="bottom",
             fontsize=5.5, color="0.4")
axes[-1].set_xlabel("Variable $x$ (unit)")
export(fig, "P04_difference_curves")
