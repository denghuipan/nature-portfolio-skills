"""D02 -- Histogram with a fitted curve and its parameters; and a two-component fit on a log count axis.
Use when: a measured distribution is summarised by a model (Gaussian, log-normal, mixture) and the fit
quality and parameters are reported.
Look: open axes, solid pale bars touching, fitted curve as a dark line, parameters written in the free
corner (mu, sigma, n), components dashed, total solid on the log panel.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.stats import norm

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(6)
v1 = rng.normal(98.4, 1.1, 2400)                         # e.g. fidelity of repeated runs (%)
v2 = np.r_[rng.normal(-2.0, 0.45, 6000), rng.normal(0.4, 0.8, 1800)]
# -------------------------------------------
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 50))
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.22, top=0.93, wspace=0.38)
bins = np.linspace(94, 102, 41)
_, _, pa = a.hist(v1, bins=bins, color=PALETTE["blue"], lw=0)
gradient_patches(a, pa, PALETTE["blue"], light=0.8)
mu, sd = norm.fit(v1)
xx = np.linspace(94, 102, 300)
a.plot(xx, norm.pdf(xx, mu, sd) * v1.size * np.diff(bins)[0], color=PALETTE["navy"], lw=1.0)
stats_text(a, [f"$\\mu$ = {mu:.2f}%", f"$\\sigma$ = {sd:.2f}%", f"n = {v1.size:,}"], loc="upper left")
a.set_xlabel("Score (%)"); a.set_ylabel("Count"); a.set_xlim(94, 102)

bins = np.linspace(-4, 4, 61)
cnt, e, pb = b.hist(v2, bins=bins, color=lighten(PALETTE["plum"], 0.45), lw=0)
gradient_patches(b, pb, lighten(PALETTE["plum"], 0.2), light=0.75)
w = np.diff(e)[0]
c1 = norm.pdf(xx := np.linspace(-4, 4, 400), -2.0, 0.45) * 6000 * w
c2 = norm.pdf(xx, 0.4, 0.8) * 1800 * w
b.plot(xx, c1, color=PALETTE["plum"], lw=0.8, ls=(0, (3, 1.5)), label="Component 1")
b.plot(xx, c2, color=PALETTE["ochre"], lw=0.8, ls=(0, (3, 1.5)), label="Component 2")
b.plot(xx, c1 + c2, color="0.1", lw=0.9, label="Sum")
b.set_yscale("log"); b.set_ylim(1, 3000); b.set_xlim(-4, 4)
b.set_xlabel("Log ratio"); b.set_ylabel("Count")
b.legend(loc="upper right", handlelength=1.8)
panel_label(a, "a", dx=-0.22, dy=1.06); panel_label(b, "b", dx=-0.25, dy=1.06)
export(fig, "D02_hist_fit")
