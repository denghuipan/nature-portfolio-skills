"""L02 -- Saturating responses with fitted sigmoids, a detection threshold and the shift between them.
Use when: dose-response, transfer curves, signal vs input level for two conditions; claim = 'shifted by D'.
Nature notes: markers = data, lines = fit; the claimed number sits on a measurement arrow between the two
threshold crossings; a soft tint under each curve groups data and fit without a legend.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(4)
def logistic(x, top, x0, k):
    return top / (1 + np.exp(-(x - x0) / k))
x1 = np.arange(0, 51, 4.0); x2 = np.arange(30, 101, 5.0)
y1 = logistic(x1, 31.5, 22, 3.6) + rng.normal(0, 0.6, x1.size)
y2 = logistic(x2, 27.8, 62, 4.2) + rng.normal(0, 0.5, x2.size)
thr = 3.0
# -------------------------------------------

from scipy.optimize import curve_fit
fig, ax = plt.subplots(figsize=figsize_1col(60))
xf = np.linspace(-2, 102, 400)
cross = []
for xs, ys, c, m, guess, name in [(x1, y1, "#5B2C91", "s", (31, 22, 4), "Data 1"),
                                   (x2, y2, "0.55", "o", (28, 62, 4), "Data 2")]:
    popt, _ = curve_fit(logistic, xs, ys, p0=guess)
    yf = logistic(xf, *popt)
    gradient_fill(ax, xf, yf, color=c, alpha=0.18, ymin=0)
    ax.plot(xf, yf, color=c, lw=1.2, zorder=3)
    ax.plot(xs, ys, m, color=c, ms=3.0, mec="w", mew=0.4, zorder=4)
    xc = popt[1] - popt[2] * np.log(popt[0] / thr - 1)
    cross.append(xc)
    ax.plot(xc, thr, "o", ms=3.5, mfc="w", mec=c, mew=0.9, zorder=5)
    direct_label(ax, popt[1] + 4, 12, name, color=c, ha="left")
ax.axhline(thr, color="0.55", ls=":", lw=0.8, zorder=1)
direct_label(ax, 85, thr, "Threshold", color="0.4", ha="center", va="bottom", dy=1)
double_arrow(ax, (cross[0], thr + 4.5), (cross[1], thr + 4.5), f"Δ = {cross[1] - cross[0]:.1f}")
ax.set_xlim(-2, 102); ax.set_ylim(-1, 35)
ax.set_xlabel("Input level (a.u.)"); ax.set_ylabel("Response (a.u.)")
style_axes(ax)
export(fig, "L02_sigmoid_fit")
