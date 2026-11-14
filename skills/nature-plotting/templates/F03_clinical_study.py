"""F03 -- Main figure for a clinical / biomedical study (7 panels, 183 x 170 mm): study design, group
distributions, dose-response, time course, differential screen, survival with numbers at risk, subgroup forest.
Use when: the results figure of a trial, cohort or animal study; design first, then primary and secondary
outcomes, then robustness across subgroups.
Layout: nature_layout.Page on a three-column grid; the design schematic spans two columns of the first row,
the forest plot's text columns fill the middle column and its frame sits exactly on the third column.
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
from matplotlib.patches import Polygon as _Poly

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(303)
groups = ["Control", "Low", "High"]
vals = [rng.normal(1.0, 0.25, 90), rng.normal(1.35, 0.3, 90), np.r_[rng.normal(1.6, 0.25, 60), rng.normal(2.3, 0.2, 30)]]
dose = np.logspace(-3, 2, 9)
curves = {"Drug 1": (3, 97, 0.08, 1.1), "Drug 2": (6, 92, 1.4, 1.0)}
reps = {k: [hill(d_, *p) + rng.normal(0, 4, 3) for d_ in dose] for k, p in curves.items()}
days = np.array([0, 7, 14, 21, 28])
ctrl = np.array([rng.normal(100 + 7 * d_, 8 + d_ * 0.6, 8) for d_ in days])
trt = np.array([rng.normal(100 + 7 * d_ - (3.4 * (d_ - 7) if d_ > 7 else 0), 8 + d_ * 0.5, 8) for d_ in days])
eff = rng.normal(0, 0.7, 4000); eff[:90] += rng.choice([-1, 1], 90) * rng.uniform(1.2, 3.0, 90)
pv = np.clip(2 * (1 - 0.5 * (1 + np.tanh(np.abs(eff) / 0.35 * 0.8 + rng.normal(0, 0.8, eff.size)))), 1e-25, 1)


def arm(n, scale):
    te = rng.weibull(1.3, n) * scale; tc = rng.uniform(10, 60, n)
    return np.minimum(te, tc), (te <= tc).astype(int)


arms = [arm(200, 42), arm(200, 27)]
sub = [("Age < 65", 512, 0.71, 0.55, 0.92), ("Age ≥ 65", 288, 0.84, 0.62, 1.13), ("Female", 395, 0.69, 0.52, 0.91),
       ("Male", 405, 0.82, 0.63, 1.06), ("Stage I–II", 466, 0.74, 0.58, 0.95), ("Stage III", 334, 0.80, 0.60, 1.07)]
pooled = (800, 0.76, 0.65, 0.89)
# -------------------------------------------
pg = Page(183, 170)
cols = columns(14, 178.5, 3, gap=13.5)
cA, cB = PALETTE["blue"], PALETTE["ochre"]

# a -- study design (spans columns 1-2) ------------------------------------------------------------
a = pg.canvas(0, 1, cols[1][0] + cols[1][1] + 2, 41)
for i in range(3):
    for j in range(3):
        icon_person(a, 4 + i * 4.3, 13 + j * 6.4, h=4.8, color=PASTEL["grey"][1] if (i + j) % 4 else "#C9C9C9")
label(a, 8.3, 10.5, "n = 1,830", va="top")
arrow(a, (17.5, 22.5), (23, 22.5))
b0 = pbox(a, 23, 17, 18, 11, "Enrolled", sub="n = 800")
circle_node(a, 46, 22.5, 2.2, "R")
arrow(a, b0.r, (43.8, 22.5))
for k, (nm, col, y) in enumerate((("Arm A", "blue", 28), ("Arm B", "orange", 8))):
    pbox(a, 53, y, 20, 9, nm, sub="n = 400", color=col)
    route(a, [(48.2, 22.5), (50.5, 22.5), (50.5, y + 4.5), (53, y + 4.5)], radius=0.8)
x0, x1 = 99, 119
tx = lambda w: x0 + (x1 - x0) * w / 52
timeline(a, x0, x1, 33, [tx(v) for v in (0, 12, 24, 52)], ["0", "12", "24", "52"], above=True)
label(a, x0, 38.5, "Week", ha="left", color="0.35")
for i, (m, wk) in enumerate((("Measure 1", (0, 12, 24, 52)), ("Measure 2", (0, 24, 52)), ("End point", (52,)))):
    y = 25 - i * 6
    label(a, x0 - 1.5, y, m, ha="right")
    a.plot([x0, x1], [y, y], color="0.85", lw=0.5)
    for w in (0, 12, 24, 52):
        a.plot(tx(w), y, "o", ms=2.8, mfc=PASTEL["purple"][1] if w in wk else "white",
               mec=PASTEL["purple"][1] if w in wk else "0.7", mew=0.6)
pg.letter(a, "a")

# b -- distributions (column 3, first row) -------------------------------------------------------------
b = pg.ax(cols[2][0], 6, cols[2][1], 32)
gc = ["0.6", lighten(cA, 0.2), cA]
vp = b.violinplot(vals, positions=range(3), widths=0.78, showextrema=False)
for body, col in zip(vp["bodies"], gc):
    body.set_facecolor(lighten(col, 0.55)); body.set_edgecolor("none"); body.set_alpha(1)
for i, (v, col) in enumerate(zip(vals, gc)):
    jitter(b, i, v, darken(col, 0.1), width=0.06, size=2, alpha=0.35)
    q1, md, q3 = np.percentile(v, [25, 50, 75])
    b.plot([i, i], [q1, q3], color="0.15", lw=2.4, solid_capstyle="butt")
    b.plot(i, md, "o", ms=2.2, color="white")
sig_bracket(b, 0, 1, 2.35, "**"); sig_bracket(b, 0, 2, 2.85, "***")
b.set_xticks(range(3)); n_ticklabels(b, groups, [len(v) for v in vals]); b.tick_params(axis="x", length=0)
b.set_ylim(0, 3.3); b.set_ylabel("Biomarker (a.u.)")

# row 2 ------------------------------------------------------------------------------------------------------
c, d, e = pg.row(54, 36, cols)
xx = np.logspace(-3.3, 2.3, 200)
for (nm, r), col, mk in zip(reps.items(), (cA, cB), ("o", "s")):
    mean_sem(c, dose, r, col, marker=mk, line=False, ms=2.8, mfc="white" if mk == "s" else col, mew=0.7)
    p = fit_hill(dose, [np.mean(v) for v in r])
    c.plot(xx, hill(xx, *p), color=col, lw=0.9, label=f"{nm} (EC$_{{50}}$ {p[2]:.2g} µM)")
    c.plot([p[2]] * 2, [-5, hill(p[2], *p)], color=col, lw=0.5, ls=(0, (3, 2)))
c.set_xscale("log"); c.set_xlim(5e-4, 2e2); c.set_ylim(-5, 135); c.set_yticks([0, 50, 100])
c.set_xticks([1e-3, 1e-1, 1e1]); c.xaxis.set_minor_locator(mticker.NullLocator())
c.set_xlabel("Concentration (µM)"); c.set_ylabel("Response (%)")
c.legend(loc="upper left", handlelength=1.2)

regime(d, 7, 28, color=PALETTE["plum"], fade="up", alpha=(0.0, 0.18))
mean_sem(d, days, ctrl, "0.35", marker="o", mfc="white", label="Vehicle", ms=2.8)
m2, e2 = mean_sem(d, days, trt, cA, marker="o", label="Treated", ms=2.8)
for dd, s_ in zip(days[2:], ("*", "**", "***")):
    d.text(dd, max(ctrl[list(days).index(dd)].mean(), m2[list(days).index(dd)]) + 22, s_, ha="center")
d.set_xticks(days); d.set_xlim(-2, 30); d.set_ylim(60, 360)
d.set_xlabel("Day"); d.set_ylabel("Volume (mm$^3$)")
d.legend(loc="upper left")
d.text(17.5, 75, "Dosing", ha="center", color=darken(PALETTE["plum"], 0.2))

up, dn = volcano(e, eff, pv, effect_thr=1.0, p_thr=1e-3, s=2)
e.set_xlim(-4, 4); e.set_ylim(0, None)
e.set_xlabel("log$_2$ fold change"); e.set_ylabel("−log$_{10}$ P")
e.text(0.03, 0.97, f"{dn.sum()} down", transform=e.transAxes, va="top", color=THEMES["updown"][1])
e.text(0.97, 0.97, f"{up.sum()} up", transform=e.transAxes, va="top", ha="right", color=THEMES["updown"][0])

# row 3 ------------------------------------------------------------------------------------------------------
f = pg.ax(cols[0][0], 106, cols[0][1], 36)
for (t, ev), col, nm in zip(arms, (cA, cB), ("Arm A", "Arm B")):
    km_curve(f, t, ev, col, label=nm)
f.set_xlim(0, 60); f.set_ylim(0, 1.02); f.set_xticks([0, 20, 40, 60])
f.set_yticks([0, 0.5, 1], ["0", "50", "100"])
f.set_xlabel("Months", labelpad=1); f.set_ylabel("Event-free (%)")
f.legend(loc="upper right")
f.text(0.04, 0.05, "HR 0.62, P < 0.001", transform=f.transAxes)
at_risk_table(f, arms, [0, 20, 40, 60], ["Arm A", "Arm B"], [cA, cB], y0=-0.42, row_h=0.11, title="At risk")

g = pg.ax(cols[2][0], 106, cols[2][1], 36)
t = pg.ax(cols[1][0] - 6, 106, cols[1][1] + 12, 36, frame=False, sharey=g); t.axis("off")
n = len(sub)
for i, (nm, nn, est, lo, hi) in enumerate(sub):
    g.plot([lo, hi], [i, i], color="0.2", lw=0.7)
    g.plot(est, i, "s", color=cA, ms=2.0 + 3.0 * nn / 512, mec="none")
    t.text(0.0, i, nm, va="center"); t.text(0.5, i, f"{nn}", va="center", ha="right")
    t.text(0.56, i, f"{est:.2f} ({lo:.2f}–{hi:.2f})", va="center")
_, pe, plo, phi = pooled
g.add_patch(_Poly([(plo, n + 0.4), (pe, n + 0.05), (phi, n + 0.4), (pe, n + 0.75)], closed=True, color="0.15"))
t.text(0.0, n + 0.4, "Overall", va="center", fontweight="bold"); t.text(0.5, n + 0.4, f"{pooled[0]}", va="center", ha="right")
t.text(0.56, n + 0.4, f"{pe:.2f} ({plo:.2f}–{phi:.2f})", va="center", fontweight="bold")
for xh, lab_, ha in ((0.0, "Subgroup", "left"), (0.5, "n", "right"), (0.56, "HR (95% CI)", "left")):
    t.text(xh, -1.1, lab_, ha=ha, va="center", color="0.35")
t.set_xlim(0, 1)
g.axvline(1, color="0.2", lw=0.6); g.axvline(pe, color="0.45", lw=0.5, ls=(0, (3, 2)))
g.set_xscale("log"); g.set_xlim(0.45, 1.6); g.set_xticks([0.5, 1, 1.5], ["0.5", "1", "1.5"])
g.xaxis.set_minor_locator(mticker.NullLocator())
g.set_ylim(n + 1.0, -1.6); g.set_yticks([])
g.set_xlabel("Hazard ratio")

pg.letters([b, c, d, e, f], "bcdef")
pg.letter(t, "g", dx=-4)                  # same x as every middle-column letter (frame x - 10 mm)
pg.save("F03_clinical_study")
