"""M05 -- Gridded field with contour lines, stippling where the signal is significant and an outlined region.
Use when: a change or anomaly field on a regular grid (latitude-longitude, x-y stage positions, a parameter
plane) with an ensemble or test behind it; dots mark cells where most members agree / P < 0.05.
Look: open frame-less map axes with degree ticks, diverging map centred at 0 with extend arrows, thin grey
contour lines, black stipple dots, a dashed box for the region analysed elsewhere, colour bar underneath.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.ndimage import gaussian_filter

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(79)
lon = np.linspace(-180, 180, 145); lat = np.linspace(-60, 75, 55)
LON, LAT = np.meshgrid(lon, lat)
field = (1.6 * np.exp(-((LAT - 55) / 18) ** 2) - 0.9 * np.exp(-((LON - 20) / 40) ** 2 - ((LAT - 10) / 15) ** 2)
         + 0.5 * np.sin(np.deg2rad(LON) * 2) * np.cos(np.deg2rad(LAT))
         + gaussian_filter(rng.normal(0, 0.5, LON.shape), 2.0))
agree = np.abs(field) > 0.55
region = (-20, 60, -10, 35)                                    # lon0, lon1, lat0, lat1
# -------------------------------------------
fig, ax = plt.subplots(figsize=figsize_mm(120, 68))
fig.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.08)
pm = ax.pcolormesh(lon, lat, field, cmap=NS_DIV_BR.reversed(), vmin=-1.5, vmax=1.5, shading="auto",
                   rasterized=True)
ax.contour(lon, lat, field, levels=[-1, -0.5, 0.5, 1], colors="0.35", linewidths=0.35)
ax.scatter(LON[agree][::3], LAT[agree][::3], s=0.35, color="0.05", lw=0)
x0, x1, y0, y1 = region
ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec="0.05", lw=0.8, ls=(0, (3, 2))))
ax.text(x1 + 3, y1, "Region R", va="top")
ax.set_xlim(-180, 180); ax.set_ylim(-60, 75); ax.set_aspect("equal")
ax.set_xticks(range(-180, 181, 60), [f"{abs(v)}°{'W' if v < 0 else 'E' if v > 0 else ''}" for v in range(-180, 181, 60)])
ax.set_yticks([-30, 0, 30, 60], ["30° S", "0°", "30° N", "60° N"])
for s in ax.spines.values():
    s.set_visible(True); s.set_linewidth(0.5)
cb = cbar_below(ax, pm, "Change (unit)", size="4%", pad=0.25, extend="both", ticks=[-1.5, -1, -0.5, 0, 0.5, 1, 1.5])
ax.text(1.0, -0.13, "Dots: ≥ 80% of members agree", transform=ax.transAxes, ha="right", color="0.35")
export(fig, "M05_field_stipple")
