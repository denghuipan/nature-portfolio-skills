"""S04 -- Study design: enrolment, allocation into arms, and a visit timeline with the measurements taken.
Use when: Fig. 1 of a clinical, field or longitudinal study (who was included, how they were split, when
each measurement happened); CONSORT details go to the supplement, this is the reader's map.
Look: person glyphs for the cohort, a circled 'R' for randomisation, pastel arm boxes with n, a time axis
with visit ticks, filled markers for the visits where each measurement was taken (one row per measurement).
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
screened, enrolled = 1830, 1240
arms = [("Group A", "Intervention", 620), ("Group B", "Comparator", 620)]
visits = [0, 4, 12, 24, 52]                                   # weeks
measures = {"Measure 1": [0, 4, 12, 24, 52], "Measure 2": [0, 12, 52], "Measure 3": [0, 24, 52],
            "Primary end point": [52]}
# -------------------------------------------
W, H = 183, 64
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
for i in range(4):
    for j in range(3):
        icon_person(ax, 6 + i * 4.2, 38 + j * 6.2, h=4.6, color=PASTEL["grey"][1] if (i + j) % 5 else "#C9C9C9")
label(ax, 12.3, 34.5, f"Screened\nn = {screened:,}", va="top", linespacing=1.15)
arrow(ax, (24, 46), (33, 46))
b0 = pbox(ax, 33, 40, 22, 12, "Enrolled", sub=f"n = {enrolled:,}", color="grey")
r = circle_node(ax, 63, 46, 2.6, "R", fc="white")
arrow(ax, b0.r, (60.4, 46))
arm_boxes = []
for k, ((g, sub, n), c) in enumerate(zip(arms, ("blue", "orange"))):
    y = 53 - k * 15
    bb = pbox(ax, 74, y, 24, 10, g, sub=f"{sub}, n = {n:,}", color=c)
    route(ax, [(65.6, 46), (69, 46), (69, y + 5), (74, y + 5)], radius=1.2)
    arm_boxes.append(bb)
x0, x1 = 110, 172
tx = lambda w: x0 + (x1 - x0) * w / 52
timeline(ax, x0, x1, 46, [tx(v) for v in visits], [str(v) for v in visits], above=True)
label(ax, x1 + 2.5, 46, "Week", ha="left", size=0.95)
ax.add_patch(plt.Rectangle((x0, 39), x1 - x0, 1.3, color=PASTEL["blue"][0], lw=0))
label(ax, x0, 37.6, "Follow-up", ha="left", va="top", size=0.95, color="0.35")
for i, (m, wk) in enumerate(measures.items()):
    y = 28 - i * 6.2
    label(ax, x0 - 2, y, m, ha="right", size=0.95)
    ax.plot([x0, x1], [y, y], color="0.88", lw=0.5)
    for w in visits:
        ax.plot(tx(w), y, "o", ms=3.2, mfc=PASTEL["purple"][1] if w in wk else "white",
                mec=PASTEL["purple"][1] if w in wk else "0.75", mew=0.6)
route(ax, [(98, 58), (103, 58), (103, 46.6), (108, 46.6)], radius=1.0, arrow_end=False)
route(ax, [(98, 43), (103, 43), (103, 46.6), (108, 46.6)], radius=1.0)
label(ax, 2, 62, "a", ha="left", va="top", size=1.33, fontweight="bold")
label(ax, 107, 62, "b", ha="left", va="top", size=1.33, fontweight="bold")
export(fig, "S04_study_design")
