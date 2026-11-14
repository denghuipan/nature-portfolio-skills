"""T08 -- A continuous trace above an aligned event raster and a categorical state ribbon.
Use when: a signal is recorded together with discrete events (spikes, detections, transactions) for several
units and a behavioural / operating state; readers compare all three on one time axis.
Look: three stacked strips sharing x, no frame on the raster and ribbon, scale bars instead of axes on the
trace, state colours keyed directly above the ribbon.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(3)
T = 60.0
t = np.linspace(0, T, 3000)
states = [(0, 12, 0), (12, 27, 1), (27, 40, 2), (40, 52, 1), (52, 60, 0)]       # (start, end, state)
state_names = ["State 1", "State 2", "State 3"]
gain = np.zeros_like(t)
for s0, s1, k in states:
    gain[(t >= s0) & (t < s1)] = [0.2, 0.8, 1.4][k]
trace = np.convolve(rng.normal(0, 1, t.size), np.ones(25) / 25, mode="same") * 4 + gain
units = []
for u in range(14):
    rate = rng.uniform(0.3, 1.6)
    ev = np.sort(rng.uniform(0, T, rng.poisson(rate * T * 2)))
    keep = rng.random(ev.size) < np.interp(ev, t, 0.25 + 0.5 * gain)
    units.append(ev[keep])
# -------------------------------------------
scol = [PALETTE["lightgrey"], PALETTE["sky"], PALETTE["ochre"]]
fig = plt.figure(figsize=figsize_mm(120, 70))
gs = fig.add_gridspec(3, 1, height_ratios=[1.3, 2.0, 0.22], hspace=0.12, left=0.1, right=0.97, top=0.9, bottom=0.05)
a0, a1, a2 = (fig.add_subplot(gs[i]) for i in range(3))
a0.plot(t, trace, color=PALETTE["ink"], lw=0.6)
a0.set_xlim(0, T); a0.axis("off")
a0.plot([0, 5], [-3.2, -3.2], color="0.1", lw=1.0, solid_capstyle="butt")
a0.text(2.5, -3.5, "5 s", ha="center", va="top", fontsize=6)
a0.plot([-0.6, -0.6], [1.5, 2.5], color="0.1", lw=1.0, clip_on=False)
a0.text(-1.0, 2.0, "1 unit", rotation=90, ha="right", va="center", fontsize=6)
a0.text(0.0, 1.08, "Signal", transform=a0.transAxes, fontsize=6, color="0.3")
for i, ev in enumerate(units):
    a1.vlines(ev, i + 0.15, i + 0.85, color="0.15", lw=0.45)
a1.set_xlim(0, T); a1.set_ylim(len(units), 0)
a1.set_yticks([0.5, len(units) - 0.5], ["1", str(len(units))]); a1.set_ylabel("Unit", labelpad=1)
despine(a1, bottom=True); a1.tick_params(labelbottom=False)
for s0, s1, k in states:
    a2.axvspan(s0, s1, color=scol[k], lw=0)
a2.set_xlim(0, T); a2.axis("off")
for k, nm in enumerate(state_names):
    a2.text(0.62 + 0.13 * k, -0.9, "■ " + nm, transform=a2.transAxes, color=darken(scol[k], 0.1), fontsize=6,
            ha="left", va="center")
export(fig, "T08_trace_state_raster")
