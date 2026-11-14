"""D08 -- Two-dimensional density as contour lines over a thinned scatter, with marginal density curves.
Use when: thousands of (x, y) pairs from two or three populations overlap; filled hexbins would hide one
population, contour lines keep all of them readable.
Look: open axes, light points (a random subset), contour lines at the 25 / 50 / 75 / 95 % probability
mass levels in the population colour, marginal KDE lines without axes, direct population labels.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.stats import gaussian_kde

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(51)
popA = rng.multivariate_normal([1.0, 1.2], [[0.25, 0.12], [0.12, 0.2]], 3000)
popB = rng.multivariate_normal([2.6, 2.4], [[0.3, -0.1], [-0.1, 0.25]], 2000)
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["ochre"]]
fig = plt.figure(figsize=figsize_mm(80, 76))
gs = fig.add_gridspec(2, 2, width_ratios=[4, 0.8], height_ratios=[0.8, 4], hspace=0.04, wspace=0.04,
                      left=0.14, right=0.98, bottom=0.13, top=0.98)
ax = fig.add_subplot(gs[1, 0]); tx = fig.add_subplot(gs[0, 0], sharex=ax); ry = fig.add_subplot(gs[1, 1], sharey=ax)
xg, yg = np.linspace(-0.8, 4.5, 140), np.linspace(-0.5, 4.2, 140)
X, Y = np.meshgrid(xg, yg)
for P, c, lab in ((popA, cols[0], "Population A"), (popB, cols[1], "Population B")):
    sub = P[rng.choice(len(P), 500, replace=False)]
    ax.scatter(sub[:, 0], sub[:, 1], s=1.5, color=lighten(c, 0.35), lw=0, zorder=1, rasterized=True)
    k = gaussian_kde(P.T)
    Z = k(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
    zs = np.sort(Z.ravel())[::-1]; cdf = np.cumsum(zs) / zs.sum()
    levels = sorted(zs[np.searchsorted(cdf, q)] for q in (0.95, 0.75, 0.5, 0.25))
    ax.contour(X, Y, Z, levels=levels, colors=[c], linewidths=[0.5, 0.7, 0.9, 1.1], zorder=2)
    kx = gaussian_kde(P[:, 0])(xg); ky = gaussian_kde(P[:, 1])(yg)
    tx.plot(xg, kx, color=c, lw=0.9); gradient_fill(tx, xg, kx, c, alpha=0.4, ymin=0)
    ry.plot(ky, yg, color=c, lw=0.9); ry.fill_betweenx(yg, 0, ky, color=c, alpha=0.15, lw=0)
    mx, my = P.mean(0)
    ax.text(mx + (0.9 if c == cols[1] else -0.95), my + (0.85 if c == cols[1] else 0.95), lab, color=darken(c, 0.15), ha="center")
for m in (tx, ry):
    m.set_xticks([]); m.set_yticks([])
tx.set_ylim(0, None); ry.set_xlim(0, None)
ax.set_xlim(-0.8, 4.5); ax.set_ylim(-0.5, 4.2)
ax.set_xlabel("Variable $x$ (unit)"); ax.set_ylabel("Variable $y$ (unit)")
ax.text(0.98, 0.02, "Contours: 25, 50, 75, 95% of mass", transform=ax.transAxes, ha="right",
        color="0.35")
export(fig, "D08_density_contours")
