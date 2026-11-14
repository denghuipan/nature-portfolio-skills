"""R04 -- Volcano plot: effect size against significance for thousands of features, top hits labelled.
Use when: a screen or differential analysis tests many features at once (genes, proteins, metabolites,
variants, parameters) and the reader needs the count of hits on each side and their names.
Look: open axes, grey non-significant cloud (rasterised), up / down hits in the up-down pair, dashed
threshold lines, hit counts written in the upper corners, labels placed to avoid overlap.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(29)
n = 6000
effect = rng.normal(0, 0.7, n)
effect[:120] += rng.choice([-1, 1], 120) * rng.uniform(1.2, 3.2, 120)
z = np.abs(effect) / 0.35 + rng.normal(0, 1.0, n)
pval = np.clip(2 * (1 - 0.5 * (1 + np.tanh(z * 0.8))), 1e-30, 1)
names = [f"Feature {i}" for i in range(n)]
# -------------------------------------------
fig, ax = plt.subplots(figsize=figsize_mm(80, 70))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.14, top=0.94)
up, dn = volcano(ax, effect, pval, effect_thr=1.0, p_thr=1e-3, names=names, label_top=8, s=3)
ax.set_xlabel("Effect size (log$_2$ fold change)"); ax.set_ylabel("−log$_{10}$ P")
ax.set_xlim(-4.2, 4.2); ax.set_ylim(0, None)
ax.text(0.02, 0.03, f"{dn.sum():,} down", transform=ax.transAxes, va="bottom", fontsize=6,
        color=THEMES["updown"][1])
ax.text(0.98, 0.03, f"{up.sum():,} up", transform=ax.transAxes, va="bottom", ha="right", fontsize=6,
        color=THEMES["updown"][0])
export(fig, "R04_volcano")
