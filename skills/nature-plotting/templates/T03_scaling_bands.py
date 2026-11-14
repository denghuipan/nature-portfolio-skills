"""T03 -- Scaling with effort (log x): mean with markers and a confidence band per method, a vertical
significance bracket at the right edge, panel subtitles that say what is measured.
Use when: a success rate or score is tracked against samples / seeds / compute / dose for two methods, and
the gap at the largest budget is the claim.
Look: open axes, two tones of one hue (light = new method, dark = reference), dots joined by thin lines,
light bands, '***' bracket outside the plot area, one shared legend centred under both panels.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
budget = np.unique(np.round(np.logspace(0, 3, 14)))
lb = np.log10(budget)
panels = {
    "Score > 0.25\n(subset A)": dict(new=(38, 26), ref=(17, 11), y=(0, 75)),
    "Score > 0.80\n(subset A)": dict(new=(12, 18), ref=(4, 6), y=(0, 40)),
}
# -------------------------------------------
c_new, c_ref = PAIRED[0][0], PAIRED[0][1]
c_new = "#7FA9DB"
fig, axs = plt.subplots(1, 2, figsize=figsize_mm(89, 52))
fig.subplots_adjust(left=0.13, right=0.93, bottom=0.30, top=0.83, wspace=0.55)
for ax, (title, p) in zip(axs, panels.items()):
    m_new = p["new"][0] + p["new"][1] * (1 - np.exp(-lb / 1.2))
    m_ref = p["ref"][0] + p["ref"][1] * (1 - np.exp(-lb / 1.6))
    for m, c, lab in ((m_new, c_new, "Method A"), (m_ref, c_ref, "Method B")):
        ax.fill_between(budget, m - 0.22 * m, m + 0.22 * m, color=c, alpha=0.22, lw=0)
        ax.plot(budget, m, "-o", color=c, ms=2.2, lw=0.8, label=lab)
    ax.set_xscale("log"); ax.set_xlim(0.8, 1300); ax.set_ylim(*p["y"])
    ax.set_xticks([1, 10, 100, 1000], ["1", "10", "100", "1,000"])
    ax.set_xlabel("Samples per target")
    ax.set_ylabel("Success rate (%)")
    subtitle(ax, title, pad=3)
    sig_bracket(ax, m_ref[-1], m_new[-1], 1700, "***", vertical=True)
panel_label(axs[0], "a", dx=-0.42, dy=1.32); panel_label(axs[1], "b", dx=-0.42, dy=1.32)
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncols=2, bbox_to_anchor=(0.5, 0.0))
export(fig, "T03_scaling_bands")
