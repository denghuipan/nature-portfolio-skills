"""S01 -- Two-stage workflow chart with icons (sample -> instrument -> raw data | processing -> model -> result).
Use when: a Fig. 1-style 'how the study works' schematic: what goes in, what happens, what comes out.
Nature notes: drawn in matplotlib on a mm canvas so fonts and line weights match the data panels and stay
vector; grey arrows inside a stage, coloured arrows across the stage boundary; icons simple and generic.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

W, H = 183, 64
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
section_header(ax, 3, 100, 55, "Stage 1  Data acquisition")
section_header(ax, 106, 180, 55, "Stage 2  Analysis")
divider(ax, 103, 3, 61)
rng = np.random.default_rng(5)

# sample (isometric blocks)
label(ax, 16, 48, "Sample", size=1.1)
for k, col in enumerate([PALETTE["lightblue"], PALETTE["sand"], PALETTE["rose"]]):
    iso_block(ax, 0, 0, 4.2 * k, 12, 10, 3.6, color=col, ox=7, oy=14)
arrow(ax, (30, 27), (37, 27), head=6, lw=1.5, color="0.35")

# instrument
inst = box(ax, 38, 19, 20, 16, "Instrument", "settings")
label(ax, 48, 48, "Measure", size=1.1)
arrow(ax, (59, 27), (66, 27), head=6, lw=1.5, color="0.35")

# raw data traces
label(ax, 82, 48, "Raw data", size=1.1)
t = np.linspace(0, 1, 200)
for k, cy in enumerate([33, 19, 5]):
    y = np.sin(2 * np.pi * (2 + k) * t) * np.exp(-t * (1 + k)) + 0.25 * rng.normal(size=t.size) + 1.4
    mini_plot(ax, 68, cy, 28, 10, t, y, color="0.35", fill=False, lw=0.6)

arrow(ax, (99, 27), (110, 27), head=6, lw=1.8, color=PALETTE["red"])

# processing steps
label(ax, 122, 48, "Pre-processing", size=1.1)
prev = None
for k, name in enumerate(["Filter", "Normalize", "Segment"]):
    b = box(ax, 112, 36 - 12 * k, 20, 8, name, fc="#F4F4F4")
    if prev:
        arrow(ax, prev.b, b.t, head=4, lw=0.7, color="0.45")
    prev = b
arrow(ax, (133, 27), (139, 27), head=6, lw=1.5, color="0.35")

# model
label(ax, 150, 48, "Model", size=1.1)
nn_diagram(ax, 141, 12, 18, 30, layers=(4, 6, 6, 3))
arrow(ax, (161, 27), (166, 27), head=6, lw=1.8, color=PALETTE["blue"])

# result (bar icon)
label(ax, 174, 48, "Result", size=1.1)
ax.add_patch(mpl.patches.Rectangle((167, 14), 13, 26, fc="none", ec="k", lw=0.5))
for k, (h, c) in enumerate([(8, "0.7"), (14, "0.7"), (22, PALETTE["red"])]):
    ax.add_patch(mpl.patches.Rectangle((168.5 + 4 * k, 14), 2.8, h, fc=c, ec="none"))
export(fig, "S01_flowchart", exact=True)
