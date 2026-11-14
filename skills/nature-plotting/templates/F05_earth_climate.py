"""F05 -- Main figure for an Earth / climate / environment paper (8 panels, 183 x 165 mm): change map with
significance, scenario projections, units vs a driver, composition over time, distributions by decade,
regional small multiples, direction rose and transitions between land classes.
Use when: a synthesis figure that moves from where (a), to how much and when (b, d, e, f), to who (c) and
what changes into what (g, h).
Layout: map spans two columns of the first row; rows 2 and 3 sit on the shared three-column grid; the small
multiples of f, the polar rose of g and the alluvial diagram of h each fill exactly one grid cell.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
from nature_schematic import *  # noqa: F401,F403  mm-canvas diagram primitives
from nature_layout import Page, columns
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.ndimage import gaussian_filter
from scipy.stats import gaussian_kde

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(505)
lon = np.linspace(-180, 180, 121); lat = np.linspace(-60, 80, 47); LON, LAT = np.meshgrid(lon, lat)
warm = (1.2 + 1.6 * np.clip((LAT - 20) / 60, 0, 1) ** 1.5 + 0.35 * np.sin(np.deg2rad(LON) * 1.5)
        + gaussian_filter(rng.normal(0, 0.6, LON.shape), 2.2))
regions = {"R1": (-120, -70, 25, 50), "R2": (0, 40, 40, 65), "R3": (70, 130, 5, 35)}
yr = np.arange(2020, 2101); u = (yr - 2020) / 80


def ens(rate, spread, n=150, plateau=False):
    base = rate * (1 - np.exp(-3 * u)) if plateau else rate * u
    e = base * (1 + spread * rng.standard_normal((n, 1))) + 0.15 * np.cumsum(rng.normal(0, 0.12, (n, yr.size)), 1)
    return np.median(e, 0), np.percentile(e, [17, 83], 0), np.percentile(e, [5, 95], 0)


S1, S2 = ens(1.0, 0.3, plateau=True), ens(3.2, 0.25)
gdp = 10 ** rng.uniform(2.6, 4.9, 120); pop = rng.lognormal(2, 1.1, 120)
impact = -18 + 5 * np.log10(gdp / 400) + rng.normal(0, 3, 120)
t = np.arange(1990, 2031); v = (t - 1990) / 40
mix = np.array([45 - 25 * v, 25 + 2 * np.sin(4 * v), 5 + 35 / (1 + np.exp(-(v - 0.65) * 10)), 12 + 6 * v])
decades = ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
anoms = [rng.normal(-0.2 + 0.18 * k, 0.45 + 0.03 * k, 400) for k in range(7)]
yrs = np.arange(1960, 2025)
reg_series = [0.02 * (yrs - 1960) * k + 0.3 * np.convolve(rng.normal(0, 1, yrs.size), np.ones(5) / 5, "same")
              for k in (0.6, 0.9, 1.2, 0.8, 1.4, 1.0)]
wind = np.r_[rng.vonmises(np.deg2rad(250), 2.0, 500), rng.vonmises(np.deg2rad(60), 1.2, 180)] % (2 * np.pi)
classes = ["Forest", "Crop", "Urban", "Other"]
flows = [np.array([[520, 90, 20, 30], [10, 380, 60, 20], [0, 0, 120, 0], [25, 40, 15, 150]])]
# -------------------------------------------
pg = Page(183, 165)
cols = columns(12, 178.5, 3, gap=13.5)
wide12 = (cols[0][0], cols[1][0] + cols[1][1] - cols[0][0])
cF = THEMES["fan"]

# a -- map --------------------------------------------------------------------------------------------------
a = pg.ax(wide12[0], 6, wide12[1], 42)
pm = a.pcolormesh(lon, lat, warm, cmap=NS_SUNSET, vmin=0, vmax=4, shading="auto", rasterized=True)
a.contour(lon, lat, warm, levels=[1, 2, 3], colors="0.35", linewidths=0.35)
sig = warm > 1.6
a.scatter(LON[sig][::3], LAT[sig][::3], s=0.25, color="0.1", lw=0)
for nm, (x0, x1, y0, y1) in regions.items():
    a.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec="0.05", lw=0.7, ls=(0, (3, 2))))
    a.text(x0 + 1.5, y1 - 1.5, nm, va="top", ha="left")
a.set_xlim(-180, 180); a.set_ylim(-60, 80)
a.set_xticks(range(-180, 181, 90), ["180° W", "90° W", "0°", "90° E", "180° E"])
a.set_yticks([-30, 0, 30, 60], ["30° S", "0°", "30° N", "60° N"])
cbar_box(a, pm, "Warming (°C)", loc="lower left", width_mm=24, ticks=[0, 2, 4], extend="max")

# b -- projections ------------------------------------------------------------------------------------------
b = pg.ax(cols[2][0], 6, cols[2][1], 42)
fan(b, yr, S1[0], [S1[1], S1[2]], cF[1], label="Scenario 1")
fan(b, yr, S2[0], [S2[1], S2[2]], cF[2], label="Scenario 2")
b.axhline(1.5, color="0.3", lw=0.5, ls=(0, (3, 2))); b.text(2022, 1.62, "1.5 °C", va="bottom", color="0.3")
b.set_xlim(2020, 2100); b.set_ylim(0, 4.6); b.set_xticks([2020, 2060, 2100])
b.set_xlabel("Year"); b.set_ylabel("Warming (°C)")
b.legend(loc="upper left")

# row 2 ----------------------------------------------------------------------------------------------------
c, d, e = pg.row(62, 36, cols)
sc = c.scatter(gdp, impact, s=3 + 30 * (pop / pop.max()) ** 0.6, c=np.log10(pop), cmap=NS_DUSK, lw=0, alpha=0.9)
c.axhline(0, color="0.2", lw=0.6, ls=(0, (3, 2)))
c.set_xscale("log"); c.set_xlim(300, 1.2e5); c.set_ylim(-32, 6)
c.set_xlabel("Income per capita (US$)"); c.set_ylabel("Impact (%)")
stats_text(c, ["$\\rho$ = 0.52, P < 10$^{-8}$"], loc="upper left")
cbar_box(c, sc, "log$_{10}$ population", loc="lower right", width_mm=12)

area_stack(d, t, mix, [PALETTE["grey"], PALETTE["sky"], PALETTE["sage"], PALETTE["ochre"]],
           labels=["Coal", "Gas", "Renew.", "Other"], label_x=2025)
d.set_xlim(1990, 2030); d.set_ylim(0, 110); d.set_xticks([1990, 2010, 2030])
d.set_xlabel("Year"); d.set_ylabel("Supply (EJ)")

grid = np.linspace(-2, 2.6, 300)
rc = n_colors(NS_SUNSET, 7, 0.25, 0.95)
for k, (dec, s_, col) in enumerate(zip(decades, anoms, rc)):
    dens = gaussian_kde(s_)(grid); dens = dens / dens.max() * 0.85
    y0 = k
    gradient_fill(e, grid, y0 + dens, col, alpha=0.75, ymin=y0, zorder=10 - k + 0.1)
    e.plot(grid, y0 + dens, color=darken(col, 0.1), lw=0.7, zorder=10 - k + 0.2)
e.set_yticks(range(7), decades); e.tick_params(axis="y", length=0)
e.set_xlim(-2, 2.6); e.set_ylim(-0.2, 7.0); e.set_xlabel("Anomaly (°C)")
e.axvline(0, color="0.4", lw=0.5, ls=(0, (2, 1.5)))
no_background(e)

# row 3 ----------------------------------------------------------------------------------------------------
fg = pg.grid(cols[0][0], 112, cols[0][1], 36, 2, 3, wgap=1.0, hgap=1.0, sharex=True, sharey=True)
for k, (axk, ser) in enumerate(zip(fg.ravel(), reg_series)):
    axk.plot(yrs, ser, color=PALETTE["brick"], lw=0.6)
    p_ = np.polyfit(yrs, ser, 1); axk.plot(yrs, np.polyval(p_, yrs), color="0.15", lw=0.6, ls=(0, (3, 1.5)))
    axk.text(0.06, 0.92, f"R{k + 1}", transform=axk.transAxes, va="top")
    axk.set_xlim(1960, 2024); axk.set_ylim(-1, 3.4); axk.set_xticks([1970, 2010]); axk.set_yticks([0, 2])
    axk.tick_params(axis="x", labelsize=mpl.rcParams["font.size"])
f_anchor = pg.ax(cols[0][0], 112, cols[0][1], 36, frame=False); f_anchor.axis("off")
f_anchor.text(0.5, -0.17, "Year", transform=f_anchor.transAxes, ha="center", va="top")
f_anchor.text(-0.2, 0.5, "Trend (°C)", transform=f_anchor.transAxes, ha="center", va="center", rotation=90)

gx, gy, gw, gh = cols[1][0], 112, cols[1][1], 36
g = pg.ax(gx + (gw - gh) / 2, gy, gh, gh, frame=False, projection="polar")
bins_ = np.linspace(0, 2 * np.pi, 25); h_, _ = np.histogram(wind, bins_)
g.bar(bins_[:-1], h_, width=np.diff(bins_), align="edge", color=PALETTE["teal"], alpha=0.85, lw=0.3, edgecolor="white")
g.set_theta_zero_location("N"); g.set_theta_direction(-1)
g.set_xticks(np.deg2rad([0, 90, 180, 270]), ["N", "E", "S", "W"])
g.set_yticks([30, 60]); g.set_rlabel_position(135); g.tick_params(axis="y", colors="0.45")
g.grid(color="0.85", lw=0.4); g.spines["polar"].set_linewidth(0.6)
g_anchor = pg.ax(gx, gy, gw, gh, frame=False); g_anchor.axis("off")

hx = pg.ax(cols[2][0] + 3, 112, cols[2][1] - 15, 36, frame=False)
alluvial(hx, [[f"{c_} " for c_ in classes], classes], flows,
         {**{f"{c_} ": col for c_, col in zip(classes, [PALETTE["sage"], PALETTE["ochre"], "0.45", PALETTE["sky"]])},
          **{c_: col for c_, col in zip(classes, [PALETTE["sage"], PALETTE["ochre"], "0.45", PALETTE["sky"]])}},
         stage_titles=["2000", "2020"])

pg.letters([a, b, c, d, e, f_anchor, g_anchor], "abcdefg")
pg.letter(hx, "h", dx=-13)
pg.save("F05_earth_climate")
