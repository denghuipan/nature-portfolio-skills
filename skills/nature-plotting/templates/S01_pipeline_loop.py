"""S01 -- Pipeline overview with two parallel branches, a shared evaluation step, a database and a feedback loop.
Use when: Fig. 1a of a methods paper: two ways of generating candidates feed one evaluation, results are stored
and summarised, and the whole thing repeats for several rounds.
Look: white group frames with coloured rounded edges and titles above, small icons inside (cluster, graph),
neutral rounded boxes, a database cylinder, stacked output boxes, a merge circle, dashed loop with its label.
Coordinates are millimetres on the printed page (1 data unit = 1 mm).
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
branches = [("Branch A", "Candidates", "Graph", "Model", "Score"),
            ("Branch B", "Sequences", "Graph", "Model", "Score")]
outputs = ["Output 1", "Output 2 (n = 2.2 million)", "Output 3"]
loop_text = "Repeat for N rounds"
# -------------------------------------------
W, H = 183, 66
fig = plt.figure(figsize=figsize_mm(W, H))
ax = fig.add_axes([0, 0, 1, 1]); canvas(ax, W, H)
rng = np.random.default_rng(3)


def cluster(x, y, n=7, r=1.5, col="#A9A9C9"):
    for k in range(n):
        dx, dy = rng.normal(0, r, 2)
        ax.add_patch(plt.Circle((x + dx, y + dy), 1.25, fc=lighten(col, rng.uniform(0, 0.4)), ec="white", lw=0.3,
                                zorder=3))


merge = circle_node(ax, 14, 33, 2.4)
ys = [46, 12]
for (title, *steps), yb, col in zip(branches, ys, ("blue", "green")):
    fr = group_frame(ax, 24, yb - 6, 62, 15, title, color=col)
    cluster(31, yb + 1.5, col="#A9A9C9" if col == "blue" else "#9CC7A9")
    label(ax, 31, yb - 4.2, steps[0])
    arrow(ax, (37, yb + 1.5), (44, yb + 1.5))
    icon_graph(ax, 45.5, yb - 1.5, 6.0, color=PALETTE["plum"], seed=4)
    label(ax, 48.5, yb - 4.2, steps[1])
    arrow(ax, (53, yb + 1.5), (64, yb + 1.5))
    label(ax, 58.5, yb + 2.6, steps[2], va="bottom")
    label(ax, 70.5, yb + 1.5, steps[3])
    elbow(ax, [(16.4, 33), (19, 33), (19, yb + 1.5), (24, yb + 1.5)])
    elbow(ax, [(76, yb + 1.5), (95, yb + 1.5), (95, 33 + (4 if yb > 33 else -4))])
ev = pbox(ax, 89, 29, 12, 8, "Evaluate", color="grey")
db = cylinder(ax, 108, 26.5, 15, 13, "Data-\nbase", fc="#F3F3F3")
arrow(ax, ev.r, (108, 33))
for i, t in enumerate(outputs):
    b = box(ax, 140, 45 - i * 11, 38, 7.5, t, fc="white", ec="0.35")
    elbow(ax, [(123, 33), (131, 33), (131, b.l[1]), (140, b.l[1])], arrow_end=True)
route(ax, [(115.5, 26.5), (115.5, 3), (14, 3), (14, 30.6)], dashed=True, color="0.25",
      label_text=loop_text, label_side="below", label_at=0.5)
route(ax, [(89, 33), (70.5, 33), (70.5, 44.6)], dashed=True, color="0.25")
label(ax, 80, 33.8, "Feedback", va="bottom", color="0.25")
export(fig, "S01_pipeline_loop")
