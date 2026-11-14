"""D07 -- Paired measurements: each subject before and after, joined by a line, with mean +- s.e.m.
Use when: the same units (subjects, samples, devices) are measured under two conditions and the within-unit
change is the test (paired t-test / Wilcoxon).
Look: open axes, thin grey pair lines, hollow condition-1 points and filled condition-2 points, a mean +-
s.e.m. marker offset to the side, bracket with P; right panel shows the per-unit differences as a swarm.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(41)
n = 18
pre = rng.normal(52, 9, n)
post = pre + rng.normal(7, 5, n)
p_value = "P = 2 × 10$^{-5}$"
# -------------------------------------------
c = PALETTE["teal"]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(89, 56), gridspec_kw=dict(width_ratios=[1.4, 1]))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.17, top=0.9, wspace=0.55)
paired_lines(a, 0, 1, pre, post, color="0.7", lw=0.5)
a.plot(np.zeros(n), pre, "o", ms=3, mfc="white", mec="0.35", mew=0.6, zorder=3)
a.plot(np.ones(n), post, "o", ms=3, color=c, zorder=3)
for x, v, col in ((-0.25, pre, "0.35"), (1.25, post, c)):
    m, e = v.mean(), v.std(ddof=1) / np.sqrt(n)
    a.errorbar(x, m, yerr=e, fmt="s", ms=3.2, color=col, elinewidth=0.8, capsize=0, zorder=4)
sig_bracket(a, 0, 1, max(post.max(), pre.max()) + 4, p_value)
a.set_xticks([0, 1], ["Condition 1", "Condition 2"]); a.tick_params(axis="x", length=0)
a.set_xlim(-0.55, 1.55); a.set_ylabel("Response (unit)")
d = post - pre
beeswarm(b, 0, d, c, width=0.25, s=6)
b.errorbar(0.45, d.mean(), yerr=1.96 * d.std(ddof=1) / np.sqrt(n), fmt="o", ms=3.4, color="0.1",
           elinewidth=0.8)
b.axhline(0, color="0.3", lw=0.5)
b.set_xlim(-0.5, 0.8); b.set_xticks([0], ["Difference"]); b.tick_params(axis="x", length=0)
b.set_ylabel("Δ response (unit)")
b.text(0.52, d.mean(), "  mean\n  95% CI", va="center", fontsize=6, color="0.3")
panel_label(a, "a", dx=-0.32, dy=1.1); panel_label(b, "b", dx=-0.62, dy=1.1)
export(fig, "D07_paired_points")
