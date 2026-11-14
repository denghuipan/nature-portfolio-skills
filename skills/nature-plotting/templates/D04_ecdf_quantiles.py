"""D04 -- Empirical cumulative distributions with medians marked, plus the same data as quantile dots.
Use when: several methods' error or latency distributions are compared without choosing bins; the median
and a high quantile (90th) are the numbers quoted in the text.
Look: open axes, log x, step ECDFs, median drop lines and dots, end labels instead of a legend; right
panel shows 10th-50th-90th percentiles as dots on a line per method.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(18)
methods = {"Method A": rng.lognormal(0.6, 0.8, 900), "Method B": rng.lognormal(1.3, 0.7, 900),
           "Method C": rng.lognormal(1.8, 0.9, 900)}
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["teal"], PALETTE["grey"]]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 52), gridspec_kw=dict(width_ratios=[1.5, 1]))
fig.subplots_adjust(left=0.08, right=0.97, bottom=0.2, top=0.94, wspace=0.42)
for (nm, v), c in zip(methods.items(), cols):
    ecdf(a, v, c, label=nm)
    m = np.median(v)
    a.plot([m, m], [0, 0.5], color=c, lw=0.5, ls=(0, (2, 1.5)))
    a.plot(m, 0.5, "o", color=c, ms=2.6)
a.axhline(0.5, color="0.8", lw=0.5, zorder=0)
a.set_xscale("log"); a.set_xlim(0.2, 100); a.set_ylim(0, 1.0)
a.set_xticks([1, 10, 100], ["1", "10", "100"])
a.set_xlabel("Error (unit)"); a.set_ylabel("Cumulative fraction")
a.legend(loc="lower right", handlelength=1.2)
y = np.arange(len(methods))[::-1]
for yi, ((nm, v), c) in zip(y, zip(methods.items(), cols)):
    q10, q50, q90 = np.percentile(v, [10, 50, 90])
    b.plot([q10, q90], [yi, yi], color=c, lw=1.0, solid_capstyle="round")
    b.plot([q10, q90], [yi, yi], "o", color=c, ms=2.2)
    b.plot(q50, yi, "o", ms=4.2, mfc="white", mec=c, mew=1.0)
b.set_xscale("log"); b.set_xlim(0.3, 50); b.set_xticks([1, 10], ["1", "10"])
b.set_yticks(y, list(methods)); b.tick_params(axis="y", length=0)
b.set_ylim(-0.6, len(methods) - 0.4)
b.set_xlabel("Error (unit)")
b.text(0.5, 1.0, "10th, 50th (open), 90th percentile", transform=b.transAxes, ha="center", va="bottom", color="0.35")
panel_label(a, "a", dx=-0.14, dy=1.06); panel_label(b, "b", dx=-0.42, dy=1.06)
export(fig, "D04_ecdf_quantiles")
