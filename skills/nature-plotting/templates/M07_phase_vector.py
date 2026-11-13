"""M07 -- Phase (angle) map with a cyclic colour map, and a vector field drawn over a magnitude map.
Use when: (a) any angular quantity (phase, orientation) -- needs a cyclic map whose ends match;
(b) flow / gradient / polarization fields.
Nature notes: a cyclic map with labelled ticks at -pi, 0, pi; streamlines or sparse arrows over a muted
magnitude map; arrow colour that contrasts with the background.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
n = 200
x = np.linspace(-1, 1, n); X, Y = np.meshgrid(x, x)
phase = np.angle((X + 1j * Y - 0.3) * np.conj(X + 1j * Y + 0.35 - 0.2j)) + 2.0 * X
phase = np.angle(np.exp(1j * phase))
U = -Y + 0.3 * X; V = X + 0.2 * Y
mag = np.hypot(U, V)
# -------------------------------------------

fig, (a, b) = plt.subplots(1, 2, figsize=figsize_mm(120, 54), gridspec_kw=dict(wspace=0.85))
im = a.imshow(phase, extent=(-1, 1, -1, 1), origin="lower", cmap=NS_PHASE, vmin=-np.pi, vmax=np.pi)
cb = cbar_side(a, im, "Phase (rad)", ticks=[-np.pi, 0, np.pi])
cb.ax.set_yticklabels(["−π", "0", "π"])
a.set_xlabel("$x$ (unit)"); a.set_ylabel("$y$ (unit)")
im2 = b.imshow(mag, extent=(-1, 1, -1, 1), origin="lower", cmap=truncate_cmap(NS_GRAYS, 0.0, 0.55))
b.streamplot(x, x, U, V, color=PALETTE["red"], linewidth=0.5, density=0.9, arrowsize=0.5)
cbar_side(b, im2, "|v| (unit)")
b.set_xlabel("$x$ (unit)"); b.set_ylabel("$y$ (unit)")
for ax_, l in ((a, "a"), (b, "b")):
    style_axes(ax_); panel_label(ax_, l, dx=-0.32)
export(fig, "M07_phase_vector")
