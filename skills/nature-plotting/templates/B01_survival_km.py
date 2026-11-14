"""B01 -- Kaplan-Meier survival curves with confidence bands, censoring ticks and a numbers-at-risk table.
Use when: time-to-event outcomes are compared between arms / groups (clinical, reliability, churn); the
at-risk table and the hazard ratio with P are part of the figure, not the legend.
Look: open axes, step curves in two strong but CVD-safe hues, light CI bands, '|' ticks at censoring, the
at-risk numbers aligned under the x ticks in the curve colours, HR and log-rank P in the free corner.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(109)


def arm(n, scale, cens_max=60):
    t_event = rng.weibull(1.3, n) * scale
    t_cens = rng.uniform(10, cens_max, n)
    return np.minimum(t_event, t_cens), (t_event <= t_cens).astype(int)


groups = [arm(210, 40), arm(205, 26)]
labels = ["Treatment", "Control"]
hr_text = ["HR = 0.62 (95% CI 0.48–0.81)", "Log-rank P = 4 × 10$^{-4}$"]
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["ochre"]]
fig, ax = plt.subplots(figsize=figsize_mm(89, 72))
fig.subplots_adjust(left=0.24, right=0.97, bottom=0.36, top=0.97)
for (t, e), c, lab in zip(groups, cols, labels):
    km_curve(ax, t, e, c, label=lab)
ax.set_xlim(0, 60); ax.set_ylim(0, 1.02)
ax.set_xticks([0, 12, 24, 36, 48, 60]); ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25", "50", "75", "100"])
ax.set_xlabel("Time since enrolment (months)", labelpad=1.5); ax.set_ylabel("Event-free survival (%)")
ax.legend(loc="upper right")
stats_text(ax, hr_text, loc="lower left")
at_risk_table(ax, groups, [0, 12, 24, 36, 48, 60], labels, cols, y0=-0.36, row_h=0.1)
export(fig, "B01_survival_km")
