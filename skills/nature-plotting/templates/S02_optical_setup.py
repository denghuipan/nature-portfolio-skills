"""S02 -- Optical set-up in line art: source, beam splitter, sample and reference arms, two detectors and
data acquisition.
Use when: Methods or Extended Data set-up figures; also as panel a of a results figure.
Nature notes: grey component boxes, one coloured beam, black signal arrows; label every component once,
above or below it, never on the beam.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from nature_schematic import *  # noqa: F401,F403

W, H = 183, 60
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
yb = 40
src = box(ax, 3, yb - 6, 22, 12, "Light source")
beam(ax, [(25, yb), (60, yb), (60, 14), (96, 14)])
beam(ax, [(60, yb), (130, yb)])
lens(ax, 36, yb, 7, w=1.4); label(ax, 36, yb + 5, "L1", va="bottom", color="0.35")
beamsplitter(ax, 60, yb, 4, label_text="BS", label_below=False)
mirror(ax, 60, 14, L=5, angle=135)
label(ax, 56, 10, "M1", color="0.35")
samp = box(ax, 76, yb - 5, 14, 10, "Sample", fc="#F4F4F4")
lens(ax, 104, yb, 7, w=1.4); label(ax, 104, yb + 5, "L2", va="bottom", color="0.35")
cone(ax, (104, yb), (118, yb), 2.6)
det1 = camera(ax, 120, yb - 4.5, 11, 9, label_text="Detector 1")
nd_filter(ax, 78, 14, h=6, label_text="Attenuator")
det2 = camera(ax, 98, 9.5, 11, 9, label_text=None)
label(ax, 103.5, 20, "Detector 2", va="bottom")
daq = box(ax, 146, 20, 24, 12, "Acquisition", "PC")
elbow(ax, [det1.r, (140, det1.r[1]), (140, 30), (146, 30)])
elbow(ax, [det2.r, (140, det2.r[1]), (140, 22), (146, 22)])
label(ax, 75, 52, "sample arm", color="0.45", size=0.95)
label(ax, 78, 4, "reference arm", color="0.45", size=0.95)
export(fig, "S02_optical_setup", exact=True)
