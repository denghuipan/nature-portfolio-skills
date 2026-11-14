"""T07 -- Long time series with raw values, a smoothed trend, a shaded period and labelled events.
Use when: daily / hourly records where single values are noisy, an intervention or season is marked, and a
few dated events need names.
Look: grid look (faint horizontal rules), raw values as light thin line, rolling mean in the main colour,
shaded window labelled at its top, event ticks with short labels above the plot area.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
set_look("grid")

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(5)
d = np.arange(0, 365)
y = 50 + 12 * np.sin(2 * np.pi * (d - 80) / 365) + rng.normal(0, 6, d.size)
y[150:210] -= np.linspace(0, 14, 60)                      # response during the window
y[210:] -= 14 * np.exp(-(d[210:] - 210) / 40)
roll = np.convolve(y, np.ones(14) / 14, mode="same")
window = (150, 210)
events = {38: "Event 1", 150: "Start", 210: "End", 300: "Event 2"}
# -------------------------------------------
c = PALETTE["teal"]
fig, ax = plt.subplots(figsize=figsize_2col(52))
fig.subplots_adjust(left=0.07, right=0.98, bottom=0.2, top=0.82)
regime(ax, *window, color=PALETTE["plum"], fade="up", alpha=(0.0, 0.22), zorder=0)
ax.text(np.mean(window), 78, "Intervention window", ha="center", va="top", color="0.3")
ax.plot(d, y, color=lighten(c, 0.55), lw=0.5, zorder=2, label="Daily value")
ax.plot(d[7:-7], roll[7:-7], color=c, lw=1.3, zorder=3, label="14-day mean")
gradient_fill(ax, d[7:-7], roll[7:-7], c, alpha=0.35, ymin=20, zorder=1)
for x, lab in events.items():
    ax.annotate(lab, (x, 1.0), xycoords=("data", "axes fraction"), xytext=(0, 6), textcoords="offset points",
                ha="center", va="bottom", color="0.25",
                arrowprops=dict(arrowstyle="-", lw=0.5, color="0.4", shrinkA=0, shrinkB=0))
ax.set_xlim(0, 364); ax.set_ylim(20, 80)
months = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30])
ax.set_xticks(months, ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_ylabel("Measured value (unit)")
ax.legend(loc="lower left", ncols=2)
export(fig, "T07_events_timeseries")
