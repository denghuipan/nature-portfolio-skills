"""F04 -- Main figure for an experimental physical-science paper (7 panels, 183 x 160 mm): instrument concept,
measurement vs model with an extrapolation, a mapped field with significance, a distribution with its fit,
raw images, a time-frequency map and an error budget.
Use when: a measurement paper's central figure: how it is measured (a), the headline scaling (b), where the
effect is (c), how reproducible it is (d), what the raw data look like (e, f) and what limits it (g).
Layout: three-column grid; b and c span two columns so their left / right frame edges coincide with the
frames below and above them; colour keys sit inside the frames.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
from nature_schematic import *  # noqa: F401,F403  mm-canvas diagram primitives
from nature_layout import Page, columns, split
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.ndimage import gaussian_filter
from scipy.signal import spectrogram, chirp
from scipy.stats import norm

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(404)
nq = np.arange(12, 54, 3)
model = 0.55 * np.exp(-0.095 * (nq - 8))
d1 = model * np.exp(rng.normal(0, 0.05, nq.size)); d2 = model * np.exp(rng.normal(0, 0.07, nq.size))
ext_x = np.array([56, 62, 68]); ext_m = 0.55 * np.exp(-0.095 * (ext_x - 8)); ext_e = ext_m * np.array([0.3, 0.4, 0.55])
lon = np.linspace(-180, 180, 121); lat = np.linspace(-60, 75, 46); LON, LAT = np.meshgrid(lon, lat)
field = (1.5 * np.exp(-((LAT - 55) / 18) ** 2) - 0.9 * np.exp(-((LON - 20) / 40) ** 2 - ((LAT - 10) / 15) ** 2)
         + 0.45 * np.sin(np.deg2rad(LON) * 2) * np.cos(np.deg2rad(LAT)) + gaussian_filter(rng.normal(0, 0.5, LON.shape), 2))
rep = rng.normal(98.4, 1.1, 2000)
imgs = []
for sd in (1, 2):
    im = np.zeros((120, 120)); r = np.random.default_rng(sd)
    im[r.integers(0, 120, 70), r.integers(0, 120, 70)] = r.uniform(0.5, 1, 70); imgs.append(gaussian_filter(im, 3))
fs_ = 1000.0; tt = np.arange(0, 8, 1 / fs_)
sig = 0.5 * np.sin(2 * np.pi * 8 * tt) + 0.4 * chirp(tt, 15, 8, 120) + 0.3 * rng.normal(0, 1, tt.size)
budget = np.array([[0.62, 0.28, 0.14, 0.07], [0.41, 0.25, 0.12, 0.05], [0.22, 0.19, 0.10, 0.04]])
# -------------------------------------------
C = THEMES["signal"]
pg = Page(183, 160)
cols = columns(12, 178.5, 3, gap=13.5)
wide = (cols[1][0], cols[2][0] + cols[2][1] - cols[1][0])            # columns 2-3
wide12 = (cols[0][0], cols[1][0] + cols[1][1] - cols[0][0])          # columns 1-2

# a -- instrument concept ------------------------------------------------------------------------------------
a = pg.canvas(0, 1, cols[0][0] + cols[0][1] + 2, 47)
pbox(a, 4, 30, 18, 10, "Source", sub="pulsed", color="orange")
icon_cells(a, 31, 29, 16, 12, n=9, color=PASTEL["teal"][1], seed=5)
label(a, 39, 42.5, "Sample (1 mm)", va="bottom")
arrow(a, (22, 35), (31, 35), color=PALETTE["ochre"])
matrix_icon(a, 32, 8, 14, 11, shape=(8, 9), cmap=NS_SEAFLOOR, grid_lw=0.25)
label(a, 39, 5.5, "Detector", va="top")
arrow(a, (39, 29), (39, 20.2), color=PALETTE["ochre"])
mini_plot(a, 5, 8, 16, 11, np.linspace(0, 1, 60), np.exp(-((np.linspace(0, 1, 60) - 0.55) / 0.12) ** 2),
          color=PALETTE["blue"], ticks=0)
label(a, 13, 5.5, "Readout", va="top")
arrow(a, (31.5, 13.5), (21.5, 13.5), color="0.4")
pg.letter(a, "a")

# b -- measurement vs model, with extrapolation (columns 2-3) ----------------------------------------------
b = pg.ax(wide[0], 6, wide[1], 40)
b.axvspan(54, 72, color=PALETTE["sand"], alpha=0.35, lw=0)
b.plot(np.r_[nq, ext_x], np.r_[model, ext_m], color="k", lw=0.9, label="Model")
b.plot(nq, d1, "o", ms=3.6, mfc="none", mec=C[0], mew=0.8, label="Data 1")
b.plot(nq, d2, "x", ms=3.6, color=C[1], mew=0.9, label="Data 2")
b.errorbar(ext_x, ext_m * np.exp(rng.normal(0, 0.05, 3)), yerr=ext_e, fmt="+", ms=4.5, color=C[2], mew=0.9,
           elinewidth=0.7, capsize=1.5, label="Estimate")
for xv, yv, txt in zip(ext_x, ext_m + ext_e, ("2 h", "4 d", "3 yr")):
    arrow_note(b, xv, yv * 7, yv * 1.4, txt, color="0.3")
b.set_yscale("log"); b.set_ylim(2e-4, 1.5); b.set_xlim(10, 72)
b.set_xlabel("System size, $n$"); b.set_ylabel("Score, $S$")
b.text(63, 0.6, "Extrapolated", ha="center", va="center", color="0.35")
legend_box(b, loc="lower left", ncols=4, columnspacing=1.0)

# c -- field map with stippling (columns 1-2) -------------------------------------------------------------------
c = pg.ax(wide12[0], 60, wide12[1], 40)
pm = c.pcolormesh(lon, lat, field, cmap=NS_DIV_BR.reversed(), vmin=-1.5, vmax=1.5, shading="auto", rasterized=True)
c.contour(lon, lat, field, levels=[-1, -0.5, 0.5, 1], colors="0.35", linewidths=0.35)
agree = np.abs(field) > 0.55
c.scatter(LON[agree][::2], LAT[agree][::2], s=0.3, color="0.05", lw=0)
c.add_patch(plt.Rectangle((-20, -10), 80, 45, fill=False, ec="0.05", lw=0.7, ls=(0, (3, 2))))
c.set_xlim(-180, 180); c.set_ylim(-60, 75)
c.set_xticks(range(-180, 181, 90), ["180° W", "90° W", "0°", "90° E", "180° E"])
c.set_yticks([-30, 0, 30, 60], ["30° S", "0°", "30° N", "60° N"])
cbar_box(c, pm, "Change (unit)", loc="lower left", width_mm=24, ticks=[-1.5, 0, 1.5], extend="both")

# d -- reproducibility histogram (column 3) ------------------------------------------------------------------
d = pg.ax(cols[2][0], 60, cols[2][1], 40)
bins = np.linspace(94, 102, 33)
_, _, ph = d.hist(rep, bins=bins, color=PALETTE["blue"], lw=0)
gradient_patches(d, ph, PALETTE["blue"], light=0.8)
mu, sd = norm.fit(rep); xx = np.linspace(94, 102, 300)
d.plot(xx, norm.pdf(xx, mu, sd) * rep.size * np.diff(bins)[0], color=PALETTE["navy"], lw=0.9)
stats_text(d, [f"$\\mu$ = {mu:.1f}%", f"$\\sigma$ = {sd:.1f}%", f"n = {rep.size:,}"], loc="upper left")
d.set_xlim(94, 102); d.set_xlabel("Fidelity (%)"); d.set_ylabel("Count")

# e -- raw images (column 1, 2 x 2) --------------------------------------------------------------------------
eg = pg.grid(cols[0][0], 114, cols[0][1], 36, 2, 2, wgap=1.2, hgap=1.2)
green = np.array(mcolors.to_rgb("#3FBF5F")); magenta = np.array(mcolors.to_rgb("#D24BD2"))
for i in range(2):
    eg[i, 0].imshow(imgs[i] / imgs[i].max(), cmap="gray", aspect="auto")
    mrg = np.clip((imgs[i] / imgs[i].max())[..., None] * green + (imgs[1 - i] / imgs[1 - i].max())[..., None] * magenta, 0, 1)
    eg[i, 1].imshow(mrg, aspect="auto")
    for j in range(2):
        eg[i, j].set_xticks([]); eg[i, j].set_yticks([])
eg[0, 0].set_ylabel("Cond. 1"); eg[1, 0].set_ylabel("Cond. 2")
eg[0, 0].set_title("Channel 1", pad=2); eg[0, 1].set_title("Merge", pad=2)
scale_bar(eg[1, 1], 30, "3 µm", loc="lower right", color="w")
e_anchor = pg.ax(cols[0][0], 114, cols[0][1], 36, frame=False); e_anchor.axis("off")

# f -- time-frequency map (column 2) ---------------------------------------------------------------------------
f = pg.ax(cols[1][0], 114, cols[1][1], 36)
fq, ts, S = spectrogram(sig, fs_, nperseg=512, noverlap=448)
P = 10 * np.log10(S + 1e-12); m = (fq >= 3) & (fq <= 200)
pmf = f.pcolormesh(ts, fq[m], P[m], cmap=NS_GLACIER.reversed(), vmin=np.percentile(P[m], 5),
                   vmax=np.percentile(P[m], 99.5), shading="gouraud", rasterized=True)
f.set_yscale("log"); f.set_ylim(4.5, 200)
f.set_yticks([10, 30, 100], ["10", "30", "100"]); f.yaxis.set_minor_locator(mticker.NullLocator())
f.set_xlabel("Time (s)"); f.set_ylabel("Frequency (Hz)")
cbar_box(f, pmf, "Power (dB)", loc="upper left", width_mm=16, ticks=[-40, -20])

# g -- error budget (column 3) --------------------------------------------------------------------------------
g = pg.ax(cols[2][0], 114, cols[2][1], 36)
pc = [PALETTE["blue"], PALETTE["sky"], PALETTE["teal"], PALETTE["mint"]]
yy = np.arange(3)[::-1]
for row, yv in zip(budget, yy):
    left = 0
    for v, col in zip(row, pc):
        g.barh(yv, v, left=left, height=0.55, color=col, lw=0); left += v
    g.barh(yv, 0.06, left=left, height=0.55, fc="white", ec="0.35", hatch="////", lw=0.5)
    g.text(left + 0.1, yv, f"{left + 0.06:.2f}", va="center")
g.set_yticks(yy, ["Set-up 1", "Set-up 2", "Set-up 3"]); g.tick_params(axis="y", length=0)
g.set_xlim(0, 1.45); g.set_ylim(-0.6, 3.1); g.set_xlabel("Error per step (%)")
square_legend(g, ["A", "B", "C", "D"], pc, loc="upper right", ncols=4, columnspacing=0.6, handletextpad=0.3)

pg.letters([b, c, d, e_anchor, f, g], "bcdefg")
pg.save("F04_measurement_physics")
