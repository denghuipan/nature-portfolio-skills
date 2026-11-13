"""K03 -- Categorical palettes as seen with normal vision and three colour-vision deficiencies.
Use when: choosing series colours. If two categories become indistinguishable in a simulated column, add a
marker / line-style difference or switch to OKABE_ITO.
Simulation: Machado et al. (2009), severity 1.0 (nature_cmaps.simulate_cvd).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

palettes = {"HOUSE": HOUSE, "HOUSE_DARK": HOUSE_DARK, "OKABE_ITO": OKABE_ITO,
            "PAIRED": [c for pair in PAIRED for c in pair], "GRAYS": GRAYS}
views = [("Normal", None), ("Deuteranopia", "deutan"), ("Protanopia", "protan"), ("Tritanopia", "tritan")]
fig, axes = plt.subplots(len(palettes), len(views), figsize=figsize_2col(70),
                         gridspec_kw=dict(wspace=0.06, hspace=0.35, left=0.12, right=0.99, top=0.9, bottom=0.03))
for i, (pname, cols) in enumerate(palettes.items()):
    rgb = np.array([mpl.colors.to_rgb(c) for c in cols])
    for j, (vname, kind) in enumerate(views):
        ax = axes[i, j]
        img = rgb if kind is None else simulate_cvd(rgb, kind)
        ax.imshow(img[None, :, :], aspect="auto")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        if i == 0:
            ax.set_title(vname, fontsize=6, pad=3)
        if j == 0:
            ax.text(-0.04, 0.5, pname, transform=ax.transAxes, ha="right", va="center", fontsize=5.5)
export(fig, "K03_palettes_cvd")
