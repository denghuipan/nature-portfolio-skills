"""L09 -- Step (set-point) history on two stacked panels, with a twin axis on the lower one.
Use when: showing how a control loop or an iterative search reached its operating point.
Nature notes: hollow markers for the search phase, filled for the hold phase, explained once; the target is
a dashed line with a short label; panels share the time axis.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
t = np.array([0.0, 0.5, 0.88, 1.25, 1.6, 1.95, 2.3, 2.65, 3.0, 3.35, 3.55, 3.75, 3.95, 4.15])
setpoint = np.array([12, 1000, 700, 520, 380, 300, 260, 280, 270, 270, 270, 270, 270, 270.0])
readout = np.array([-26, 7, 4, 0, -5, -9, -13, -12, -14.5, -15, -15, -15, -15, -15.0])
hold_from = 9
target = -15
# -------------------------------------------

fig, (a, b) = plt.subplots(2, 1, figsize=figsize_mm(70, 66), sharex=True, gridspec_kw=dict(hspace=0.12))
step_series(a, t, setpoint, markers="o", hollow_until=hold_from)
a.set_yscale("log"); a.set_ylim(8, 2000); a.set_ylabel("Set point (a.u.)"); log_ticks(a.yaxis)
step_series(b, t, readout, markers="o", hollow_until=hold_from)
b.axhline(target, color="0.4", ls=(0, (3, 2)), lw=0.7)
direct_label(b, 1.0, target, "target", color="0.35", dy=-1.5, va="top")
b.set_ylim(-29, 12); b.set_ylabel("Readout (dB)"); b.set_xlabel("Time (s)")
b2 = b.twinx()
b2.set_ylim(*[10 ** (v / 10) for v in b.get_ylim()]); b2.set_yscale("log")
b2.set_ylabel("Readout (linear)"); b2.tick_params(which="both", direction="in")
b.legend(handles=[mpl.lines.Line2D([], [], ls="none", marker="o", mfc="w", mec="0.45", ms=3, label="Search"),
                  mpl.lines.Line2D([], [], ls="none", marker="o", mfc="k", mec="k", ms=3, label="Hold")],
         loc="upper right")
style_axes(a); style_axes(b)
b.tick_params(axis="y", which="both", right=False)
a.set_xlim(0, 4.4)
export(fig, "L09_step_series")
