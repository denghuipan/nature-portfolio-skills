"""S06 -- Process flow in cross-section: one small drawing per step, arrows between steps, material key.
Use when: fabrication / sample-preparation / protocol steps (Methods, Extended Data).
Nature notes: identical scale and material colours in every step; step number + verb under each drawing;
a single material key instead of labelling every layer in every step.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

W, H = 183, 44
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
MAT = {"Material A": "#9AA3AD", "Material B": "#CFE3F3", "Material C": "#F5DEA8", "Mask": "#3A3F47"}
w, gap, x0, y0 = 27, 9.0, 4, 14

def draw(x, layers, extra=None):
    yy = y0
    for name, h, xs in layers:
        for (a_, b_) in xs:
            ax.add_patch(mpl.patches.Rectangle((x + a_ * w, yy), (b_ - a_) * w, h, fc=MAT[name], ec="0.3", lw=0.4))
        yy += h
    if extra:
        extra(x, yy)

full = [(0, 1)]
steps = [("1  Substrate", [("Material A", 6, full)], None),
         ("2  Deposit", [("Material A", 6, full), ("Material B", 3, full)], None),
         ("3  Coat", [("Material A", 6, full), ("Material B", 3, full), ("Material C", 2.5, full)], None),
         ("4  Expose", [("Material A", 6, full), ("Material B", 3, full), ("Material C", 2.5, full)], "uv"),
         ("5  Develop / etch", [("Material A", 6, full), ("Material B", 3, full), ("Material C", 2.5, [(0.35, 0.65)])], None)]
for k, (name, layers, extra) in enumerate(steps):
    x = x0 + k * (w + gap)
    def uv(xx, top, x=x):
        for xm in (0.0, 0.65):
            ax.add_patch(mpl.patches.Rectangle((x + xm * w, top + 3.0), 0.35 * w, 1.0, fc=MAT["Mask"], ec="none"))
        for xa in np.linspace(x + 3, x + w - 3, 6):
            arrow(ax, (xa, top + 9.5), (xa, top + 4.4), color="#7E5AA6", lw=0.6, head=3)
    draw(x, layers, uv if extra == "uv" else None)
    label(ax, x + w / 2, y0 - 2.5, name, va="top", size=1.0)
    if k < len(steps) - 1:
        arrow(ax, (x + w + 1.2, y0 + 5), (x + w + gap - 1.2, y0 + 5), color="0.4", head=5)
for i, (name, c) in enumerate(MAT.items()):
    xx = 4 + i * 30
    ax.add_patch(mpl.patches.Rectangle((xx, 3), 4, 2.6, fc=c, ec="0.3", lw=0.4))
    label(ax, xx + 5.5, 4.3, name, ha="left", size=0.95)
export(fig, "S06_process_flow", exact=True)
