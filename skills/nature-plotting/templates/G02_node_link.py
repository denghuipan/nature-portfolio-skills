"""G02 -- Node-link network: node area = size of a unit, edge width = connection strength, a weight key.
Use when: a small network (5-30 nodes) between named modules / regions / groups is the result of an
analysis, and the strongest connections should stand out.
Look: no axes, nodes in their group colours with white rims, grey edges with width on a log scale, a
legend of edge widths with decade values, nodes arranged left / centre / right by role with group brackets.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(131)
pos = {"In 1": (-1.0, 1.4), "In 2": (-0.35, 1.5), "In 3": (0.35, 1.5), "In 4": (1.0, 1.4),
       "Hub L": (-1.55, 0.4), "Core L": (-0.6, 0.35), "Core R": (0.6, 0.35), "Hub R": (1.55, 0.4),
       "Out 1": (-0.9, -0.7), "Out 2": (-0.3, -0.85), "Out 3": (0.3, -0.85), "Out 4": (0.9, -0.7)}
role = {k: (0 if k.startswith("In") else 2 if k.startswith("Out") else 1) for k in pos}
size = {k: (rng.uniform(20, 50) if role[k] != 1 else rng.uniform(140, 260)) for k in pos}
edges, w = [], []
for a in pos:
    for b in pos:
        if a < b and (role[a] != role[b] or {a, b} == {"Core L", "Core R"}) and rng.random() < 0.55:
            edges.append((a, b)); w.append(10 ** rng.uniform(3, 6))
# -------------------------------------------
gcol = [PALETTE["sage"], PALETTE["ochre"], PALETTE["plum"]]
fig, ax = plt.subplots(figsize=figsize_mm(89, 70))
fig.subplots_adjust(left=0.16, right=0.82, bottom=0.03, top=0.97)
node_link(ax, pos, size, edges, np.log10(w), {k: gcol[role[k]] for k in pos}, edge_color="0.3", curved=0.12,
          edge_alpha=0.75)
for k, (x, y) in pos.items():
    off = 0.2 if role[k] != 1 else 0.3
    ax.text(x, y + off if role[k] == 0 else y - off, k, ha="center", va="bottom" if role[k] == 0 else "top", zorder=5, bbox=dict(boxstyle="square,pad=0.08", fc="white", ec="none", alpha=0.85))
ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.2, 1.85)
for y0, y1, nm in ((1.25, 1.65, "Input"), (0.1, 0.65, "Core"), (-1.05, -0.55, "Output")):
    bracket_label(ax, y0, y1, nm, x=1.0)
key = fig.add_axes([0.01, 0.62, 0.15, 0.3]); key.axis("off")
for i, (v, lw) in enumerate(((1e3, 0.3), (1e4, 0.93), (1e5, 1.57), (1e6, 2.2))):
    key.plot([0, 0.3], [0.8 - 0.22 * i] * 2, color="0.3", lw=lw)
    key.text(0.4, 0.8 - 0.22 * i, f"10$^{int(np.log10(v))}$", va="center")
key.text(0, 1.0, "Weight", va="bottom"); key.set_xlim(0, 1); key.set_ylim(0, 1.1)
export(fig, "G02_node_link")
