"""F02 -- Main figure for a methods paper (7 panels, 183 x 146 mm): overview schematic, benchmark,
scaling, agreement, embedding, error distribution and ranking.
Use when: Fig. 1 or 2 of a computational / methods paper: what the method does (a), that it wins (b, g),
how it scales (c), how accurate it is (d, f) and what it learns (e).
Layout: nature_layout.Page in mm -- one schematic band, then two rows on a shared three-column grid, so
every frame edge lines up; letters 10 mm left and 3 mm above each frame; colour keys inside frames.
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

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(202)
methods = ["Method A", "Method B", "Method C"]
succ = {"Set 1": ([78, 61, 47], [3, 4, 4]), "Set 2": ([66, 40, 35], [4, 5, 5])}
budget = np.unique(np.round(np.logspace(0, 3, 12)))
lb = np.log10(budget)
ref = rng.gamma(3, 0.7, 8000) - 1.5
pred = ref + rng.standard_t(4, ref.size) * 0.13
cent = np.array([[0, 0], [3, 1.2], [1.2, 3.4], [-2.6, 2.3], [-1.9, -2.5], [2.6, -2.2]])
emb = np.vstack([rng.multivariate_normal(c, np.eye(2) * 0.33, 350) for c in cent]); lab = np.repeat(range(6), 350)
errs = {m: rng.lognormal(mu, 0.75, 900) for m, mu in zip(methods, (0.4, 1.0, 1.5))}
entries = [f"Model {i}" for i in range(1, 11)]
score = np.sort(rng.normal(0.62, 0.09, 10)); half = rng.uniform(0.015, 0.04, 10)
# -------------------------------------------
cA, cB, cC = THEMES["soft"][0], THEMES["soft"][2], THEMES["soft"][3]
mcol = [PALETTE["blue"], PALETTE["grey"], "0.75"]
pg = Page(183, 146)
cols = columns(12, 178.5, 3, gap=13.5)

# a -- overview schematic -----------------------------------------------------------------------
a = pg.canvas(0, 1, 183, 31)
fr = group_frame(a, 8, 6, 38, 20, "Inputs", color="green")
icon_cells(a, 11, 9, 14, 13, n=9, color=PASTEL["green"][1], seed=3)
icon_stack(a, 30, 9.5, 10, 12, n=3)
for i, (t, sub, c) in enumerate((("Encoder", "6 blocks", "blue"), ("Core", "24 blocks", "purple"),
                                 ("Decoder", "6 blocks", "blue"))):
    pbox(a, 56 + i * 25, 9, 19, 14, t, sub=sub, color=c)
    if i:
        arrow(a, (56 + i * 25 - 6, 16), (56 + i * 25, 16))
arrow(a, (46, 16), (56, 16))
plus_node(a, 128.5, 16, 1.1)
arrow(a, (125, 16), (127.4, 16)); arrow(a, (129.6, 16), (135, 16))
cylinder(a, 135, 8.5, 13, 15, "Store", fc="#F2F2F2")
icon_bars(a, 157, 15, 11, 9, colors=[PASTEL["orange"][1]] * 3 + [PALETTE["blue"]])
mini_plot(a, 157, 3, 11, 9, np.linspace(0, 1, 40), np.linspace(0, 1, 40) ** 0.5, color=PALETTE["blue"], ticks=0)
route(a, [(148, 18), (152, 18), (152, 19.5), (157, 19.5)], radius=0.8)
route(a, [(148, 13), (152, 13), (152, 7.5), (157, 7.5)], radius=0.8)
label(a, 170, 19.5, "Scores", ha="left"); label(a, 170, 7.5, "Predictions", ha="left")
route(a, [(141.5, 8.5), (141.5, 3), (65.5, 3), (65.5, 9)], dashed=True, color="0.35",
      label_text="Iterative refinement (3 rounds)", label_side="above")
pg.letter(a, "a")

# row 1 ------------------------------------------------------------------------------------------
b, c, d = pg.row(44, 38, cols)
x = np.arange(2)
for k, (m, col) in enumerate(zip(methods, [cA, cB, cC])):
    bars(b, x + (k - 1) * 0.26, [succ[s][0][k] for s in succ], colors=[col, col], err=[succ[s][1][k] for s in succ],
         width=0.24)
sig_bracket(b, -0.26, 0, 88, "***"); sig_bracket(b, 0.74, 1.0, 76, "**")
b.set_xticks(x, list(succ)); b.tick_params(axis="x", length=0)
b.set_ylim(0, 100); b.set_ylabel("Success (%)")
square_legend(b, ["A", "B", "C"], [cA, cB, cC], loc="upper right", ncols=3, columnspacing=0.6,
              handletextpad=0.3)
subtitle(b, "Benchmark (methods A–C)")

for m, col, s0, s1 in ((methods[0], mcol[0], 38, 24), (methods[1], mcol[1], 17, 11)):
    mu = s0 + s1 * (1 - np.exp(-lb / 1.3))
    c.fill_between(budget, mu * 0.8, mu * 1.2, color=col, alpha=0.2, lw=0)
    c.plot(budget, mu, "-o", color=col, ms=2.0, lw=0.8, label=m)
c.set_xscale("log"); c.set_xlim(0.8, 1300); c.set_ylim(0, 80)
c.set_xticks([1, 10, 100, 1000], ["1", "10", "100", "1,000"]); c.xaxis.set_minor_locator(mticker.NullLocator())
c.set_xlabel("Samples per target"); c.set_ylabel("Success (%)")
c.legend(loc="upper left")
subtitle(c, "Scaling")

lim = (-1.6, 6)
hb = d.hexbin(ref, pred, gridsize=40, extent=(*lim, *lim), cmap=NS_SEAFLOOR, bins="log", mincnt=1, lw=0)
d.plot(lim, lim, color="0.1", lw=0.5)
d.set_xlim(lim); d.set_ylim(lim)
d.set_xlabel("Reference (unit)"); d.set_ylabel("Predicted (unit)")
r2 = 1 - np.sum((pred - ref) ** 2) / np.sum((ref - ref.mean()) ** 2)
stats_text(d, [f"$R^2$ = {r2:.3f}", f"n = {ref.size:,}"], loc="upper left")
cbar_box(d, hb, "Count", loc="lower right", width_mm=14)
subtitle(d, "Agreement")

# row 2 ------------------------------------------------------------------------------------------
e, f, g = pg.row(96, 38, cols)
e.scatter(emb[:, 0], emb[:, 1], s=0.7, c=[EDITORIAL[k] for k in lab], lw=0, rasterized=True)
for k in range(6):
    cx, cy = np.median(emb[lab == k], 0)
    e.text(cx, cy, f"C{k + 1}", ha="center", va="center",
           bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
e.set_xticks([]); e.set_yticks([]); e.set_xlabel("Dim 1"); e.set_ylabel("Dim 2")
e.set_xlim(-4.4, 4.6); e.set_ylim(-4.3, 5.0)
subtitle(e, "Learned representation")

for (m, v), col in zip(errs.items(), mcol):
    ecdf(f, v, col, label=m)
    md = np.median(v)
    f.plot([md, md], [0, 0.5], color=col, lw=0.5, ls=(0, (2, 1.5))); f.plot(md, 0.5, "o", color=col, ms=2.2)
f.set_xscale("log"); f.set_xlim(0.2, 60); f.set_ylim(0, 1)
f.set_xticks([1, 10], ["1", "10"]); f.xaxis.set_minor_locator(mticker.NullLocator())
f.set_xlabel("Error (unit)"); f.set_ylabel("Cumulative fraction")
f.legend(loc="lower right")
subtitle(f, "Error distribution")

y = np.arange(10)
for yi, s_, h_ in zip(y, score, half):
    col = PALETTE["blue"] if yi == 9 else "0.55"
    g.plot([s_ - h_, s_ + h_], [yi, yi], color=col, lw=0.8); g.plot(s_, yi, "o", color=col, ms=2.4)
g.axvline(0.6, color="0.35", lw=0.5, ls=(0, (3, 2)))
g.set_yticks(y, entries); g.tick_params(axis="y", length=0); g.set_ylim(-0.7, 9.7)
g.set_xlabel("Score (95% CI)")
subtitle(g, "Ranking")

pg.letters([b, c, d, e, f, g], "bcdefg")
pg.save("F02_method_benchmark")
