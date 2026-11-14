"""F01 -- A full-page composite (183 x 150 mm): overview schematic on top, three result panels, then a wide
trend panel next to a ranking.
Use when: assembling a main figure. One gridspec in mm-sized figure, one look, one palette, panel letters
in the same position for every panel, subtitles only where they add information.
Look: everything from the other templates combined -- pipeline boxes, soft bars with brackets, density
parity, embedding with labels, scenario fan, dot ranking.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
from nature_schematic import *  # noqa: F401,F403  mm-canvas diagram primitives
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(151)
methods = ["Method A", "Method B", "Method C"]; ns = [412, 412, 405]
succ = [78, 61, 49]; err = [3, 4, 4]
ref = rng.gamma(3, 0.7, 6000) - 1.5; pred = ref + rng.standard_t(4, ref.size) * 0.15
cent = np.array([[0, 0], [3, 1], [1.2, 3.2], [-2.4, 2.2], [-1.8, -2.4]])
emb = np.vstack([rng.multivariate_normal(c, np.eye(2) * 0.35, 400) for c in cent]); lab = np.repeat(range(5), 400)
t = np.arange(0, 101); base = 100 * (1 - np.exp(-t / 30))
runs = base[None, :] * rng.normal(1, 0.12, (200, 1)) + rng.normal(0, 3, (200, t.size)).cumsum(1) * 0.15
entries = [f"Entry {i}" for i in range(1, 11)]; score = np.sort(rng.normal(0.6, 0.1, 10)); half = rng.uniform(0.02, 0.05, 10)
# -------------------------------------------
fig = plt.figure(figsize=figsize_mm(183, 150))
top = fig.add_axes([0, 0.79, 1, 0.21]); canvas(top, 183, 31.5)
steps = [("Collect", "grey"), ("Process", "blue"), ("Model", "purple"), ("Evaluate", "orange")]
for i, (s, c) in enumerate(steps):
    b = pbox(top, 12 + i * 40, 10, 26, 11, s, sub=f"Step {i + 1}", color=c)
    if i:
        arrow(top, (12 + i * 40 - 14, 15.5), (12 + i * 40, 15.5))
cylinder(top, 166, 9, 12, 13, "Store", fc="#F3F3F3")
arrow(top, (12 + 3 * 40 + 26, 15.5), (166, 15.5))
route(top, [(172, 9), (172, 3.5), (25, 3.5), (25, 10)], dashed=True, color="0.35", label_text="Iterate",
      label_side="below")
top.text(1, 30.5, "a", fontsize=8, fontweight="bold", va="top")

gs = fig.add_gridspec(2, 3, left=0.07, right=0.98, top=0.74, bottom=0.07, hspace=0.42, wspace=0.42,
                      height_ratios=[1, 0.9])
b = fig.add_subplot(gs[0, 0]); c = fig.add_subplot(gs[0, 1]); d = fig.add_subplot(gs[0, 2])
e = fig.add_subplot(gs[1, :2]); f = fig.add_subplot(gs[1, 2])

bars(b, range(3), succ, colors=[THEMES["soft"][0], THEMES["soft"][2], THEMES["soft"][2]], err=err, width=0.66)
b.set_xticks(range(3)); n_ticklabels(b, methods, ns); b.tick_params(axis="x", length=0)
sig_bracket(b, 0, 1, 88, "***"); sig_bracket(b, 1, 2, 72, "**")
b.set_ylim(0, 100); b.set_ylabel("Success (%)")

lim = (-1.6, 6)
hb = c.hexbin(ref, pred, gridsize=45, extent=(*lim, *lim), cmap=NS_SEAFLOOR, bins="log", mincnt=1, lw=0)
c.plot(lim, lim, color="0.1", lw=0.5); c.set_xlim(lim); c.set_ylim(lim); c.set_aspect("equal")
c.set_xlabel("Reference (unit)"); c.set_ylabel("Predicted (unit)")
cbar_inset(c, hb, "Count", loc="lower right", width="32%", height="4%", borderpad=1.6)

d.scatter(emb[:, 0], emb[:, 1], s=0.8, c=[EDITORIAL[k] for k in lab], lw=0, rasterized=True)
for k in range(5):
    cx, cy = np.median(emb[lab == k], 0)
    d.text(cx, cy, f"C{k + 1}", ha="center", va="center", fontsize=6,
           bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
d.set_aspect("equal"); d.axis("off")
d.annotate("", xy=(0.18, 0.0), xytext=(0, 0), xycoords="axes fraction",
           arrowprops=dict(arrowstyle="-|>", lw=0.6, color="0.2", mutation_scale=5, shrinkA=0, shrinkB=0))
d.annotate("", xy=(0, 0.18), xytext=(0, 0), xycoords="axes fraction",
           arrowprops=dict(arrowstyle="-|>", lw=0.6, color="0.2", mutation_scale=5, shrinkA=0, shrinkB=0))
d.text(0, -0.03, "Dim 1", transform=d.transAxes, fontsize=6, va="top")
d.text(-0.03, 0, "Dim 2", transform=d.transAxes, fontsize=6, rotation=90, ha="right", va="bottom")

fan(e, t, np.median(runs, 0), [np.percentile(runs, [17, 83], 0), np.percentile(runs, [5, 95], 0)],
    THEMES["fan"][1], label="Ensemble median")
e.plot(t, base, color="0.15", lw=0.7, ls=(0, (4, 2)), label="Reference")
e.set_xlim(0, 100); e.set_ylim(0, 140); e.set_xlabel("Time (unit)"); e.set_ylabel("Quantity (unit)")
e.legend(loc="upper left", ncols=2)

y = np.arange(10)
for yi, s_, h_ in zip(y, score, half):
    col = PALETTE["blue"] if yi == 9 else "0.55"
    f.plot([s_ - h_, s_ + h_], [yi, yi], color=col, lw=0.8); f.plot(s_, yi, "o", color=col, ms=2.6)
f.set_yticks(y, entries); f.tick_params(axis="y", length=0); despine(f, left=True)
f.set_xlabel("Score (95% CI)")
for ax_, l, dx in ((b, "b", -0.36), (c, "c", -0.36), (d, "d", -0.1), (e, "e", -0.14), (f, "f", -0.5)):
    panel_label(ax_, l, dx=dx, dy=1.12)
export(fig, "F01_composite_figure")
