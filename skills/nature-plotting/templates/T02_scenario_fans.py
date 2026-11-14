"""T02 -- Scenario fans: central estimate with nested uncertainty bands, plus regional small multiples.
Use when: projections under two or more scenarios, each with a spread from an ensemble (models, bootstrap,
Monte Carlo), and the date / value where the scenarios separate matters.
Look: open axes, bands at two percentile levels (darker = narrower), flat reference line, dashed vertical
markers for the divergence point, one large global panel above a 3 x 3 grid that shares both axes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(11)
t = np.arange(2020, 2101)
u = (t - t[0]) / (t[-1] - t[0])


def scenario(rate, spread, plateau=False, n=200, k=1.0):
    base = -rate * (1 - np.exp(-4 * u)) if plateau else -rate * u
    ens = base[None, :] * k * (1 + spread * rng.standard_normal((n, 1))) + \
        0.8 * np.cumsum(rng.normal(0, 0.25, (n, t.size)), axis=1) * u
    return np.median(ens, 0), np.percentile(ens, [17, 83], 0), np.percentile(ens, [5, 95], 0)


S1 = scenario(18, 0.35, plateau=True)          # Scenario 1 (low)
S2 = scenario(62, 0.30)                        # Scenario 2 (high)
ref = -2.5 * (1 - np.exp(-6 * u))              # flat reference (e.g. cost of an intervention)
regions = [f"Region {i}" for i in range(1, 10)]
kreg = rng.uniform(0.4, 1.25, 9)
div = [2049, 2050]                             # divergence at two significance levels
# -------------------------------------------
cs, cm, cr = THEMES["fan"][1], THEMES["fan"][2], THEMES["fan"][0]
fig = plt.figure(figsize=figsize_mm(89, 150))
top = fig.add_gridspec(1, 1, left=0.17, right=0.97, top=0.97, bottom=0.53)
grid = fig.add_gridspec(3, 3, left=0.17, right=0.97, top=0.44, bottom=0.06, hspace=0.42, wspace=0.12)

ax = fig.add_subplot(top[0])
ax.axhline(0, color="0.2", lw=0.6, zorder=1)
ax.plot(t, ref, color=cr, lw=1.0, label="Reference cost")
fan(ax, t, S1[0], [S1[1], S1[2]], cs, label="Scenario 1")
fan(ax, t, S2[0], [S2[1], S2[2]], cm, label="Scenario 2")
for d in div:
    ax.axvline(d, color="0.15", ls=(0, (3, 2)), lw=0.6)
ax.plot([], [], color="0.15", ls=(0, (3, 2)), lw=0.6, label="Divergence year (5%, 1% levels)")
ax.set_xlim(2020, 2100); ax.set_ylim(-80, 32)
ax.set_ylabel("Change relative to baseline (%)")
ax.set_xlabel("Year")
ax.legend(loc="upper right", handlelength=1.6)
subtitle(ax, "All regions")
panel_label(ax, "a", dx=-0.2, dy=1.06)

axes = []
for i, name in enumerate(regions):
    a = fig.add_subplot(grid[i // 3, i % 3], sharex=axes[0] if axes else None, sharey=axes[0] if axes else None)
    axes.append(a)
    a.axhline(0, color="0.2", lw=0.5)
    s1 = [S1[0] * kreg[i], S1[1] * kreg[i], S1[2] * kreg[i]]
    s2 = [S2[0] * kreg[i], S2[1] * kreg[i], S2[2] * kreg[i]]
    fan(a, t, s1[0], [s1[1], s1[2]], cs, lw=0.8)
    fan(a, t, s2[0], [s2[1], s2[2]], cm, lw=0.8)
    d = 2040 + int(30 * (1.3 - kreg[i]))
    a.axvline(d, color="0.15", ls=(0, (3, 2)), lw=0.5)
    subtitle(a, name, pad=2)
    a.set_xlim(2020, 2100); a.set_ylim(-75, 25)
    a.set_xticks([2040, 2080]); a.set_yticks([-75, -50, -25, 0, 25])
    if i % 3:
        a.tick_params(labelleft=False)
    if i < 6:
        a.tick_params(labelbottom=False)
share_labels(fig, axes, xlabel="Year", ylabel="Change relative to baseline (%)")
panel_label(axes[0], "b", dx=-0.62, dy=1.25)
export(fig, "T02_scenario_fans")
