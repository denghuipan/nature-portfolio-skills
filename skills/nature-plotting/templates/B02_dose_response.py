"""B02 -- Dose-response curves: replicate means +- s.e.m. on a log dose axis, four-parameter logistic fits,
half-maximal doses marked.
Use when: several compounds / conditions are titrated and compared by potency (EC50 / IC50) and efficacy.
Look: open axes, log x with decade labels, marker shape and colour per compound, fitted curves as smooth
lines, dashed drop lines from the half-maximal point to the axis, EC50 values in a small table key.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(113)
dose = np.logspace(-3, 2, 11)                                  # e.g. µM
truth = {"Compound 1": (2, 98, 0.08, 1.1), "Compound 2": (5, 95, 1.2, 0.9), "Compound 3": (10, 70, 6.0, 1.4)}
reps = {k: [hill(d, *p) + rng.normal(0, 4, 3) for d in dose] for k, p in truth.items()}
# -------------------------------------------
cols = [PALETTE["blue"], PALETTE["teal"], PALETTE["ochre"]]; marks = ["o", "s", "^"]
fig, ax = plt.subplots(figsize=figsize_mm(80, 62))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.17, top=0.96)
xx = np.logspace(-3.3, 2.3, 300)
rows = []
for (nm, r), c, mk in zip(reps.items(), cols, marks):
    mean_sem(ax, dose, r, c, marker=mk, line=False, ms=3.2, mfc="white" if mk != "o" else c, mew=0.7)
    p = fit_hill(dose, [np.mean(v) for v in r])
    ax.plot(xx, hill(xx, *p), color=c, lw=1.0)
    half = hill(p[2], *p)
    ax.plot([p[2], p[2]], [-5, half], color=c, lw=0.5, ls=(0, (3, 2)))
    rows.append((nm, p[2], c))
ax.set_xscale("log"); ax.set_xlim(5e-4, 2e2); ax.set_ylim(-5, 110)
ax.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100])
ax.set_xlabel("Concentration (µM)"); ax.set_ylabel("Response (% of maximum)")
ax.text(0.03, 0.97, "EC$_{50}$ (µM)", transform=ax.transAxes, fontsize=6, va="top", color="0.3")
for i, (nm, ec, c) in enumerate(rows):
    ax.text(0.03, 0.89 - 0.075 * i, f"{nm}  {ec:.2g}", transform=ax.transAxes, fontsize=6, va="top", color=c)
ax.text(0.97, 0.04, "mean ± s.e.m., n = 3", transform=ax.transAxes, ha="right", fontsize=6, color="0.4")
export(fig, "B02_dose_response")
