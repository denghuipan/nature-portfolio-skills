"""D04 -- One quantity in several groups: step histograms + density (a) and ECDF (b).
Use when: comparing residual / error distributions; the ECDF answers 'what fraction is below X' exactly.
Nature notes: outline (step) histograms overlay cleanly; state the bin width; short ticks mark medians;
the ECDF needs no binning choice and shows the tails.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(34)
groups = {"Data 1": rng.normal(0, 38, 2000), "Data 2": rng.normal(5, 55, 2000), "Data 3": rng.standard_t(4, 2000) * 9}
colors = ["0.45", "#B08850", "#5B2C91"]
# -------------------------------------------

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_2col(54), gridspec_kw=dict(wspace=0.32))
bins = np.arange(-200, 201, 10); grid = np.linspace(-200, 200, 400)
for (name, v), c in zip(groups.items(), colors):
    hist_step(a, v, bins, c, label=name)
    kde_line(a, v, grid, c, lw=0.7, ls=(0, (3, 1.5)))
    a.plot([np.median(v)] * 2, [0, 0.0015], color=c, lw=1.4)
    ecdf(b, np.abs(v), c, label=name)
a.set_xlim(-200, 200); a.set_ylim(0, None)
a.set_xlabel("Residual (unit)"); a.set_ylabel("Density (unit$^{-1}$)")
a.legend(loc="upper left"); stats_text(a, ["bin width 10"], loc="upper right")
b.set_xscale("log"); b.set_xlim(0.5, 400); b.set_ylim(0, 1.02)
for q in (0.5, 0.9):
    b.axhline(q, color="0.75", lw=0.5, ls=":")
    b.text(0.55, q, f"{int(q * 100)} %", va="bottom", fontsize=5.5, color="0.4")
b.set_xlabel("|Residual| (unit)"); b.set_ylabel("Cumulative fraction")
for ax_, l in ((a, "a"), (b, "b")):
    style_axes(ax_); panel_label(ax_, l, dx=-0.2)
export(fig, "D04_hist_kde_ecdf")
