"""G01 -- Alluvial diagram: how items move between categories across three stages.
Use when: the same population is classified at several stages (screening -> assignment -> outcome; class at
time 1 -> time 2 -> time 3) and the transitions matter more than the totals.
Look: no axes, node bars proportional to counts, ribbons in the source colour at low opacity, node names and
counts outside the first and last stages, stage titles on top.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
stages = [["Source 1", "Source 2", "Source 3"],
          ["Class A", "Class B", "Class C", "Class D"],
          ["Outcome 1", "Outcome 2"]]
flows = [np.array([[420, 120, 60, 20],
                   [80, 260, 90, 30],
                   [10, 40, 150, 120]]),
         np.array([[430, 80], [300, 120], [130, 170], [40, 130]])]
# -------------------------------------------
colors = {"Source 1": PALETTE["blue"], "Source 2": PALETTE["teal"], "Source 3": PALETTE["ochre"],
          "Class A": "0.55", "Class B": "0.55", "Class C": "0.55", "Class D": "0.55",
          "Outcome 1": PALETTE["sage"], "Outcome 2": PALETTE["brick"]}
fig, ax = plt.subplots(figsize=figsize_mm(110, 64))
fig.subplots_adjust(left=0.15, right=0.83, bottom=0.02, top=0.92)
alluvial(ax, stages, flows, colors, label_fmt="{name} ({value:,.0f})", stage_titles=["Stage 1", "Stage 2", "Stage 3"])
export(fig, "G01_alluvial")
