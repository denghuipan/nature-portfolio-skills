"""B03 -- Time course of two groups: mean +- s.e.m. at each visit, a shaded treatment period and per-time-point
significance stars; the right panel shows the area under the curve per subject.
Use when: repeated measurements over days / weeks in treated vs control groups (animal studies, cohorts,
cultures), with a summary statistic tested separately.
Look: open axes, filled vs hollow markers, thin error bars without caps, stars above the time points that
differ, a light band and label for the treatment window, AUC as bars with points.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(127)
days = np.array([0, 3, 7, 10, 14, 21, 28])
n = 8
ctrl = np.array([rng.normal(100 + 6 * d, 8 + d, n) for d in days])
trt = np.array([rng.normal(100 + 6 * d - (3.2 * (d - 3) if d > 3 else 0), 8 + d * 0.8, n) for d in days])
pv = [1, 0.6, 0.04, 0.008, 6e-4, 2e-4, 1e-4]
window = (3, 14)
# -------------------------------------------
c1, c2 = "0.35", PALETTE["blue"]
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(110, 56), gridspec_kw=dict(width_ratios=[2.4, 1]))
fig.subplots_adjust(left=0.1, right=0.98, bottom=0.18, top=0.9, wspace=0.42)
regime(a, *window, color=PALETTE["ochre"], fade="up", alpha=(0.0, 0.32))
a.text(np.mean(window), 1.0, "Treatment", transform=a.get_xaxis_transform(), ha="center", va="bottom",
       color="0.35")
mean_sem(a, days, ctrl, c1, marker="o", mfc="white", label="Control", ms=3.2)
m2, e2 = mean_sem(a, days, trt, c2, marker="o", label="Treated", ms=3.2)
mc = ctrl.mean(1)
for d, p, y1, y2 in zip(days, pv, mc + ctrl.std(1) / np.sqrt(n), m2 + e2):
    s = p_to_stars(p)
    if s != "NS":
        a.text(d, max(y1, y2) + 8, s, ha="center", va="bottom")
a.set_xticks(days); a.set_xlabel("Day"); a.set_ylabel("Volume (mm$^3$)")
a.set_xlim(-1.5, 29.5); a.set_ylim(60, 330)
a.legend(loc="upper left")
auc_c = np.trapezoid(ctrl, days, axis=0) / 1000; auc_t = np.trapezoid(trt, days, axis=0) / 1000
bars(b, [0, 1], [auc_c.mean(), auc_t.mean()], colors=["0.82", lighten(c2, 0.45)],
     err=[auc_c.std(ddof=1) / np.sqrt(n), auc_t.std(ddof=1) / np.sqrt(n)], points=[auc_c, auc_t], width=0.62)
sig_bracket(b, 0, 1, max(auc_c.max(), auc_t.max()) + 0.4, "P = 0.002")
b.set_xticks([0, 1], ["Control", "Treated"]); b.tick_params(axis="x", length=0)
b.set_ylim(0, max(auc_c.max(), auc_t.max()) + 1.4)
b.set_ylabel("AUC (10$^3$ mm$^3$ d)")
panel_label(a, "a", dx=-0.15, dy=1.12); panel_label(b, "b", dx=-0.42, dy=1.12)
export(fig, "B03_timecourse_stars")
