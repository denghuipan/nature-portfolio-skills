"""R07 -- Scatter with one regression line and confidence band per group; slopes written at the line ends.
Use when: the same relationship is fitted in 2-4 groups (sexes, sites, species, conditions) and the claim is
about different slopes or offsets.
Look: open axes, group marker shapes AND colours (readable in greyscale), light 95% CI bands, slope with
CI at the right end of each line, no legend box.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(47)
groups = {"Group 1": (0.9, 1.0, 45, "o"), "Group 2": (0.55, 2.4, 40, "s"), "Group 3": (0.2, 3.6, 38, "^")}
data = {}
for g, (slope, icpt, n, m) in groups.items():
    x = rng.uniform(0, 10, n)
    data[g] = (x, icpt + slope * x + rng.normal(0, 1.0, n))
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["ochre"], PALETTE["plum"]]
fig, ax = plt.subplots(figsize=figsize_mm(89, 64))
fig.subplots_adjust(left=0.12, right=0.78, bottom=0.15, top=0.96)
ends_y, labs = [], []
for (g, (slope, icpt, n, m)), c in zip(groups.items(), cols):
    x, y = data[g]
    ax.scatter(x, y, s=8, marker=m, facecolors="none" if m != "o" else lighten(c, 0.45), edgecolors=c,
               linewidths=0.6, zorder=3)
    X = np.c_[np.ones_like(x), x]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta; s2 = resid @ resid / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    xx = np.linspace(0, 10, 100); XX = np.c_[np.ones_like(xx), xx]
    se = np.sqrt(np.einsum("ij,jk,ik->i", XX, cov, XX))
    yy = XX @ beta
    ax.fill_between(xx, yy - 1.97 * se, yy + 1.97 * se, color=c, alpha=0.15, lw=0)
    ax.plot(xx, yy, color=c, lw=1.0)
    ends_y.append(yy[-1]); labs.append(f"{g}\nslope {beta[1]:.2f} ± {1.97 * np.sqrt(cov[1, 1]):.2f}")
end_labels(ax, 10, ends_y, labs, colors=cols, min_gap=16, linespacing=1.1)
ax.set_xlim(0, 10); ax.set_xlabel("Predictor (unit)"); ax.set_ylabel("Outcome (unit)")
export(fig, "R07_group_regression")
