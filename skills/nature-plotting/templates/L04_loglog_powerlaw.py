"""L04 -- Log-log scaling with a power-law guide (a) and a ranked spectrum with marked cut-offs (b).
Use when: a quantity follows (or departs from) a power law; eigen / singular-value spectra with a rank cut.
Nature notes: the guide is dashed black with its law next to it; families keep one ordered colour map;
cut-off points are hollow markers labelled with the value they define (leader line if space is tight).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(7)
u = np.logspace(-1.3, 0.5, 40)
levels = np.arange(1, 10)
family = {l: u ** 2 / (1 + (u / (0.25 + 0.03 * l)) ** 2) * 0.35 * (1 + 0.15 * rng.random()) for l in levels}
model = u ** 2 / (1 + (u / 0.6) ** 1.6) * 0.6
k = np.arange(1, 501)
n1 = 7e-3 * np.exp(-k / 700); n2 = 1e-2 * np.exp(-k / 600)
sig1 = np.exp(-(k / 110) ** 1.4); sig2 = np.exp(-(k / 70) ** 1.4)
s1 = np.sqrt(sig1 ** 2 + n1 ** 2); s2 = np.sqrt(sig2 ** 2 + n2 ** 2)
k1 = int(np.argmax(sig1 < n1)) + 1; k2 = int(np.argmax(sig2 < n2)) + 1
# -------------------------------------------

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 52), gridspec_kw=dict(wspace=0.45))
_, col = line_mappable(truncate_cmap(NS_GLACIER, 0.1, 0.8), 1, 9)
a.plot(u, model, color="0.35", lw=1.2, zorder=3)
for l in levels:
    a.plot(u, family[l], color=col(l), lw=0.8, alpha=0.9)
a.plot(u, u ** 2, "k--", lw=0.8)
direct_label(a, 0.16, 0.16 ** 2, r"$\propto x^2$", ha="right", va="bottom", dx=-2, dy=2)
a.set_xscale("log"); a.set_yscale("log"); a.set_ylim(1e-3, 1); log_ticks(a.yaxis)
a.set_xlabel("$x$ (a.u.)"); a.set_ylabel("$y$ (a.u.)")
stats_text(a, ["Model: grey", "Data 1–9: colour"], loc="lower right")

for s, n, c, kc, ty in [(s1, n1, PALETTE["blue"], k1, 0.035), (s2, n2, PALETTE["red"], k2, 0.12)]:
    b.plot(k, s, color=c, lw=1.1)
    b.plot(k, n, color=c, lw=0.8, ls=(0, (3, 1.5)))
    b.plot(kc, s[kc - 1], "o", ms=3.6, mfc="w", mec=c, mew=0.9, zorder=4)
    callout(b, (kc, s[kc - 1]), (700, ty), str(kc), color=c)
b.set_xscale("log"); b.set_yscale("log"); b.set_ylim(1e-3, 1.5); b.set_xlim(1, 2000)
log_ticks(b.yaxis); log_ticks(b.xaxis)
b.set_xlabel("Index $k$"); b.set_ylabel("Normalized value $S_k/S_1$")
from matplotlib.lines import Line2D
b.legend(handles=[Line2D([], [], color="0.3", lw=1.1, label="Data"),
                  Line2D([], [], color="0.3", lw=0.8, ls=(0, (3, 1.5)), label="Noise only")],
         loc="center left", handlelength=1.6)
for ax_, l in ((a, "a"), (b, "b")):
    style_axes(ax_); panel_label(ax_, l, dx=-0.30)
export(fig, "L04_loglog_powerlaw")
