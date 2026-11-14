"""N04 -- Reliability diagram: observed frequency against predicted probability, with the bin counts below.
Use when: a model outputs probabilities / confidences and the claim is that they are calibrated (or that a
recalibration helps); ECE is reported.
Look: square open panel, perfect-calibration diagonal in grey, bars from the diagonal to the observed value
(the gap) in a light tint, observed values as dots and line, a short count strip on a log axis below.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(107)
p = rng.beta(2.2, 1.4, 20000)
truth_raw = rng.random(p.size) < np.clip(p ** 1.6, 0, 1)                  # over-confident model
p_cal = np.clip(p ** 1.6 + rng.normal(0, 0.02, p.size), 0, 1)
truth_cal = rng.random(p.size) < p_cal
# -------------------------------------------
bins = np.linspace(0, 1, 11); mid = 0.5 * (bins[1:] + bins[:-1])


def rel(pp, yy):
    idx = np.clip(np.digitize(pp, bins) - 1, 0, 9)
    obs = np.array([yy[idx == i].mean() for i in range(10)]); cnt = np.bincount(idx, minlength=10)
    conf = np.array([pp[idx == i].mean() for i in range(10)])
    return obs, cnt, np.sum(cnt * np.abs(obs - conf)) / cnt.sum()


fig = plt.figure(figsize=figsize_mm(110, 66))
gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], hspace=0.1, wspace=0.35, left=0.1, right=0.98, top=0.92,
                      bottom=0.14)
for j, (pp, yy, title, c) in enumerate(((p, truth_raw, "Before recalibration", PALETTE["brick"]),
                                        (p_cal, truth_cal, "After recalibration", PALETTE["blue"]))):
    ax = fig.add_subplot(gs[0, j]); hx = fig.add_subplot(gs[1, j], sharex=ax)
    obs, cnt, ece = rel(pp, yy)
    ax.plot([0, 1], [0, 1], color="0.75", lw=0.6)
    ax.bar(mid, obs - mid, bottom=mid, width=0.09, color=lighten(c, 0.6), lw=0)
    ax.plot(mid, obs, "-o", color=c, ms=2.6, lw=0.9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_yticks([0, 0.5, 1])
    ax.tick_params(labelbottom=False); ax.set_ylabel("Observed frequency")
    stats_text(ax, [f"ECE = {ece:.3f}"], loc="upper left")
    subtitle(ax, title)
    hx.bar(mid, cnt, width=0.09, color="0.75", lw=0); hx.set_yscale("log"); hx.set_ylim(10, 2e4)
    hx.set_yticks([100, 10000], ["10$^2$", "10$^4$"]); hx.yaxis.set_minor_locator(mticker.NullLocator())
    hx.set_xticks([0, 0.5, 1]); hx.set_xlabel("Predicted probability"); hx.set_ylabel("n")
    panel_label(ax, "ab"[j], dx=-0.25, dy=1.12)
export(fig, "N04_calibration")
