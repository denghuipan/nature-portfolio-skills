"""M01 -- Cell heat map with white cell borders, a log colour bar, and a separate summary row.
Use when: a metric over two categorical / binned factors (condition x sample), plus one aggregate row.
Nature notes: white gridlines separate cells; a sequential map from light (good) to dark (bad); log norm when
values span decades; the aggregate row sits apart so it is not read as one more condition.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(51)
rows = [f"Condition {i}" for i in range(1, 6)]
cols = [f"S{j}" for j in range(1, 10)]
Z = 10 ** (rng.normal(-3.2, 0.25, (5, 9)) + np.linspace(0, 1.6, 5)[:, None])
Z[-1, -1] *= 6
summary = 10 ** rng.normal(-2.6, 0.3, (1, 9))
# -------------------------------------------

fig = plt.figure(figsize=figsize_mm(89, 58))
gs = fig.add_gridspec(2, 1, height_ratios=[5, 1], hspace=0.12, left=0.22, right=0.86, bottom=0.17, top=0.95)
a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
norm = mpl.colors.LogNorm(1e-4, 1e-1)
m = heatmap(a, Z[::-1], None, rows[::-1], cmap=NS_REDS, norm=norm)
heatmap(b, summary, cols, ["Summary"], cmap=NS_REDS, norm=norm)
a.tick_params(labelbottom=False)
b.set_xlabel("Sample")
cax = fig.add_axes([0.89, 0.17, 0.025, 0.78])
cb = fig.colorbar(m, cax=cax)
style_cbar(cb, "Error (a.u.)", minor=False)
export(fig, "M01_heatmap_annotated")
