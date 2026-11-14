"""C01 -- Benchmark bars across task families: soft fills, error bars, significance brackets, n under each bar.
Use when: one method is compared with baselines on several benchmark subsets of different sizes, and the
reader needs the success rate, its uncertainty, the test result and the sample size in one glance.
Look: open axes, the method of interest in a light hue, baselines in greys (or a darker tone of the same
hue), no bar outlines, thin error bars without caps, brackets with stars, 'n = ...' on a second tick line,
one subtitle per family, shared y axis on the left only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(2)
fam1 = dict(labels=["Method A", "Method B", "Method C"], ns=[428, 428, 427], m=[76, 52, 42], e=[4, 5, 5])
fam2 = dict(labels=["Subset 1", "Subset 2", "Subset 3"], ns=[25, 38, 8],
            a=[39, 65, 47], b=[19, 28, 35], ea=[12, 7, 9], eb=[4, 8, 6])
fam3 = dict(labels=["Type 1", "Type 2", "Type 3", "Type 4", "Type 5"], ns=[66, 28, 40, 91, 23],
            m=[78, 72, 51, 68, 41], e=[8, 13, 15, 9, 19])
fam4 = dict(labels=["Pair 1", "Pair 2", "Pair 3"], ns=[1064, 65, 338],
            a=[76, 63, 86], b=[67, 30, 85], ea=[2, 10, 1], eb=[2, 8, 1])
# -------------------------------------------
cA, cB, cC = THEMES["soft"][0], THEMES["soft"][2], THEMES["soft"][3]
cA2 = THEMES["soft"][1]
fig = plt.figure(figsize=figsize_2col(62))
gs = fig.add_gridspec(1, 4, width_ratios=[3, 3.6, 4.6, 3.4], wspace=0.12, left=0.06, right=0.995, top=0.86,
                      bottom=0.22)
axs = [fig.add_subplot(gs[i]) for i in range(4)]

ax = axs[0]
x = np.arange(3)
bars(ax, x, fam1["m"], colors=[cA, cB, cB], err=fam1["e"], width=0.7)
ax.set_xticks(x); n_ticklabels(ax, fam1["labels"], fam1["ns"])
sig_bracket(ax, 0, 1, 90, "***"); sig_bracket(ax, 1, 2, 63, "**")
subtitle(ax, "Family 1")

ax = axs[1]
x = np.arange(3)
for k, (vals, errs, c, off) in enumerate(((fam2["a"], fam2["ea"], cA, -0.19), (fam2["b"], fam2["eb"], cB, 0.19))):
    bars(ax, x + off, vals, colors=[c] * 3, err=errs, width=0.36)
pts = [rng.normal(fam2["a"][2], 9, 8), rng.normal(fam2["b"][2], 7, 8)]
ax.scatter(np.full(8, 2 - 0.19) + rng.uniform(-0.06, 0.06, 8), pts[0], s=4, color=darken(cA, 0.35), zorder=5, lw=0)
ax.scatter(np.full(8, 2 + 0.19) + rng.uniform(-0.06, 0.06, 8), pts[1], s=4, color=darken(cB, 0.45), zorder=5, lw=0)
ax.set_xticks(x); n_ticklabels(ax, fam2["labels"], fam2["ns"])
sig_bracket(ax, -0.19, 0.19, 57, "**"); sig_bracket(ax, 0.81, 1.19, 78, "***")
square_legend(ax, ["Method A", "Method B"], [cA, cB], loc="upper right", bbox=(1.02, 1.03), ncols=2)
subtitle(ax, "Family 2")

ax = axs[2]
x = np.arange(5)
bars(ax, x, fam3["m"], colors=[cA] * 5, err=fam3["e"], width=0.62)
ax.set_xticks(x); n_ticklabels(ax, fam3["labels"], fam3["ns"])
subtitle(ax, "Family 3 (no baseline available)")

ax = axs[3]
x = np.arange(3)
for vals, errs, c, off in ((fam4["a"], fam4["ea"], cA, -0.19), (fam4["b"], fam4["eb"], cA2, 0.19)):
    bars(ax, x + off, vals, colors=[c] * 3, err=errs, width=0.36)
ax.set_xticks(x); n_ticklabels(ax, fam4["labels"], fam4["ns"])
for i in range(3):
    sig_bracket(ax, i - 0.19, i + 0.19, max(fam4["a"][i] + fam4["ea"][i], fam4["b"][i] + fam4["eb"][i]) + 6, "***")
square_legend(ax, ["Method A", "Method D"], [cA, cA2], loc="upper right", bbox=(1.02, 1.03), ncols=2)
subtitle(ax, "Family 4")

for i, ax in enumerate(axs):
    ax.set_ylim(0, 114); ax.set_yticks([0, 20, 40, 60, 80, 100]); ax.spines["left"].set_bounds(0, 100)
    ax.tick_params(axis="x", length=0)
    if i:
        despine(ax, left=True); ax.tick_params(labelleft=False)
axs[0].set_ylabel("Success (%)")
fig.text(0.006, 0.97, "a", fontsize=8, fontweight="bold", va="top")
export(fig, "C01_bars_significance")
