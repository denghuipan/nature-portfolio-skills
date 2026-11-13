"""F01 -- A complete double-column composite figure (183 mm wide, <= 170 mm tall): schematic on top,
five data panels below, aligned frames, lowercase bold panel letters, exact-size export.
Use when: assembling a main figure. Start from this layout, swap in the panel builders you need.
Nature notes: one figure = one claim; the schematic takes the top band; frames align on a common grid;
letters a-f in reading order at the same offset from every frame; save at the exact canvas size so the PDF
is 183 mm wide.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

rng = np.random.default_rng(71)
fig = plt.figure(figsize=figsize_mm(183, 128))
gs = fig.add_gridspec(3, 3, height_ratios=[0.5, 1, 1], left=0.07, right=0.93, bottom=0.07, top=0.97,
                      hspace=0.62, wspace=0.42)

# a -- schematic band (mm canvas inside the top row)
a = fig.add_subplot(gs[0, :])
pa = a.get_position()
aw, ah = pa.width * 183, pa.height * 128                  # band size in mm -> 1 data unit = 1 mm
canvas(a, aw, ah)
bw, by, bh = 28, ah * 0.06, ah * 0.6
xs = np.linspace(2, aw - bw - 10, 4)
b1 = box(a, xs[0], by, bw, bh, "Input", "Data 1–3")
b2 = box(a, xs[1], by, bw, bh, "Process A")
b3 = box(a, xs[2], by, bw, bh, "Process B")
b4 = box(a, xs[3], by, bw + 8, bh, "Output", fc="#FBE3E2", ec=PALETTE["red"])
for p_, q_ in [(b1, b2), (b2, b3), (b3, b4)]:
    arrow(a, p_.r, q_.l, head=6, lw=1.2, color="0.35")
section_header(a, xs[0], xs[2] + bw, by + bh + 2.2, "Stage 1")
section_header(a, xs[3], xs[3] + bw + 8, by + bh + 2.2, "Stage 2")

# b -- two series with a regime
b = fig.add_subplot(gs[1, 0])
x = np.linspace(0, 10, 15)
d1 = 5e-4 * (1 + 10 ** ((x - 5) / 2.6)); d2 = 7e-4 * (1 + 10 ** ((x - 6.5) / 1.0))
b.plot(x, d1, "-o", color=PALETTE["blue"], ms=2.6, mec="w", mew=0.3)
b.plot(x, d2, "-s", color=PALETTE["red"], ms=2.4, mec="w", mew=0.3)
b.set_yscale("log"); b.set_ylim(2e-4, 3); log_ticks(b.yaxis)
regime(b, 7.2, 10, color=PALETTE["red"], alpha=(0, 0.16)); ref_line(b, 7.2, "x", None)
direct_label(b, 8.3, 0.3, "Data 2", color=PALETTE["red"], ha="right")
direct_label(b, 9.7, 3.5e-3, "Data 1", color=PALETTE["blue"], ha="right", va="top")
b.set_xlabel("Variable $x$ (unit)"); b.set_ylabel("Error (a.u.)")

# c -- distributions
c = fig.add_subplot(gs[1, 1])
data = [np.abs(rng.normal(m, 0.05, 120)) for m in (0.10, 0.12, 0.16)]
cols = [PALETTE["blue"], PALETTE["green"], PALETTE["red"]]
boxplot(c, data, [1, 2, 3], cols, alpha=0.45)
for p, d, col in zip([1, 2, 3], data, cols):
    jitter(c, p, d, col, size=3, alpha=0.35, hollow=True)
c.set_xticks([1, 2, 3], ["G1", "G2", "G3"]); c.set_ylabel("Value (unit)")
c.tick_params(axis="x", which="both", bottom=False, top=False)

# d -- heat map with colour bar
d = fig.add_subplot(gs[1, 2])
Z = 10 ** (rng.normal(-3, 0.3, (5, 6)) + np.linspace(0, 1.5, 5)[:, None])
m = heatmap(d, Z, [f"S{i}" for i in range(1, 7)], [f"C{i}" for i in range(1, 6)], cmap=NS_REDS,
            norm=mpl.colors.LogNorm(1e-4, 1e-1))
cbar_side(d, m, "Error", ticks=[1e-4, 1e-3, 1e-2, 1e-1])

# e -- parity
e = fig.add_subplot(gs[2, 0])
t = rng.uniform(0, 10, 400); pr = t + rng.normal(0, 0.3, t.size)
parity(e, t, pr, tol=0.5, s=3, stats_loc="upper left")
e.set_xlabel("True (unit)"); e.set_ylabel("Predicted (unit)")

# f -- offset curves spanning two columns
f = fig.add_subplot(gs[2, 1:])
xx = np.linspace(0, 100, 600)
curves = [np.exp(-((xx - 30 - 8 * k) / 9) ** 2) + 0.5 * np.exp(-((xx - 70 + 4 * k) / 5) ** 2) for k in range(4)]
ridgeline(f, xx, curves, n_colors(truncate_cmap(NS_GLACIER, 0.1, 0.7), 4), offset=0.9, fill="gradient",
          labels_left=[f"Data {k + 1}" for k in range(4)])
f.set_yticks([]); f.set_xlim(0, 100); f.set_ylim(-0.05, 0.9 * 3 + 1.6); f.set_xlabel("Variable $x$ (unit)")
f.tick_params(axis="y", which="both", left=False, right=False)

for ax_ in (b, c, e, f):
    style_axes(ax_)
f.tick_params(axis="y", which="both", left=False, right=False)
c.tick_params(axis="x", which="both", bottom=False, top=False)
# panel letters: same offset (mm) from every frame
W, H = (v * 25.4 for v in fig.get_size_inches())
for ax_, l in zip((a, b, c, d, e, f), "abcdef"):
    p = ax_.get_position()
    fig.text(p.x0 - (9 if l != "a" else 2) / W, p.y1 + 2.5 / H, l, fontsize=8, fontweight="bold", va="top", ha="left")
export(fig, "F01_composite_figure", exact=True)
