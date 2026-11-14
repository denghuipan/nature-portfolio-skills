"""T01 -- Measured points against a model curve on a log axis, hollow markers, keyed in a dashed box.
Use when: several measurement variants (full / reduced / approximate ...) are compared with one prediction
over a size or depth parameter, and a second panel extrapolates where only some variants can be measured.
Look: framed axes with a faint grid (set_look("framed")), hollow o / x / + markers, black model line,
dashed key box, small dashed-box inset sketch, vertical arrows carrying cost notes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
set_look("framed")

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(4)
n = np.arange(12, 54, 2)
model = 0.55 * np.exp(-0.095 * (n - 8))
model[n > 34] *= 0.8                                   # a kink where the model changes regime
d1 = model * np.exp(rng.normal(0, 0.05, n.size))      # Data 1 (full)
d2 = model * np.exp(rng.normal(0, 0.07, n.size))      # Data 2 (reduced)
d3 = model * np.exp(rng.normal(0, 0.07, n.size))      # Data 3 (approximate)
m = np.array([12, 14, 16, 18, 20])
mod_b = 0.022 * np.exp(-0.21 * (m - 12)) + 0.0006
est_b = mod_b * np.exp(rng.normal(0, 0.06, m.size))
err_b = est_b * np.array([0.18, 0.25, 0.3, 0.38, 0.6])
cost = [("2 h", "1 d"), ("2 wk", "4 yr"), ("4 yr", "600 yr"), ("100 yr", None), ("10,000 yr", None)]
# -------------------------------------------
C = THEMES["signal"]
fig = plt.figure(figsize=figsize_2col(78))
gs = fig.add_gridspec(1, 2, width_ratios=[2.25, 1], wspace=0.08, left=0.07, right=0.99, bottom=0.13, top=0.9)
ax, bx = fig.add_subplot(gs[0]), fig.add_subplot(gs[1], sharey=None)

ax.plot(n, model, color="k", lw=1.0, zorder=2, label="Model prediction")
ax.plot(n, d1, "o", ms=4.2, mfc="none", mec=C[0], mew=0.8, label="Data 1")
ax.plot(n, d2, "x", ms=4.2, color=C[1], mew=0.9, label="Data 2")
ax.plot(n, d3, "+", ms=5.0, color=C[2], mew=0.9, label="Data 3")
ax.set_yscale("log"); ax.set_ylim(1e-3, 1.2); ax.set_xlim(10, 55)
ax.set_xlabel("System size, $n$"); ax.set_ylabel("Score, $S$")
subtitle(ax, "Directly measurable")
legend_box(ax, loc="lower left", ncols=2, columnspacing=1.2, title="Depth $d$ = 14", title_fontsize=6)
# inset sketch: a dashed box holding a small dot lattice (stand-in for an illustration of the setting)
ins = ax.inset_axes([0.55, 0.70, 0.42, 0.26]); ins.set_xlim(0, 10); ins.set_ylim(0, 4); ins.axis("off")
dashed_frame(ax, 0.55, 0.70, 0.97, 0.96)
gi, gj = np.meshgrid(np.arange(6), np.arange(3))
ins.scatter(0.8 + gi.ravel() * 0.7, 0.8 + gj.ravel() * 1.1, s=14,
            c=[[C[0], C[1], C[2]][(i + j) % 3] for i, j in zip(gi.ravel(), gj.ravel())], alpha=0.85)
for k, t in enumerate("ABCD"):
    ins.add_patch(plt.Rectangle((5.6 + k * 1.05, 1.2), 0.6, 1.6, color=lighten(C[2], 0.25 * k), lw=0))
    ins.text(5.9 + k * 1.05, 0.55, t, ha="center", va="center", fontsize=6, color=C[2])

bx.errorbar(m, est_b, yerr=err_b, fmt="x", ms=4.5, color=C[1], mew=0.9, elinewidth=0.7, capsize=2,
            label="Data 2 (±5$\\sigma$)")
bx.plot(m, mod_b, color="k", lw=1.0, label="Model prediction")
bx.set_yscale("log"); bx.set_ylim(1e-3, 1.2); bx.set_xlim(11, 21); bx.set_xticks(m)
bx.tick_params(labelleft=False)
bx.set_xlabel("Depth, $d$")
subtitle(bx, "Extrapolated regime")
for x, y, (c1, c2) in zip(m, est_b + err_b, cost):
    tail = y * 5                                           # arrow from here down to just above the error bar
    arrow_note(bx, x, tail, y * 1.25, c2 or c1, color=C[0] if c2 else "0.35")
    if c2:                                                 # a second cost estimate stacked above the first
        bx.text(x, tail * 1.75, c1, ha="center", va="bottom", fontsize=6, color="0.35")
bx.text(0.03, 0.97, "Cost: method X", transform=bx.transAxes, fontsize=6, color="0.35", va="top")
bx.text(0.03, 0.91, "Cost: method Y", transform=bx.transAxes, fontsize=6, color=C[0], va="top")
legend_box(bx, loc="lower left", title="$n$ = 53", title_fontsize=6)
panel_label(ax, "a", dx=-0.09, dy=1.1); panel_label(bx, "b", dx=-0.06, dy=1.1)
export(fig, "T01_marker_decay_log")
